import unittest
import envtest # modifies path
from raytracing import *


class TestMaterial(unittest.TestCase):
    def testMaterialInvalid(self):
        self.assertRaises(TypeError, Material.n, 5)


class TestMaterialSubclasses(unittest.TestCase):
    def setUp(self) -> None:
        self.subclasses = []

        for material in dir(materials):
            object = getattr(materials, material)
            try:
                if (object != Material) and issubclass(object, Material):
                    self.subclasses.append(object)
            except TypeError:
                pass

    def testMaterialSubclassesTypeError(self):
        for subclass in self.subclasses:
            self.assertRaises(TypeError, subclass.n, None)
            self.assertRaises(TypeError, subclass.n, 'test')

    def testMaterialSubclassesValueErrors(self):
        for subclass in self.subclasses:
            self.assertRaises(ValueError, subclass.n, 100)
            self.assertRaises(ValueError, subclass.n, 0)
            self.assertRaises(ValueError, subclass.n, -100)

    def testMaterialSubclasses(self):
        for subclass in self.subclasses:
            print(subclass)


class TestN_BK7(unittest.TestCase):
    def testN_BK7TypeErrors(self):
        self.assertRaises(TypeError, N_BK7.n, None)
        self.assertRaises(TypeError, N_BK7.n, 'test')

    def testN_BK7ValueErrors(self):
        self.assertRaises(ValueError, N_BK7.n, 100)
        self.assertRaises(ValueError, N_BK7.n, 0)
        self.assertRaises(ValueError, N_BK7.n, -100)

    def testN_BK7(self):
        self.assertEqual(1.3965252243506636, N_BK7.n(5))


class TestN_SF2(unittest.TestCase):
    def testN_SF2TypeErrors(self):
        self.assertRaises(TypeError, N_SF2.n, None)
        self.assertRaises(TypeError, N_SF2.n, 'test')

    def testN_SF2ValueErrors(self):
        self.assertRaises(ValueError, N_SF2.n, 100)
        self.assertRaises(ValueError, N_SF2.n, 0)
        self.assertRaises(ValueError, N_SF2.n, -100)

    def testN_SF2(self):
        self.assertEqual(1.5178527121226975, N_SF2.n(5))


class TestSF2(unittest.TestCase):
    def testSF2TypeErrors(self):
        self.assertRaises(TypeError, SF2.n, None)
        self.assertRaises(TypeError, SF2.n, 'test')

    def testSF2ValueErrors(self):
        self.assertRaises(ValueError, SF2.n, 100)
        self.assertRaises(ValueError, SF2.n, 0)
        self.assertRaises(ValueError, SF2.n, -100)

    def testSF2(self):
        self.assertEqual(1.5385861348077337, SF2.n(5))


class TestSF5(unittest.TestCase):
    def testSF5TypeErrors(self):
        self.assertRaises(TypeError, SF5.n, None)
        self.assertRaises(TypeError, SF5.n, 'test')

    def testSF5ValueErrors(self):
        self.assertRaises(ValueError, SF5.n, 100)
        self.assertRaises(ValueError, SF5.n, 0)
        self.assertRaises(ValueError, SF5.n, -100)

    def testSF5(self):
        self.assertEqual(1.5612286489801115, SF5.n(5))


class TestN_SF5(unittest.TestCase):
    def testN_SF5TypeErrors(self):
        self.assertRaises(TypeError, N_SF5.n, None)
        self.assertRaises(TypeError, N_SF5.n, 'test')

    def testN_SF5ValueErrors(self):
        self.assertRaises(ValueError, N_SF5.n, 100)
        self.assertRaises(ValueError, N_SF5.n, 0)
        self.assertRaises(ValueError, N_SF5.n, -100)

    def testN_SF5(self):
        self.assertEqual(1.539610715563772, N_SF5.n(5))


class TestN_SF6HT(unittest.TestCase):
    def testN_SF6HTTypeErrors(self):
        self.assertRaises(TypeError, N_SF6HT.n, None)
        self.assertRaises(TypeError, N_SF6HT.n, 'test')

    def testN_SF6HTValueErrors(self):
        self.assertRaises(ValueError, N_SF6HT.n, 100)
        self.assertRaises(ValueError, N_SF6HT.n, 0)
        self.assertRaises(ValueError, N_SF6HT.n, -100)

    def testN_SF6HT(self):
        self.assertEqual(1.664053106820355, N_SF6HT.n(5))


class TestN_SF10(unittest.TestCase):
    def testN_SF10TypeErrors(self):
        self.assertRaises(TypeError, N_SF10.n, None)
        self.assertRaises(TypeError, N_SF10.n, 'test')

    def testN_SF10ValueErrors(self):
        self.assertRaises(ValueError, N_SF10.n, 100)
        self.assertRaises(ValueError, N_SF10.n, 0)
        self.assertRaises(ValueError, N_SF10.n, -100)

    def testN_SF10(self):
        self.assertEqual(1.5948478106562147, N_SF10.n(5))


class TestN_SF11(unittest.TestCase):
    def testN_SF11TypeErrors(self):
        self.assertRaises(TypeError, N_SF11.n, None)
        self.assertRaises(TypeError, N_SF11.n, 'test')

    def testN_SF11ValueErrors(self):
        self.assertRaises(ValueError, N_SF11.n, 100)
        self.assertRaises(ValueError, N_SF11.n, 0)
        self.assertRaises(ValueError, N_SF11.n, -100)

    def testN_SF11(self):
        self.assertEqual(1.6396821789377511, N_SF11.n(5))


class TestN_BAF10(unittest.TestCase):
    def testN_BAF10TypeErrors(self):
        self.assertRaises(TypeError, N_BAF10.n, None)
        self.assertRaises(TypeError, N_BAF10.n, 'test')

    def testN_BAF10ValueErrors(self):
        self.assertRaises(ValueError, N_BAF10.n, 100)
        self.assertRaises(ValueError, N_BAF10.n, 0)
        self.assertRaises(ValueError, N_BAF10.n, -100)

    def testN_BAF10(self):
        self.assertEqual(1.5469302146171202, N_BAF10.n(5))


class TestE_BAF11(unittest.TestCase):
    def testE_BAF11TypeErrors(self):
        self.assertRaises(TypeError, E_BAF11.n, None)
        self.assertRaises(TypeError, E_BAF11.n, 'test')

    def testE_BAF11ValueErrors(self):
        self.assertRaises(ValueError, E_BAF11.n, 100)
        self.assertRaises(ValueError, E_BAF11.n, 0)
        self.assertRaises(ValueError, E_BAF11.n, -100)

    def testE_BAF11(self):
        self.assertEqual(1.5713583894047798, E_BAF11.n(5))


class TestN_BAK1(unittest.TestCase):
    def testN_BAK1TypeErrors(self):
        self.assertRaises(TypeError, N_BAK1.n, None)
        self.assertRaises(TypeError, N_BAK1.n, 'test')

    def testN_BAK1ValueErrors(self):
        self.assertRaises(ValueError, N_BAK1.n, 100)
        self.assertRaises(ValueError, N_BAK1.n, 0)
        self.assertRaises(ValueError, N_BAK1.n, -100)

    def testN_BAK1(self):
        self.assertEqual(1.4716376125966693, N_BAK1.n(5))


class TestN_BAK4(unittest.TestCase):
    def testN_BAK4TypeErrors(self):
        self.assertRaises(TypeError, N_BAK4.n, None)
        self.assertRaises(TypeError, N_BAK4.n, 'test')

    def testN_BAK4ValueErrors(self):
        self.assertRaises(ValueError, N_BAK4.n, 100)
        self.assertRaises(ValueError, N_BAK4.n, 0)
        self.assertRaises(ValueError, N_BAK4.n, -100)

    def testN_BAK4(self):
        self.assertEqual(1.459391121152617, N_BAK4.n(5))


class TestFK51A(unittest.TestCase):
    def testFK51ATypeErrors(self):
        self.assertRaises(TypeError, FK51A.n, None)
        self.assertRaises(TypeError, FK51A.n, 'test')

    def testFK51AValueErrors(self):
        self.assertRaises(ValueError, FK51A.n, 100)
        self.assertRaises(ValueError, FK51A.n, 0)
        self.assertRaises(ValueError, FK51A.n, -100)

    def testFK51A(self):
        self.assertEqual(1.4251526811342752, FK51A.n(5))


class TestLAFN7(unittest.TestCase):
    def testLAFN7TypeErrors(self):
        self.assertRaises(TypeError, LAFN7.n, None)
        self.assertRaises(TypeError, LAFN7.n, 'test')

    def testLAFN7ValueErrors(self):
        self.assertRaises(ValueError, LAFN7.n, 100)
        self.assertRaises(ValueError, LAFN7.n, 0)
        self.assertRaises(ValueError, LAFN7.n, -100)

    def testLAFN7(self):
        self.assertEqual(1.5810761652641074, LAFN7.n(5))


class TestN_LASF9(unittest.TestCase):
    def testN_LASF9TypeErrors(self):
        self.assertRaises(TypeError, N_LASF9.n, None)
        self.assertRaises(TypeError, N_LASF9.n, 'test')

    def testN_LASF9ValueErrors(self):
        self.assertRaises(ValueError, N_LASF9.n, 100)
        self.assertRaises(ValueError, N_LASF9.n, 0)
        self.assertRaises(ValueError, N_LASF9.n, -100)

    def testN_LASF9(self):
        self.assertEqual(1.7197092324835102, N_LASF9.n(5))


class TestN_LAK22(unittest.TestCase):
    def testN_LAK22TypeErrors(self):
        self.assertRaises(TypeError, N_LAK22.n, None)
        self.assertRaises(TypeError, N_LAK22.n, 'test')

    def testN_LAK22ValueErrors(self):
        self.assertRaises(ValueError, N_LAK22.n, 100)
        self.assertRaises(ValueError, N_LAK22.n, 0)
        self.assertRaises(ValueError, N_LAK22.n, -100)

    def testN_LAK22(self):
        self.assertEqual(1.528065402814606, N_LAK22.n(5))


class TestN_SSK5(unittest.TestCase):
    def testN_SSK5TypeErrors(self):
        self.assertRaises(TypeError, N_SSK5.n, None)
        self.assertRaises(TypeError, N_SSK5.n, 'test')

    def testN_SSK5ValueErrors(self):
        self.assertRaises(ValueError, N_SSK5.n, 100)
        self.assertRaises(ValueError, N_SSK5.n, 0)
        self.assertRaises(ValueError, N_SSK5.n, -100)

    def testN_SSK5(self):
        self.assertEqual(1.541289278092723, N_SSK5.n(5))


class TestE_FD10(unittest.TestCase):
    def testE_FD10TypeErrors(self):
        self.assertRaises(TypeError, E_FD10.n, None)
        self.assertRaises(TypeError, E_FD10.n, 'test')

    def testE_FD10ValueErrors(self):
        self.assertRaises(ValueError, E_FD10.n, 100)
        self.assertRaises(ValueError, E_FD10.n, 0)
        self.assertRaises(ValueError, E_FD10.n, -100)

    def testE_FD10(self):
        self.assertEqual(1.5975207997018837, E_FD10.n(5))


class TestFusedSilica(unittest.TestCase):
    def testFusedSilicaTypeErrors(self):
        self.assertRaises(TypeError, FusedSilica.n, None)
        self.assertRaises(TypeError, FusedSilica.n, 'test')

    def testFusedSilicaValueErrors(self):
        self.assertRaises(ValueError, FusedSilica.n, 100)
        self.assertRaises(ValueError, FusedSilica.n, 0)
        self.assertRaises(ValueError, FusedSilica.n, -100)

    def testFusedSilica(self):
        self.assertEqual(1.3404572894914368, FusedSilica.n(5))


if __name__ == '__main__':
    unittest.main()



