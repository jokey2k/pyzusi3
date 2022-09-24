from operator import attrgetter
import unittest

from pyzusi3 import messages


class TestOperators(unittest.TestCase):
    def test_parameter_operators(self):
        param1 = messages.ParameterId(id1=2, id2=266, id3=None, id4=None, id5=None, id6=None)
        param2 = messages.ParameterId(id1=2, id2=266, id3=1, id4=None, id5=None, id6=None)
        self.assertTrue(param1 < param2)
        self.assertTrue(param2 > param1)
        param1 = messages.ParameterId(id1=2, id2=266, id3=1, id4=1, id5=None, id6=None),
        param2 = messages.ParameterId(id1=2, id2=266, id3=2, id4=None, id5=None, id6=None),
        self.assertTrue(param1 < param2)
        self.assertTrue(param2 > param1)
        param1 = messages.ParameterId(id1=2, id2=266, id3=1, id4=None, id5=None, id6=None)
        param2 = messages.ParameterId(id1=2, id2=266, id3=1, id4=1, id5=None, id6=None)
        self.assertTrue(param1 < param2)
        self.assertTrue(param2 > param1)
        param1 = messages.ParameterId(id1=2, id2=266, id3=2, id4=2, id5=4, id6=1)
        param2 = messages.ParameterId(id1=2, id2=266, id3=12, id4=2, id5=None, id6=None)
        self.assertTrue(param1 < param2)
        self.assertTrue(param2 > param1)

    def test_parameter_lt_sort(self):
        unsorted = (
            messages.ParameterId(id1=2, id2=266, id3=1, id4=1, id5=None, id6=None),
            messages.ParameterId(id1=2, id2=266, id3=2, id4=None, id5=None, id6=None),
            messages.ParameterId(id1=2, id2=266, id3=None, id4=None, id5=None, id6=None),
            messages.ParameterId(id1=2, id2=266, id3=1, id4=None, id5=None, id6=None),
        )
        real_sorted = (
            messages.ParameterId(id1=2, id2=266, id3=None, id4=None, id5=None, id6=None),
            messages.ParameterId(id1=2, id2=266, id3=1, id4=None, id5=None, id6=None),
            messages.ParameterId(id1=2, id2=266, id3=1, id4=1, id5=None, id6=None),
            messages.ParameterId(id1=2, id2=266, id3=2, id4=None, id5=None, id6=None),
        )
        sorting_test = tuple(sorted(unsorted))
        self.assertEqual(sorting_test, real_sorted)


class TestInstantiation(unittest.TestCase):
    def test_all_messages(self):
        """Ensure all messages can be instantiated without parameters"""

        messages.ParameterId()
        with self.assertRaises(TypeError):
            # needs 3 parameters at least
            messages.LowlevelParameter()
        messages.HELLO()
        messages.ACK_HELLO()
        messages.NEEDED_DATA()
        messages.ACK_NEEDED_DATA()
        messages.DATA_FTD()
        messages.STATUS_NOTBREMSSYSTEM()
        messages.STATUS_SIFA()
        messages.STATUS_ZUGBEEINFLUSSUNG_GRUND()
        messages.STATUS_INDUSI_EINSTELLUNGEN()
        messages.STATUS_INDUSI_BETRIEBSDATEN()
        messages.STATUS_ETCS_EINSTELLUNGEN()
        messages.STATUS_ETCS_BETRIEBSDATEN()
        messages.STATUS_ZUB_EINSTELLUNGEN()
        messages.STATUS_ZUB_BETRIEBSDATEN()
        messages.STATUS_ZBS_EINSTELLUNGEN()
        messages.STATUS_ZBS_BETRIEBSDATEN()
        messages.STATUS_FAHRSPERRE_EINSTELLUNGEN()
        messages.STATUS_FAHRSPERRE_BETRIEBSDATEN()
        messages.STATUS_TUEREN()
        messages.STATUS_FAHRZEUG()
        messages.STATUS_ZUGVERBAND()
        messages.STATUS_WEICHEN()
        messages.STATUS_WEICHEN_WEICHE()
        messages.STATUS_LM_ZUSIDISPLAY()
        messages.STATUS_LM_ZUSIDISPLAY_DISPLAY()
        messages.STATUS_ZUGFAHRDATEN()
        messages.STATUS_ZUGFAHRDATEN_FAHRZEUG()
        messages.DATA_OPERATION()
        messages.DATA_OPERATION_BETAETIGUNG()
        messages.DATA_OPERATION_KOMBISCHALTER()
        messages.DATA_OPERATION_SCHALTERFUNKTION()
        messages.DATA_OPERATION_MAUSKLICK()
        messages.DATA_PROG()
        messages.INPUT()
        messages.CONTROL()
