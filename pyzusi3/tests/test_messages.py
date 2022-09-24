import unittest

from pyzusi3 import messages

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
