from .ray import *
import numpy as np
import collections.abc as collections
import warnings


class RayTrace(Rays):
    def __init__(self, rays):
        super(RayTrace, self).__init__(rays=rays)

