from pyroll.core import RollPass
from pyroll.core.hooks import Hook

RollPass.wusatowski_temperature_coefficient = Hook[float]()
RollPass.wusatowski_velocity_coefficient = Hook[float]()
RollPass.wusatowski_material_coefficient = Hook[float]()
RollPass.wusatowski_friction_coefficient = Hook[float]()
RollPass.wusatowski_exponent = Hook[float]()

from . import hookimpls
