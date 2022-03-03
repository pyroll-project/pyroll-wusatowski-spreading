# Usage of the Plugin

The plugin provides an implementation of the `width_change` hook on `RollPass`, calculation the spread using the
equivalent rectangle approach and Wusatowski's model.

The plugin defines several hooks on `RollPass`, which are used in spread calculation:

| Hook                                 | Description                                   |
|--------------------------------------|-----------------------------------------------|
| `wusatowski_temperature_coefficient` | The temperature correction coefficient $`a`$. |
| `wusatowski_velocity_coefficient`    | The velocity correction coefficient $`c`$.    |
| `wusatowski_material_coefficient`    | The material correction coefficient $`d`$.    |
| `wusatowski_friction_coefficient`    | The friction correction coefficient $`f`$.    |
| `wusatowski_exponent`                | The spread exponent $`w`$.                    |

The plugin provides base implementations of them, so it works out of the box. For `wusatowski_exponent`
and `wusatowski_velocity_coefficient` the equations shown on the [model page](model.md) are implemented. The others
default to 1.

Provide your own hook implementations or set attributes on the `RollPass` instances to alter the spreading behavior.