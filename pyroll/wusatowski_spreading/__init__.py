from pyroll.core import RollPass
from pyroll.core.hooks import Hook

RollPass.wusatowski_temperature_coefficient = Hook[float]()
RollPass.wusatowski_velocity_coefficient = Hook[float]()
RollPass.wusatowski_material_coefficient = Hook[float]()
RollPass.wusatowski_friction_coefficient = Hook[float]()
RollPass.wusatowski_exponent = Hook[float]()


@RollPass.wusatowski_temperature_coefficient
def wusatowski_temperature_coefficient(self: RollPass):
    return 1


@RollPass.wusatowski_velocity_coefficient
def wusatowski_velocity_coefficient(self: RollPass):
    return (-0.002958 + 0.00341 * self.draught) * self.velocity + 1.07168 - 0.10431 * self.draught


@RollPass.wusatowski_material_coefficient
def wusatowski_material_coefficient(self: RollPass):
    return 1


@RollPass.wusatowski_friction_coefficient
def wusatowski_friction_coefficient(self: RollPass):
    return 1


@RollPass.wusatowski_exponent
def wusatowski_exponent_low_strain(self: RollPass):
    if self.draught >= 0.5:
        in_equivalent_height = self.in_profile.equivalent_rectangle.height
        in_equivalent_width = self.in_profile.equivalent_rectangle.width

        return 10 ** (
                -1.269 * (in_equivalent_height / (2 * self.roll.working_radius)) ** 0.556
                * in_equivalent_width / in_equivalent_height
        )


@RollPass.wusatowski_exponent
def wusatowski_exponent_high_strain(self: RollPass):
    if self.draught < 0.5:
        in_equivalent_height = self.in_profile.equivalent_rectangle.height
        in_equivalent_width = self.in_profile.equivalent_rectangle.width

        return 10 ** (
                -3.457 * (in_equivalent_height / (2 * self.roll.working_radius)) ** 0.968
                * in_equivalent_width / in_equivalent_height
        )


# noinspection PyUnresolvedReferences
@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass()

    if not self.has_set_or_cached("width"):
        self.width = rp.roll.groove.usable_width

    return (
            rp.wusatowski_temperature_coefficient
            * rp.wusatowski_velocity_coefficient
            * rp.wusatowski_material_coefficient
            * rp.wusatowski_friction_coefficient
            * rp.draught ** (-rp.wusatowski_exponent)
    ) * rp.in_profile.width


RollPass.root_hooks.add(RollPass.OutProfile.width)
