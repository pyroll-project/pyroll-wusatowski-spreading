import logging

from pyroll.core import BaseRollPass, RollPass, ThreeRollPass, Hook

VERSION = "2.0.2"
PILLAR_MODEL_LOADED = False

BaseRollPass.wusatowski_temperature_coefficient = Hook[float]()
"""Temperature correction factor a for Wusatowski's spread equation."""

BaseRollPass.wusatowski_velocity_coefficient = Hook[float]()
"""Velocity correction factor c for Wusatowski's spread equation."""

BaseRollPass.wusatowski_material_coefficient = Hook[float]()
"""Material correction factor d for Wusatowski's spread equation."""

BaseRollPass.wusatowski_friction_coefficient = Hook[float]()
"""Friction correction factor f for Wusatowski's spread equation."""

BaseRollPass.wusatowski_exponent = Hook[float]()
"""Exponent w for Wusatowski's spread equation."""


@BaseRollPass.wusatowski_temperature_coefficient
def wusatowski_temperature_coefficient(self: BaseRollPass):
    return 1


@BaseRollPass.wusatowski_velocity_coefficient
def wusatowski_velocity_coefficient(self: BaseRollPass):
    return (-0.002958 + 0.00341 * self.draught) * self.velocity + 1.07168 - 0.10431 * self.draught


@BaseRollPass.wusatowski_material_coefficient
def wusatowski_material_coefficient(self: BaseRollPass):
    return 1


@BaseRollPass.wusatowski_friction_coefficient
def wusatowski_friction_coefficient(self: BaseRollPass):
    return 1


@BaseRollPass.wusatowski_exponent
def wusatowski_exponent_low_strain(self: BaseRollPass):
    if self.draught >= 0.5:
        in_equivalent_height = self.in_profile.equivalent_height
        in_equivalent_width = self.in_profile.equivalent_width

        return 10 ** (
                -1.269 * (in_equivalent_height / (2 * self.roll.working_radius)) ** 0.556
                * in_equivalent_width / in_equivalent_height
        )


@BaseRollPass.wusatowski_exponent
def wusatowski_exponent_high_strain(self: BaseRollPass):
    if self.draught < 0.5:
        in_equivalent_height = self.in_profile.equivalent_height
        in_equivalent_width = self.in_profile.equivalent_width

        return 10 ** (
                -3.457 * (in_equivalent_height / (2 * self.roll.working_radius)) ** 0.968
                * in_equivalent_width / in_equivalent_height
        )


@BaseRollPass.OutProfile.width
def width(self: BaseRollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_LOADED and rp.disk_elements):
        if not self.has_set_or_cached("width"):
            return None

        return (
                rp.wusatowski_temperature_coefficient
                * rp.wusatowski_velocity_coefficient
                * rp.wusatowski_material_coefficient
                * rp.wusatowski_friction_coefficient
                * rp.draught ** (-rp.wusatowski_exponent)
        ) * rp.in_profile.width


try:
    # noinspection PyUnresolvedReferences
    @RollPass.DiskElement.pillar_spreads
    def pillar_spreads(self: RollPass.DiskElement):
        rp = self.roll_pass
        return (
                rp.wusatowski_temperature_coefficient
                # * rp.wusatowski_velocity_coefficient
                * rp.wusatowski_material_coefficient
                * rp.wusatowski_friction_coefficient
                * self.pillar_draughts ** (-rp.wusatowski_exponent)
        )


    PILLAR_MODEL_LOADED = True

except AttributeError:
    logging.getLogger(__name__).debug("Pillar model not loaded. Can not register respective hook function.")
