import envtest  # modifies path
import matplotlib.pyplot as plt

from raytracing import *


class TestAchromatDoubletLens(envtest.RaytracingTestCase):
    def setUp(self):
        # fa, fb, R1, R2, R3, tc1, tc2, te, n1, n2, diameter
        self.parameters = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def testInvalidTC1(self):
        with self.assertRaises(ValueError) as tc1Error:
            self.parameters[5] = -1
            AchromatDoubletLens(*self.parameters)
        self.assertEqual(str(tc1Error.exception), "The first center thickness must be positive.")

    def testInvalidTC2(self):
        with self.assertRaises(ValueError) as tc2Error:
            self.parameters[6] = -1
            AchromatDoubletLens(*self.parameters)
        self.assertEqual(str(tc2Error.exception), "The second center thickness must be positive.")

    def testInvalidTE(self):
        with self.assertRaises(ValueError) as teError:
            self.parameters[7] = -1
            AchromatDoubletLens(*self.parameters)
        self.assertEqual(str(teError.exception), "The edge thickness must be positive.")

    def testInvalidIndexOfRefract1(self):
        with self.assertRaises(ValueError) as n1Error:
            self.parameters[8] = 0.99999
            AchromatDoubletLens(*self.parameters)
        self.assertEqual(str(n1Error.exception), "The index of refraction of the first material must be at least 1.")

    def testInvalidIndexOfRefract2(self):
        with self.assertRaises(ValueError) as n1Error:
            self.parameters[9] = 0.99999
            AchromatDoubletLens(*self.parameters)
        self.assertEqual(str(n1Error.exception), "The index of refraction of the second material must be at least 1.")

    def testInvalidWavelength(self):
        with self.assertRaises(ValueError) as wvlError:
            AchromatDoubletLens(*self.parameters, wavelengthRef=-0.00000000001)
        self.assertEqual(str(wvlError.exception), "Cannot create a lens with a negative defined wavelength.")

    def testInit(self):
        achromat = AchromatDoubletLens(fa=-100.0, fb=-103.6, R1=-52.0, R2=49.9, R3=600.0, tc1=2.0, tc2=4.0, te=7.7,
                                       n1=N_BAK4.n(0.5876), n2=SF5.n(0.5876), diameter=25.4, url='https://www.test.com',
                                       label="testInit Doublet")
        self.assertIsNotNone(achromat)

    def testWarnThickness(self):
        with self.assertWarns(UserWarning):
            achromat = AchromatDoubletLens(fa=125.0, fb=122.0, R1=77.6, R2=-55.9, R3=-160.8, tc1=4.0, tc2=2.8, te=5.0,
                                           n1=N_BK7.n(0.5876), n2=N_SF5.n(0.5876), diameter=25.4,
                                           url='https://www.test.com', label="testThickness Doublet")

    def testWarnBackFocalLength(self):
        with self.assertWarns(UserWarning):
            achromat = AchromatDoubletLens(fa=30.0, fb=22.9, R1=20.89, R2=-16.73, R3=-79.8, tc1=12, tc2=2.0, te=8.8,
                                           n1=N_BAF10.n(0.5876), n2=N_SF6HT.n(0.5876), diameter=25.4,
                                           url='https://www.test.com', label="TestBackFocalLength Doublet")

    def testWarnEffectiveFocalLength(self):
        with self.assertWarns(UserWarning):
            achromat = AchromatDoubletLens(fa=150.00, fb=126.46, R1=92.05, R2=-72.85, R3=-305.87, tc1=23.2, tc2=23.1,
                                           te=36.01, n1=1.6700, n2=1.8467, diameter=75, url="https://www.test.com",
                                           label="TestEffectiveFocalLength Doublet")

    def testPointsOfInterest(self):
        z = 10
        achromat = AchromatDoubletLens(fa=-100.0, fb=-103.6, R1=-52.0, R2=49.9, R3=600.0, tc1=2.0, tc2=4.0, te=7.7,
                                       n1=N_BAK4.n(0.5876), n2=SF5.n(0.5876), diameter=25.4, url='https://www.test.com',
                                       label="testPoI Doublet")
        points = achromat.pointsOfInterest(z)
        f = -1.0 / achromat.C
        p1 = z - (1 - achromat.D) / achromat.C
        ff = p1 - f

        p2 = z + achromat.L + (1 - achromat.A) / achromat.C
        fb = p2 + f

        self.assertIsNotNone(achromat)
        self.assertAlmostEqual(points[0]['z'], ff)
        self.assertAlmostEqual(points[1]['z'], fb)


class TestAchromatDoubletLensSubclasses(envtest.RaytracingTestCase):
    def setUp(self) -> None:
        self.subclasses = AchromatDoubletLens.__subclasses__()

    def testSubclassesInit(self):
        fails = []
        for subclass in self.subclasses:
            achromat = subclass()

            try:
                self.assertIsNotNone(achromat)
            except AssertionError:
                fails.append('{} not properly initiated.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testPointsOfInterest(self):
        fails = []
        z = 0
        for subclass in self.subclasses:
            achromat = subclass()
            points = achromat.pointsOfInterest(z)

            f = -1.0 / achromat.C
            p1 = z - (1 - achromat.D) / achromat.C
            ff = p1 - f

            p2 = z + achromat.L + (1 - achromat.A) / achromat.C
            fb = p2 + f

            try:
                self.assertAlmostEqual(points[0]['z'], ff)
                self.assertAlmostEqual(points[1]['z'], fb)
            except AssertionError:
                fails.append('{} has the wrong points of interest.'.format(subclass.__name__))
        self.assertEqual([], fails)


class TestSingletLens(envtest.RaytracingTestCase):
    def setUp(self):
        # f, fb, R1, R2, tc, te, n, diameter
        self.parameters = [1, 1, 1, 1, 1, 1, 1, 1]

    def testInvalidTC(self):
        with self.assertRaises(ValueError) as tcError:
            self.parameters[4] = -1
            SingletLens(*self.parameters)
        self.assertEqual(str(tcError.exception), "The first center thickness must be positive")

    def testInvalidTE(self):
        with self.assertRaises(ValueError) as teError:
            self.parameters[5] = -1
            SingletLens(*self.parameters)
        self.assertEqual(str(teError.exception), "The edge thickness must be positive.")

    def testInvalidWavelength(self):
        with self.assertRaises(ValueError) as wvlError:
            SingletLens(*self.parameters, wavelengthRef=-0.1)
        self.assertEqual(str(wvlError.exception), "Cannot create a lens with a negative defined wavelength.")

    def testInit(self):
        achromat = SingletLens(f=75.0, fb=72.0, R1=38.6, R2=100000, tc=4.1, te=2.0, n=N_BK7.n(0.5876),
                               diameter=25.4, url='https://www.test.com', label="TestInit Singlet")
        self.assertIsNotNone(achromat)

    def testWarnThickness(self):
        with self.assertWarns(UserWarning):
            achromat = SingletLens(f=63.52, fb=62.41, R1=77.6, R2=-55.9, tc=4.0, te=5.0, n=N_BK7.n(0.5876),
                                   diameter=25.4, url='https://www.test.com', label="testThickness Singlet")

    def testWarnBackFocalLength(self):
        with self.assertWarns(UserWarning):
            achromat = SingletLens(f=15.9, fb=22.9, R1=20.89, R2=-16.73, tc=12, te=1.9, n=N_BAF10.n(0.5876),
                                   diameter=25.4, url='https://www.test.com',
                                   label="TestBackFocalLength Singlet")

    def testWarnEffectiveFocalLength(self):
        with self.assertWarns(UserWarning):
            achromat = SingletLens(f=150.00, fb=57.82, R1=92.05, R2=-72.85, tc=23.2, te=4.8, n=1.6700,
                                   diameter=75, url="https://www.test.com",
                                   label="TestEffectiveFocalLength Singlet")


class TestSingletLensSubclasses(envtest.RaytracingTestCase):
    def setUp(self) -> None:
        self.subclasses = SingletLens.__subclasses__()

    def testSubclassesInit(self):
        fails = []
        for subclass in self.subclasses:
            achromat = subclass()

            try:
                self.assertIsNotNone(achromat)
            except AssertionError:
                fails.append('{} not properly initiated.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testPointsOfInterest(self):
        fails = []
        z = 0
        for subclass in self.subclasses:
            achromat = subclass()
            points = achromat.pointsOfInterest(z)

            f = -1.0 / achromat.C
            p1 = z - (1 - achromat.D) / achromat.C
            ff = p1 - f

            p2 = z + achromat.L + (1 - achromat.A) / achromat.C
            fb = p2 + f

            try:
                self.assertAlmostEqual(points[0]['z'], ff)
                self.assertAlmostEqual(points[1]['z'], fb)
            except AssertionError:
                fails.append('{} has the wrong points of interest.'.format(subclass.__name__))
        self.assertEqual([], fails)


class TestObjectives(envtest.RaytracingTestCase):
    def testInvalidNA(self):
        # f, NA, focusToFocusLength, backAperture, workingDistance
        parameters = [1, -0.1, 10, 2, 4]
        with self.assertRaises(ValueError) as naError:
            Objective(*parameters)
        self.assertEqual(str(naError.exception), "The numerical aperture NA must be positive.")

    def testInit(self):
        objective = Objective(f=180 / 40, NA=0.8, focusToFocusLength=40, backAperture=7, workingDistance=2,
                              label='TestInit Objective', url="https://www.test.com")
        self.assertIsNotNone(objective)

    def testWarnNotFullyTested(self):
        Objective.warningDisplayed = False

        with self.assertWarns(FutureWarning):
            objective = Objective(f=180 / 40, NA=0.8, focusToFocusLength=40, backAperture=7, workingDistance=2,
                                  label='TestWarn Objective', url="https://www.test.com")

        self.assertTrue(Objective.warningDisplayed)

    def testFlipOrientation(self):
        original = Objective(f=180 / 40, NA=0.8, focusToFocusLength=40, backAperture=7, workingDistance=2,
                             label='TestFlip Objective', url="https://www.test.com")
        flipped = Objective(f=180 / 40, NA=0.8, focusToFocusLength=40, backAperture=7, workingDistance=2,
                            label='TestFlip Objective', url="https://www.test.com")
        flipped.flipOrientation()

        self.assertFalse(original.isFlipped)
        self.assertTrue(flipped.isFlipped)
        self.assertNotEqual(original.frontVertex, flipped.frontVertex)
        self.assertNotEqual(original.backVertex, flipped.backVertex)

    def testFlipOrientationAfterFlip(self):
        original = Objective(f=180 / 40, NA=0.8, focusToFocusLength=40, backAperture=7, workingDistance=2,
                             label='TestFlip Objective', url="https://www.test.com")
        original.flipOrientation()
        original.flipOrientation()
        self.assertFalse(original.isFlipped)
        self.assertEqual(original.backVertex, 38)
        self.assertEqual(original.frontVertex, 0)

    def testPointsOfInterest(self):
        z = 10
        objective = Objective(f=180 / 40, NA=0.8, focusToFocusLength=40, backAperture=7, workingDistance=2,
                              label='TestPoI Objective', url="https://www.test.com")
        points = objective.pointsOfInterest(z)
        ff = z + objective.focusToFocusLength
        fb = z

        self.assertAlmostEqual(points[0]['z'], fb)
        self.assertAlmostEqual(points[1]['z'], ff)

    def testPointsOfInterestFlipped(self):
        z = 10
        objective = Objective(f=180 / 40, NA=0.8, focusToFocusLength=40, backAperture=7, workingDistance=2,
                              label='TestPoI Objective', url="https://www.test.com")
        points = objective.pointsOfInterest(z)
        ff = z + objective.focusToFocusLength
        fb = z
        self.assertAlmostEqual(points[0]['z'], fb)
        self.assertAlmostEqual(points[1]['z'], ff)

        objective.flipOrientation()
        points = objective.pointsOfInterest(z)
        self.assertAlmostEqual(points[0]['z'], ff)
        self.assertAlmostEqual(points[1]['z'], fb)


class TestObjectivesSubclasses(envtest.RaytracingTestCase):
    def setUp(self) -> None:
        self.subclasses = Objective.__subclasses__()

    def testSubclassesInit(self):
        fails = []
        for subclass in self.subclasses:
            objective = subclass()

            try:
                self.assertIsNotNone(objective)
            except AssertionError:
                fails.append('{} not properly initiated.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testFlipOrientation(self):
        fails = []
        for subclass in self.subclasses:
            original = subclass()
            flipped = subclass().flipOrientation()

            try:
                self.assertFalse(original.isFlipped)
                self.assertTrue(flipped.isFlipped)
                self.assertNotEqual(original.frontVertex, flipped.frontVertex)
                self.assertNotEqual(original.backVertex, flipped.backVertex)
            except AssertionError:
                fails.append('{} was not properly flipped.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testPointsOfInterest(self):
        fails = []
        z = 10
        for subclass in self.subclasses:
            objective = subclass()
            points = objective.pointsOfInterest(z)
            ff = z + objective.focusToFocusLength
            fb = z

            try:
                self.assertAlmostEqual(points[0]['z'], fb)
                self.assertAlmostEqual(points[1]['z'], ff)
            except AssertionError:
                fails.append('{} has the wrong point of interest.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testPointsOfInterestFlipped(self):
        fails = []
        z = 10
        for subclass in self.subclasses:
            objective = subclass()
            points = objective.pointsOfInterest(z)
            ff = z + objective.focusToFocusLength
            fb = z

            try:
                self.assertAlmostEqual(points[0]['z'], fb)
                self.assertAlmostEqual(points[1]['z'], ff)

                objective.flipOrientation()
                points = objective.pointsOfInterest(z)
                self.assertAlmostEqual(points[0]['z'], ff)
                self.assertAlmostEqual(points[1]['z'], fb)
            except AssertionError:
                fails.append('{} has the wrong point of interest.'.format(subclass.__name__))
        self.assertEqual([], fails)


if __name__ == '__main__':
    envtest.main()
