import numpy as np


def equivalent_height(profile):
    return np.sqrt(profile.cross_section * profile.rotated.height / profile.rotated.width)


def equivalent_width(profile):
    return np.sqrt(profile.cross_section * profile.rotated.width / profile.rotated.height)


def compression(roll_pass):
    return equivalent_height(roll_pass.out_profile) / equivalent_height(roll_pass.in_profile)
