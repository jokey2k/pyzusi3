import asyncio
from enum import Enum
import threading

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer, Slot, QSettings
from pyzusi3.client import ZusiClient
from pyzusi3 import messages as zusimsg

from form_ui import Ui_MainWindow
import form_rc

__version__ = "1.0.0"


class AutoSifaState(Enum):
    INACTIVE = 0
    WAITING_FOR_REQUEST = 1
    SEND_PEDAL_DOWN = 2
    SEND_PEDAL_UP = 3


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.zusiClient = None
        self.zusiTask = None
        self.zusiLoop = asyncio.new_event_loop()
        self.zusiThread = None

        self.led_init = True
        self.reset_led()
        self.reset_textfields()

        self.timer_ui_update = QTimer()
        self.timer_ui_update.timeout.connect(self.update_ui)

        self.timer_autosifa = QTimer()
        self.timer_autosifa.timeout.connect(self.autosifa_run)
        self.autosifa_state = AutoSifaState.INACTIVE

        self.settings = QSettings()
        ip = self.settings.value("ip")
        if ip is not None:
            self.ui.zusi_ip.setText(ip)

    def reset_led(self):
        self.previous_led_state = {
            'sifa': None
        }
        self.update_leds()

    def get_leds_state(self):
        if self.zusiClient is None:
            return {
                'sifa': zusimsg.LMZUSTAND_MIT_INVERS.AUS
            }

        if zusimsg.STATUS_SIFA not in self.zusiClient.local_state:
            sifa_state = zusimsg.LMZUSTAND.AUS
        else:
            sifa_state = self.zusiClient.local_state[zusimsg.STATUS_SIFA].lm

        return {
            'sifa': sifa_state
        }

    def update_ui(self):
        self.setUpdatesEnabled(False)
        self.update_leds()
        self.update_text()
        self.setUpdatesEnabled(True)

    def update_leds(self):
        if not self.led_init:
            if self.zusiClient is None:
                return
        else:
            self.led_init = False

        if self.zusiClient is not None and self.zusiClient.connected:
            self.ui.connectButton.setStyleSheet("color: white; background-color: green;")
            self.ui.connectButton.setEnabled(False)
        else:
            self.ui.connectButton.setStyleSheet("color: black; background-color: lightgray;")
            self.ui.connectButton.setEnabled(True)

        # create 500ms blink
        new_state = self.get_leds_state()
        current_state = self.previous_led_state
        led_off_states = [
            None,
            zusimsg.LMZUSTAND.AUS,
            zusimsg.LMZUSTAND_MIT_INVERS.AUS,
        ]

        for statevar, uielement, on_color, off_color in [
            ('sifa', self.ui.lm_sifa, 'white', 'gray')
        ]:
            if current_state[statevar] != new_state[statevar]:
                lamp_state = new_state[statevar]
                if lamp_state in led_off_states:
                    uielement.setStyleSheet("color: black; background-color: %s;" % off_color)
                else:
                    uielement.setStyleSheet("color: black; background-color: %s;" % on_color)

    def update_text(self):
        if self.zusiClient is None:
            return

        if zusimsg.STATUS_SIFA in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_SIFA]

            self.ui.sifabauart.setText(state.bauart)
            status = "NORMAL"
            if state.lm == zusimsg.LMZUSTAND.AN:
                status = "LAMPE AN"
            if state.hupe is not None and state.hupe != zusimsg.STATUS_SIFA_HUPE.HUPE_AUS:
                status = state.hupe.name
            self.ui.sifastatus.setText(status)

        self.ui.autosifastatus.setText(str(self.autosifa_state))

    def autosifa_run(self):
        if self.zusiClient is None:
            self.autosifa_state = AutoSifaState.INACTIVE
            return

        if self.autosifa_state == AutoSifaState.INACTIVE and not self.ui.autosifa_check.isChecked():
            return

        if zusimsg.STATUS_SIFA not in self.zusiClient.local_state:
            self.autosifa_state = AutoSifaState.INACTIVE
            return

        state = self.zusiClient.local_state[zusimsg.STATUS_SIFA]

        if self.autosifa_state == AutoSifaState.INACTIVE:
            if self.ui.autosifa_check.isChecked():
                self.autosifa_state = AutoSifaState.WAITING_FOR_REQUEST
        elif self.autosifa_state == AutoSifaState.WAITING_FOR_REQUEST:
            if state.lm == zusimsg.LMZUSTAND.AN or \
                state.hupe == zusimsg.STATUS_SIFA_HUPE.HUPE_WARNUNG or \
                state.hupe == zusimsg.STATUS_SIFA_HUPE.HUPE_ZWANGSBREMSUNG:
                self.autosifa_state = AutoSifaState.SEND_PEDAL_DOWN
            elif not self.ui.autosifa_check.isChecked():
                self.autosifa_state = AutoSifaState.INACTIVE
        elif self.autosifa_state == AutoSifaState.SEND_PEDAL_DOWN:
            if not self.ui.autosifa_invers.isChecked():
                msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.SIFA, zusimsg.INPUT_TASTATURKOMMANDO.Unbestimmt,
                                    zusimsg.INPUT_TASTATURAKTION.Down, tastatur_schalterposition=0)
            else:
                msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.SIFA, zusimsg.INPUT_TASTATURKOMMANDO.Unbestimmt,
                                    zusimsg.INPUT_TASTATURAKTION.Up, tastatur_schalterposition=0)
            self.zusiClient.send_input(msg)
            self.autosifa_state = AutoSifaState.SEND_PEDAL_UP
        elif self.autosifa_state == AutoSifaState.SEND_PEDAL_UP:
            if not self.ui.autosifa_invers.isChecked():
                msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.SIFA, zusimsg.INPUT_TASTATURKOMMANDO.Unbestimmt,
                                    zusimsg.INPUT_TASTATURAKTION.Up, tastatur_schalterposition=0)
            else:
                msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.SIFA, zusimsg.INPUT_TASTATURKOMMANDO.Unbestimmt,
                                    zusimsg.INPUT_TASTATURAKTION.Down, tastatur_schalterposition=0)
            self.zusiClient.send_input(msg)
            self.autosifa_state = AutoSifaState.WAITING_FOR_REQUEST

    def reset_textfields(self):
        self.ui.sifastatus.clear()
        self.ui.sifabauart.clear()
        self.ui.autosifastatus.clear()
        self.setWindowTitle("AutoSifa " + __version__)

    @Slot()
    def on_connectButton_clicked(self):
        self.ui.connectButton.setEnabled(False)
        self.timer_ui_update.start(250)
        self.timer_autosifa.start(250)
        self.zusiThread = threading.Thread(target=lambda: self.run_zusi_loop(), daemon=True)
        self.zusiThread.start()

    @Slot(str)
    def on_zusi_ip_textChanged(self, text):
        self.settings.setValue("ip", text)

    def run_zusi_loop(self):
        asyncio.set_event_loop(self.zusiLoop)
        self.zusiLoop.call_soon(lambda: self.connect_zusi())
        self.zusiLoop.run_forever()

    def connect_zusi(self):
        self.zusiClient = ZusiClient(self.ui.zusi_ip.text(), 1436, "AutoSifa", __version__)
        self.zusiClient.request_status(
            displays=[
                zusimsg.FAHRPULT_ANZEIGEN.STATUS_SIFA
            ],
            control=True,
        )
        loop = asyncio.get_event_loop()
        loop.create_task(self.zusiClient.connect())
