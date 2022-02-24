import sys

from pyroll import RollPass
from . import lib


@RollPass.hookimpl
def wusatowski_temperature_coefficient(roll_pass):
    return 1


@RollPass.hookimpl
def wusatowski_velocity_coefficient(roll_pass):
    compression = lib.compression(roll_pass)
    return (-0.002958 + 0.00341 * compression) * roll_pass.velocity + 1.07168 - 0.10431 * compression


@RollPass.hookimpl
def wusatowski_material_coefficient(roll_pass):
    return 1


@RollPass.hookimpl
def wusatowski_friction_coefficient(roll_pass):
    return 1


@RollPass.hookimpl
def wusatowski_exponent(roll_pass):
    in_equivalent_height = lib.equivalent_height(roll_pass.in_profile)
    in_equivalent_width = lib.equivalent_width(roll_pass.in_profile)
    return 10 ** (
            -1.269 * (in_equivalent_height / 2 / roll_pass.roll_radius) ** 0.56
            * in_equivalent_width / in_equivalent_height
    )


@RollPass.hookimpl
def width_change(roll_pass):
    compression = lib.compression(roll_pass)
    spread = (
            roll_pass.wusatowski_temperature_coefficient
            * roll_pass.wusatowski_velocity_coefficient
            * wusatowski_material_coefficient
            * wusatowski_friction_coefficient
            * compression ** (-wusatowski_exponent)
    )
    out_equivalent_height = lib.equivalent_height(roll_pass.out_profile)

    in_equivalent_width = lib.equivalent_width(roll_pass.in_profile)
    out_equivalent_width = spread * in_equivalent_width

    out_profile_width = out_equivalent_width * roll_pass.out_profile.height / out_equivalent_height
    width_change = out_profile_width - roll_pass.in_profile.rotated.width

    return width_change


RollPass.plugin_manager.register(sys.modules[__name__])
