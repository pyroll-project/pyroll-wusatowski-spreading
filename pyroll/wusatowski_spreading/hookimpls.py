from pyroll.core import RollPass


@RollPass.wusatowski_temperature_coefficient
def wusatowski_temperature_coefficient(self: RollPass):
    return 1


@RollPass.wusatowski_velocity_coefficient
def wusatowski_velocity_coefficient(self: RollPass):
    compression = (self.out_profile.equivalent_rectangle.height
                   / self.in_profile.equivalent_rectangle.height)
    return (-0.002958 + 0.00341 * compression) * self.velocity + 1.07168 - 0.10431 * compression


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


@RollPass.spread
def spread(self: RollPass):
    return (
            self.wusatowski_temperature_coefficient
            * self.wusatowski_velocity_coefficient
            * self.wusatowski_material_coefficient
            * self.wusatowski_friction_coefficient
            * self.draught ** (-self.wusatowski_exponent)
    )
