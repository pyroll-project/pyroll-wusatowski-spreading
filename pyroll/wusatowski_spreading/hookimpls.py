import logging
from pyroll.core import RollPass


@RollPass.hookimpl
def wusatowski_temperature_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def wusatowski_velocity_coefficient(roll_pass):
    compression = (roll_pass.out_profile.equivalent_rectangle.height
                   / roll_pass.in_profile.equivalent_rectangle.height)
    return (-0.002958 + 0.00341 * compression) * roll_pass.velocity + 1.07168 - 0.10431 * compression


@RollPass.hookimpl
def wusatowski_material_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def wusatowski_friction_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl(specname="wusatowski_exponent")
def wusatowski_exponent_low_strain(roll_pass: RollPass):
    compression = (roll_pass.out_profile.equivalent_rectangle.height
                   / roll_pass.in_profile.equivalent_rectangle.height)

    if compression >= 0.5:
        in_equivalent_height = roll_pass.in_profile.equivalent_rectangle.height
        in_equivalent_width = roll_pass.in_profile.equivalent_rectangle.width

        return 10 ** (
                -1.269 * (in_equivalent_height / (2 * roll_pass.roll.working_radius)) ** 0.556
                * in_equivalent_width / in_equivalent_height
        )


@RollPass.hookimpl(specname="wusatowski_exponent")
def wusatowski_exponent_high_strain(roll_pass: RollPass):
    compression = (roll_pass.out_profile.equivalent_rectangle.height
                   / roll_pass.in_profile.equivalent_rectangle.height)

    if compression < 0.5:
        in_equivalent_height = roll_pass.in_profile.equivalent_rectangle.height
        in_equivalent_width = roll_pass.in_profile.equivalent_rectangle.width

        return 10 ** (
                -3.457 * (in_equivalent_height / (2 * roll_pass.roll.working_radius)) ** 0.968
                * in_equivalent_width / in_equivalent_height
        )


@RollPass.hookimpl
def spread(roll_pass: RollPass):
    compression = (roll_pass.out_profile.equivalent_rectangle.height
                   / roll_pass.in_profile.equivalent_rectangle.height)
    return (
            roll_pass.wusatowski_temperature_coefficient
            * roll_pass.wusatowski_velocity_coefficient
            * roll_pass.wusatowski_material_coefficient
            * roll_pass.wusatowski_friction_coefficient
            * compression ** (-roll_pass.wusatowski_exponent)
    )
