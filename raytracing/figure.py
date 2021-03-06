from .graphics import *
from .ray import Ray
import matplotlib.pyplot as plt
import itertools
import warnings
import sys


class Figure:
    """Base class to contain the required objects of a figure.
    Promote to a backend-derived Figure class to enable display features.
    """
    def __init__(self, opticalPath):
        self.path = opticalPath

        self.graphics = []
        self.lines = []
        self.labels = []
        self.points = []
        self.annotations = []

        self.styles = dict()
        self.styles['default'] = {'rayColors': ['b', 'r', 'g'], 'onlyAxialRay': False,
                                  'imageColor': 'r', 'objectColor': 'b', 'onlyPrincipalAndAxialRays': True,
                                  'limitObjectToFieldOfView': True, 'removeBlockedRaysCompletely': False}
        self.styles['publication'] = self.styles['default'].copy()
        self.styles['presentation'] = self.styles['default'].copy()  # same as default for now
        self.styles['publication'].update({'rayColors': ['0.4', '0.2', '0.6'],
                                           'imageColor': '0.3', 'objectColor': '0.1'})

        self.designParams = self.styles['default']

    def design(self, style: str = None,
               rayColors: List[Union[str, tuple]] = None, onlyAxialRay: bool = None,
               imageColor: Union[str, tuple] = None, objectColor: Union[str, tuple] = None):
        """ Update the design parameters of the figure.
        All parameters are None by default to allow for the update of one parameter at a time.

        Parameters
        ----------
        style: str, optional
            Set all design parameters following a supported design style : 'default', 'presentation', 'publication'.
        rayColors : List[Union[str, tuple]], optional
            List of the colors to use for the three different ray type. Default is ['b', 'r', 'g'].
        onlyAxialRay : bool, optional
            Only draw the ray fan coming from the center of the object (axial ray).
            Works with fanAngle and fanNumber. Default to False.
        imageColor : Union[str, tuple], optional
            Color of image arrows. Default to 'r'.
        objectColor : Union[str, tuple], optional
            Color of object arrow. Default to 'b'.
        """
        if style is not None:
            if style in self.styles.keys():
                self.designParams = self.styles[style]
            else:
                raise ValueError("Available styles are : {}".format(self.styles.keys()))

        newDesignParams = {'rayColors': rayColors, 'onlyAxialRay': onlyAxialRay,
                           'imageColor': imageColor, 'objectColor': objectColor}
        for key, value in newDesignParams.items():
            if value is not None:
                self.designParams[key] = value

    def initializeDisplay(self):
        """ Configure the imaging path and the figure according to the display conditions. """

        note1 = ""
        note2 = ""
        if self.designParams['limitObjectToFieldOfView']:
            fieldOfView = self.path.fieldOfView()
            if fieldOfView != float('+Inf'):
                self.path.objectHeight = fieldOfView
                note1 = "FOV: {0:.2f}".format(self.path.objectHeight)
            else:
                warnings.warn("Infinite field of view: cannot use limitObjectToFieldOfView=True.")
                self.designParams['limitObjectToFieldOfView'] = False

            imageSize = self.path.imageSize()
            if imageSize != float('+Inf'):
                note1 += " Image size: {0:.2f}".format(imageSize)
            else:
                warnings.warn("Infinite image size: cannot use limitObjectToFieldOfView=True.")
                self.designParams['limitObjectToFieldOfView'] = False

        if not self.designParams['limitObjectToFieldOfView']:
            note1 = "Object height: {0:.2f}".format(self.path.objectHeight)

        if self.designParams['onlyPrincipalAndAxialRays']:
            (stopPosition, stopDiameter) = self.path.apertureStop()
            if stopPosition is None or self.path.principalRay() is None:
                warnings.warn("No aperture stop in system: cannot use onlyPrincipalAndAxialRays=True since they are "
                              "not defined.")
                self.designParams['onlyPrincipalAndAxialRays'] = False
            else:
                note2 = "Only chief and marginal rays shown"

        label = Label(x=0.05, y=0.02, text=note1 + "\n" + note2, fontsize=11, useDataUnits=False, alignment='left')
        self.labels.append(label)

    def setGraphicsFromPath(self):
        self.graphics = self.graphicsOfElements

        if self.path.showObject:
            self.graphics.append(self.graphicOfObject)
        if self.path.showImages:
            self.graphics.extend(self.graphicsOfImages)

        if self.path.showEntrancePupil:
            (pupilPosition, pupilDiameter) = self.path.entrancePupil()
            if pupilPosition is not None:
                self.graphics.append(self.graphicOfEntrancePupil)

        if self.path.showPointsOfInterest:
            self.points.extend(self.pointsOfInterest)
            self.labels.extend(self.stopsLabels)

    @property
    def graphicsOfElements(self) -> List[Graphic]:
        maxRayHeight = 0
        for line in self.lines:
            if line.label == 'ray':  # FIXME: need a more robust reference to rayTraces
                if max(line.yData) > maxRayHeight:
                    maxRayHeight = max(line.yData)

        graphics = []
        z = 0
        for element in self.path.elements:
            graphic = GraphicOf(element, x=z, minSize=maxRayHeight)
            if type(graphic) is list:  # MatrixGroup creates stand-alone graphics for now
                graphics.extend(graphic)
            elif graphic is not None:
                graphics.append(graphic)
            z += element.L
        return graphics

    @property
    def graphicOfObject(self) -> Graphic:
        objectArrow = Arrow(dy=self.path.objectHeight, y=-self.path.objectHeight / 2, color='b')
        objectGraphic = Graphic([objectArrow], x=self.path.objectPosition)
        return objectGraphic

    @property
    def graphicsOfImages(self) -> List[Graphic]:
        imageGraphics = []

        images = self.path.intermediateConjugates()

        for (imagePosition, magnification) in images:
            imageHeight = magnification * self.path.objectHeight

            arrow = Arrow(dy=imageHeight, y=-imageHeight / 2, color='r')
            graphic = Graphic([arrow], x=imagePosition)

            imageGraphics.append(graphic)

        return imageGraphics

    @property
    def graphicOfEntrancePupil(self) -> Graphic:
        (pupilPosition, pupilDiameter) = self.path.entrancePupil()
        if pupilPosition is not None:
            halfHeight = pupilDiameter / 2.0

            return Graphic([ApertureBars(halfHeight)], x=pupilPosition)

    @property
    def pointsOfInterest(self) -> List[Point]:
        """
        Labels of general points of interest are drawn below the
        axis, at 25% of the largest diameter.
        """
        labels = {}  # Gather labels at same z

        # For the group as a whole, then each element
        for pointOfInterest in self.path.pointsOfInterest(z=0):
            zStr = "{0:3.3f}".format(pointOfInterest['z'])
            label = pointOfInterest['label']
            if zStr in labels:
                labels[zStr] = labels[zStr] + ", " + label
            else:
                labels[zStr] = label

        # Points of interest for each element
        zElement = 0
        groupIndex = 0
        physicalElements = [element for element in self.path.elements if type(element).__name__ != 'Space']

        for element in self.path.elements:
            pointsOfInterest = element.pointsOfInterest(zElement)
            if pointsOfInterest:
                groupIndex += 1

            for pointOfInterest in pointsOfInterest:
                zStr = "{0:3.3f}".format(pointOfInterest['z'])
                label = pointOfInterest['label']
                if len(physicalElements) > 1:
                    label = '{' + label.strip('$') + '}'
                    label = '${}_{}$'.format(label, groupIndex)
                if zStr in labels:
                    labels[zStr] = labels[zStr] + ", " + label
                else:
                    labels[zStr] = label
            zElement += element.L

        points = []
        halfHeight = self.displayRange / 2
        for zStr, label in labels.items():
            points.append(Point(text=label, x=float(zStr), y=-halfHeight * 0.5))
        return points

    @property
    def stopsLabels(self) -> List[Label]:
        """ AS and FS are drawn at 110% of the largest diameter. """
        labels = []
        halfHeight = self.displayRange / 2

        (apertureStopPosition, apertureStopDiameter) = self.path.apertureStop()
        if apertureStopPosition is not None:
            labels.append(Label('AS', apertureStopPosition, halfHeight * 1.1, fontsize=18))

        (fieldStopPosition, fieldStopDiameter) = self.path.fieldStop()
        if fieldStopPosition is not None:
            labels.append(Label('FS', fieldStopPosition, halfHeight * 1.1, fontsize=18))

        return labels

    @property
    def displayRange(self):
        """ The maximum height of the objects in the optical path. """
        from .laserpath import LaserPath   # Fixme: circular import fix

        if isinstance(self.path, LaserPath):
            return self.laserDisplayRange
        else:
            return self.imagingDisplayRange

    @property
    def imagingDisplayRange(self):
        displayRange = 0
        for graphic in self.graphicsOfElements:
            if graphic.halfHeight * 2 > displayRange:
                displayRange = graphic.halfHeight * 2

        if displayRange == float('+Inf') or displayRange <= self.path._objectHeight:
            displayRange = self.path._objectHeight

        conjugates = self.path.intermediateConjugates()
        if len(conjugates) != 0:
            for (planePosition, magnification) in conjugates:
                if not 0 <= planePosition <= self.path.L:
                    continue
                magnification = abs(magnification)
                if displayRange < self.path._objectHeight * magnification:
                    displayRange = self.path._objectHeight * magnification

        return displayRange

    @property
    def laserDisplayRange(self):
        displayRange = 0
        for graphic in self.graphicsOfElements:
            if graphic.halfHeight * 2 > displayRange:
                displayRange = graphic.halfHeight * 2

        if displayRange == float('+Inf') or displayRange == 0:
            if self.path.inputBeam is not None:
                displayRange = self.path.inputBeam.w * 3
            else:
                displayRange = 100

        return displayRange

    def rayTraceLines(self, rays) -> List[Line]:
        """ A list of all ray trace line objects corresponding to either
        1. the group of rays defined by the user (fanAngle, fanNumber, rayNumber).
        2. the principal and axial rays.
        """

        colors = self.designParams['rayColors']

        linewidth = 0.5
        manyRayTraces = self.path.traceMany(rays)

        maxHeight = 0
        for rayTrace in manyRayTraces:
            (x, y) = self.rearrangeRayTraceForPlotting(rayTrace)
            if len(y) == 0:
                continue
            if abs(y[0]) > maxHeight:
                maxHeight = abs(y[0])

        lines = []
        for rayTrace in manyRayTraces:
            (x, y) = self.rearrangeRayTraceForPlotting(rayTrace)

            if len(y) == 0:
                continue  # nothing to plot, ray was fully blocked

            if maxHeight == 0:  # only axial ray
                colorIndex = 1
            else:
                colorIndex = int(np.round(
                    (y[0] + maxHeight) / (maxHeight * 2) * (len(colors) - 1)))
                colorIndex = colorIndex % len(colors)

            line = Line(x, y, color=colors[colorIndex], lineWidth=linewidth, label='ray')
            lines.append(line)

        return lines

    def beamTraceLines(self, beam) -> List[Line]:
        """ Draw beam trace corresponding to input beam
        Because the laser beam diffracts through space, we cannot
        simply propagate the beam over large distances and trace it
        (as opposed to rays, where we can). We must split Space()
        elements into sub elements to watch the beam size expand.

        We arbitrarily split Space() elements into N sub elements
        before plotting.
        """
        from .imagingpath import ImagingPath  # Fixme: circular import fix
        from .matrix import Space

        N = 100
        highResolution = ImagingPath()
        for element in self.path.elements:
            if isinstance(element, Space):
                for i in range(N):
                    highResolution.append(Space(d=element.L / N,
                                                n=element.frontIndex))
            else:
                highResolution.append(element)

        beamTrace = highResolution.trace(beam)
        x, y = self.rearrangeBeamTraceForPlotting(beamTrace)

        lines = [Line(x, y, 'r'),
                 Line(x, [-v for v in y], 'r')]

        return lines

    def beamWaistAnnotations(self, beam) -> List[ArrowAnnotation]:
        """ Draws the expected waist (i.e. the focal spot or the spot where the
        size is minimum) for all positions of the beam. This will show "waists" that
        are virtual if there is an additional lens between the beam and the expected
        waist.

        It is easy to obtain the waist position from the complex radius of curvature
        because it is the position where the complex radius is imaginary. The position
        returned is relative to the position of the beam, which is why we add the actual
        position of the beam to the relative position. """

        annotations = []
        arrowLength = self.laserDisplayRange * 0.1

        beamTrace = self.path.trace(beam)
        for beam in beamTrace:
            relativePosition = beam.waistPosition
            position = beam.z + relativePosition
            size = beam.waist
            if not 0 <= position <= self.path.L:
                continue

            annotations.append(ArrowAnnotation((position, size + arrowLength), (position, size),
                                               color='g', arrowStyle='->'))
            annotations.append(ArrowAnnotation((position, -size + -arrowLength), (position, -size),
                                               color='g', arrowStyle='->'))

        return annotations

    def rearrangeRayTraceForPlotting(self, rayList: List[Ray]):
        """
        This function removes the rays that are blocked in the imaging path.
        Parameters
        ----------
        rayList : List of Rays
            an object from rays class or a list of rays
        """
        x = []
        y = []
        for ray in rayList:
            if not ray.isBlocked:
                x.append(ray.z)
                y.append(ray.y)
            elif self.designParams['removeBlockedRaysCompletely']:
                return [], []
            # else: # ray will simply stop drawing from here
        return x, y

    @staticmethod
    def rearrangeBeamTraceForPlotting(rayList):
        x = []
        y = []
        for ray in rayList:
            x.append(ray.z)
            y.append(ray.w)
        return x, y

    @property
    def mplFigure(self) -> 'MplFigure':
        figure = MplFigure(opticalPath=self.path)
        figure.graphics = self.graphics
        figure.lines = self.lines
        figure.labels = self.labels
        figure.points = self.points
        figure.annotations = self.annotations
        figure.designParams = self.designParams
        return figure

    def display(self, raysList, comments=None, title=None, backend='matplotlib', display3D=False, filepath=None):
        self.initializeDisplay()

        self.lines = []
        for rays in raysList:
            rayTrace = self.rayTraceLines(rays=rays)
            self.lines.extend(rayTrace)

        self.setGraphicsFromPath()

        if backend is 'matplotlib':
            mplFigure = self.mplFigure
            mplFigure.create(comments, title)
            if display3D:
                mplFigure.display3D(filepath=filepath)
            else:
                mplFigure.display2D(filepath=filepath)
        else:
            raise NotImplementedError("The only supported backend is matplotlib.")

    def displayGaussianBeam(self, beams=None,
                            title=None, comments=None, backend='matplotlib', display3D=False, filepath=None):
        self.lines = []
        self.graphics = self.graphicsOfElements
        for beam in beams:
            self.lines.extend(self.beamTraceLines(beam))
            self.annotations.extend(self.beamWaistAnnotations(beam))

        if backend is 'matplotlib':
            mplFigure = self.mplFigure
            mplFigure.create(comments, title)
            if display3D:
                mplFigure.display3D(filepath=filepath)
            else:
                mplFigure.display2D(filepath=filepath)
        else:
            raise NotImplementedError("The only supported backend is matplotlib.")


class MplFigure(Figure):
    """Matplotlib Figure"""
    def __init__(self, opticalPath):
        super().__init__(opticalPath)

        self.figure = None
        self.axes = None
        self.axesComments = None

    def create(self, comments=None, title=None):
        if comments is not None:
            self.figure, (self.axes, self.axesComments) = plt.subplots(2, 1, figsize=(10, 7))
            self.axesComments.axis('off')
            self.axesComments.text(0., 1.0, comments, transform=self.axesComments.transAxes,
                                   fontsize=10, verticalalignment='top')
        else:
            self.figure, self.axes = plt.subplots(figsize=(10, 7))

        self.axes.set(xlabel='Distance', ylabel='Height', title=title)

    def display2D(self, filepath=None):
        self.draw()

        self.axes.callbacks.connect('ylim_changed', self.onZoomCallback)
        plt.connect('resize_event', self.onZoomCallback)

        if filepath is not None:
            self.figure.savefig(filepath, dpi=600)
        else:
            self._showPlot()

    def display3D(self, filepath=None):
        raise NotImplementedError()

    def draw(self):
        self.drawGraphics()
        self.drawPoints()
        self.drawLabels()

        for line in self.lines:
            self.axes.add_line(line.patch)

        for annotation in self.annotations:
            self.axes.add_patch(annotation.patch)

        self.updateDisplayRange()
        self.updateGraphics()
        self.updateLabels()

    def drawGraphics(self):
        for graphic in self.graphics:
            componentPatches = graphic.patches2D

            for patch in componentPatches:
                self.axes.add_patch(patch)

            if graphic.hasLabel:
                graphic.label = graphic.label.mplLabel
                self.axes.add_artist(graphic.label.patch)

            self.points.extend(graphic.points)

            for line in graphic.lines:
                self.axes.add_line(line.patch)

            for annotation in graphic.annotations:
                self.axes.add_patch(annotation.patch)

    def drawPoints(self):
        for point in self.points:
            if point.hasPointMarker:
                self.axes.plot([point.x], [0], 'ko', markersize=3, color=point.color, linewidth=0.4)
            if point.text is not None:
                self.labels.append(point)

    def drawLabels(self):
        self.labels = [label.mplLabel for label in self.labels]

        for label in self.labels:
            artist = label.patch
            if not label.useDataUnits:
                artist.set_transform(self.axes.transAxes)
            self.axes.add_artist(artist)

    def updateGraphics(self):
        for graphic in self.graphics:
            xScaling, yScaling = self.scalingOfGraphic(graphic)

            translation = transforms.Affine2D().translate(graphic.x, graphic.y)
            noScale = transforms.Affine2D().scale(1, 1)
            scaling = transforms.Affine2D().scale(xScaling, yScaling)

            for component in graphic.components:
                if component.hasFixedWidth:
                    component.patch.set_transform(noScale + translation + self.axes.transData)
                else:
                    component.patch.set_transform(scaling + translation + self.axes.transData)

            if graphic.hasLabel:
                graphic.label.patch.set_transform(translation + self.axes.transData)

    def updateLabels(self):
        self.resetLabelOffsets()
        self.fixLabelOverlaps()

    def resetLabelOffsets(self):
        """Reset previous offsets applied to the labels.

        Used with a zoom callback to properly replace the labels.
        """
        for graphic in self.graphics:
            if graphic.hasLabel:
                graphic.label.resetPosition()

        for label in self.labels:
            label.resetPosition()

    def getRenderedLabels(self) -> List[MplLabel]:
        """List of labels rendered inside the current display."""
        labels = []
        for graphic in self.graphics:
            if graphic.hasLabel:
                if graphic.label.isRenderedOn(self.figure):
                    labels.append(graphic.label)

        for label in self.labels:
            if label.isRenderedOn(self.figure):
                labels.append(label)

        return labels

    def fixLabelOverlaps(self, maxIteration: int = 5):
        """Iteratively identify overlapping label pairs and move them apart in x-axis."""
        labels = self.getRenderedLabels()
        if len(labels) < 2:
            return

        i = 0
        while i < maxIteration:
            noOverlap = True
            boxes = [label.boundingBox(self.axes, self.figure) for label in labels]
            for (a, b) in itertools.combinations(range(len(labels)), 2):
                boxA, boxB = boxes[a], boxes[b]

                if boxA.overlaps(boxB):
                    noOverlap = False
                    if boxB.x1 > boxA.x1:
                        requiredSpacing = boxA.x1 - boxB.x0
                    else:
                        requiredSpacing = boxA.x0 - boxB.x1

                    self.translateLabel(labels[a], boxA, dx=-requiredSpacing/2)
                    self.translateLabel(labels[b], boxB, dx=requiredSpacing/2)

            i += 1
            if noOverlap:
                break

    def translateLabel(self, label, bbox, dx):
        """Internal method to translate a label and make sure it stays inside the display."""
        label.translate(dx)

        xMin, xMax = self.axes.get_xlim()
        if bbox.x0 + dx < xMin:
            label.translate(xMin - (bbox.x0 + dx))
        elif bbox.x1 + dx > xMax:
            label.translate(xMax - (bbox.x1 + dx))

    def updateDisplayRange(self):
        """Set a symmetric Y-axis display range defined as 1.5 times the maximum halfHeight of all graphics."""
        halfDisplayHeight = self.displayRange/2 * 1.5
        self.axes.autoscale()
        self.axes.set_ylim(-halfDisplayHeight, halfDisplayHeight)

    def onZoomCallback(self, axes):
        self.updateGraphics()
        self.updateLabels()

    def scalingOfGraphic(self, graphic):
        xScale, yScale = self.axesToDataScale()

        heightFactor = graphic.halfHeight * 2 / yScale
        xScaling = xScale * (heightFactor / 0.2) ** (3 / 4)

        return xScaling, 1

    def axesToDataScale(self):
        """ Dimensions of the figure in data units. """
        xScale, yScale = self.axes.viewLim.bounds[2:]

        return xScale, yScale

    def _showPlot(self):
        try:
            plt.plot()
            if sys.platform.startswith('win'):
                plt.show()
            else:
                plt.draw()
                while True:
                    if plt.get_fignums():
                        plt.pause(0.001)
                    else:
                        break

        except KeyboardInterrupt:
            plt.close()
