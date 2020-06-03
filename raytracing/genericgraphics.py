import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib import text as mplText
import matplotlib.path as mpath
from typing import List
import numpy as np
import math

class Component:
    def __init__(x:float, y:float, label = ""):
        self.x = x
        self.y = y
        self.label = ""
        self.dx = 0
        self.color = None

    @property
    def width(self):
        raise NotImplemented("Subclass must return width as drawn in data space")

    @property
    def height(self):
        raise NotImplemented("Subclass must return height as drawn in data space")

    def patch(self, axes):
        raise NotImplemented("Subclass must return a matplotlib patch")

    def tinker(self):
        raise NotImplemented("Subclass must return a Tinker drawing command")

    @property
    def centroid(self):
        return self.x + self.width/2, self.y + self.height/2 

    @property
    def boundingBox(self):
        return self.x, self.y, self.x+self.width, self.y+self.height

    def translate(self, dx: float):
        """Translate the label in the x-axis by a small amount 'dx'.

        The offset is stackable and can be removed with the method resetPosition().
        Used by the FigureManager to solve overlapping issues with the labels.
        """
        self.x += dx
        self.dx += dx

    def resetPosition(self):
        """Remove the effect of previous translations."""

        self.x -= dx
        self.dx = 0

class Surface(Component):
    def __init__(self, R, diameter, x, y, label=""):
        self.R = R
        self.halfHeight = diameter / 2
        super(SurfacePatch, self).__init__(x=x, y=y, label=label)        

    def patch(self, axes):
        Path = mpath.Path
        h = self.halfHeight
        R1 = self.R
        v1 = self.x

        if R1 == float("+inf"):
            return Path([(v1, -h), (v1, h)], [Path.MOVETO, Path.LINETO])

        phi1 = math.asin(h / abs(R1))
        delta1 = R1 * (1.0 - math.cos(phi1))
        ctl1 = abs((1.0 - math.cos(phi1)) / math.sin(phi1) * R1)
        corner1 = v1 + delta1

        coords = [(corner1, -h), (v1, -ctl1), (v1, 0),
                  (v1, 0), (v1, ctl1), (corner1, h)]
        actions = [Path.MOVETO, Path.CURVE3, Path.CURVE3,
                   Path.LINETO, Path.CURVE3, Path.CURVE3]

        return patches.PathPatch(Path(coords, actions),
                                 color=[0.85, 0.95, 0.95],
                                 fill=True)
    
class SurfacePair(Component):
    def __init__(self, surfaceA, surfaceB, dx, label=""):
        self.dx = dx
        self.surfaceA = surfaceA
        self.surfaceB = surfaceB
        self.surfaceB.x = surfaceA.x + dx

        super(SurfacePair, self).__init__(x=surfaceA.x, y=surfaceA.y,label )

    def patch(self, axes):
        # FIXME: Line between surfaces
        return patches.PatchCollection([self.surfaceA.patch(),self.surfaceB.patch()])


class Label(Component):
    def __init__(self, text: str, x, y, size='small'):
        self.size = size
        super(LabelPatch, self).__init__(x=x, y=y, label=text)

    def patch(self, axes):
        fontsize = 8
        if size == 'small':
            fontsize = 8

        return mplText.Text(x=self.x, y=self.y, text=self.label, fontsize=fontsize, horizontalalignment='center')


class Aperture(Component):
    def __init__(self, x, y, width=0,label=""):
        self.width = width
        super(Aperture, self).__init__(x=x, y=y, label=label)

    def patch(self):
        if self.width <= 0.01:
            coords = [[self.x - 0.01 / 2, self.y], [self.x + 0.01 / 2, self.y]]
        else:
            coords = [[self.x, self.y], [self.x + width, self.y]]
        return patches.Polygon(coords,
                            linewidth=3,
                            closed=False,
                            color=color)
