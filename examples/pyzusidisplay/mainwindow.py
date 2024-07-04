import asyncio
from enum import Enum
import logging
import math
import time
import threading

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer, Slot
from pyzusi3.client import ZusiClient
from pyzusi3 import messages as zusimsg

from form_ui import Ui_MainWindow


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

        self.timer_led_update = QTimer()
        self.timer_led_update.timeout.connect(self.update_leds)

        self.timer_ui_update = QTimer()
        self.timer_ui_update.timeout.connect(self.update_ui)

        self.timer_autosifa = QTimer()
        self.timer_autosifa.timeout.connect(self.autosifa_run)
        self.autosifa_state = AutoSifaState.INACTIVE

        self.timer_tueren_links_delayed = QTimer()
        self.timer_tueren_links_delayed.setSingleShot(True)
        self.timer_tueren_links_delayed.timeout.connect(self.tueren_links_delayed)

        self.timer_tueren_rechts_delayed = QTimer()
        self.timer_tueren_rechts_delayed.setSingleShot(True)
        self.timer_tueren_rechts_delayed.timeout.connect(self.tueren_rechts_delayed)

        self.last_z_value = 0.0
        self.z_inc = 0

    def reset_led(self):
        self.previous_led_state = {
            'u': None,
            'm': None,
            'o': None,
            '40': None,
            '500': None,
            '1000': None,
            'sifa': None
        }
        self.update_leds()

    def get_leds_state(self):
        if self.zusiClient is None:
            return {
                'u': zusimsg.LMZUSTAND_MIT_INVERS.AUS,
                'm': zusimsg.LMZUSTAND_MIT_INVERS.AUS,
                'o': zusimsg.LMZUSTAND_MIT_INVERS.AUS,
                '40': zusimsg.LMZUSTAND_MIT_INVERS.AUS,
                '500': zusimsg.LMZUSTAND_MIT_INVERS.AUS,
                '1000': zusimsg.LMZUSTAND_MIT_INVERS.AUS,
                'sifa': zusimsg.LMZUSTAND_MIT_INVERS.AUS
            }

        if zusimsg.STATUS_INDUSI_BETRIEBSDATEN not in self.zusiClient.local_state:
            return self.previous_led_state

        indusi_state = self.zusiClient.local_state[zusimsg.STATUS_INDUSI_BETRIEBSDATEN]

        led_state = {
            'u': indusi_state.lm_u,
            'm': indusi_state.lm_m,
            'o': indusi_state.lm_o,
            '40': indusi_state.lm_befehl,
            '500': indusi_state.lm_500hz,
            '1000': indusi_state.lm_1000hz
        }

        if zusimsg.STATUS_SIFA not in self.zusiClient.local_state:
            sifa_state = zusimsg.LMZUSTAND.AUS
        else:
            sifa_state = self.zusiClient.local_state[zusimsg.STATUS_SIFA].lm
        led_state['sifa'] = sifa_state

        return led_state

    def update_leds(self):
        if not self.led_init:
            if self.zusiClient is None:
                return
        else:
            self.led_init = False

        current_time = time.time()
        # create 500ms blink
        blink_on = (current_time - int(current_time) >= 0.5)
        new_state = self.get_leds_state()
        current_state = self.previous_led_state
        led_off_states = [
            None,
            zusimsg.LMZUSTAND.AUS,
            zusimsg.LMZUSTAND_MIT_INVERS.AUS,
        ]
        if blink_on:
            led_off_states.append(zusimsg.LMZUSTAND_MIT_INVERS.BLINKEND_INVERS)
        else:
            led_off_states.append(zusimsg.LMZUSTAND.BLINKEN)
            led_off_states.append(zusimsg.LMZUSTAND_MIT_INVERS.BLINKEND)

        self.setUpdatesEnabled(False)

        for statevar, uielement, on_color, off_color in [
            ('u', self.ui.lm_u, 'dodgerblue', 'mediumblue'),
            ('m', self.ui.lm_m, 'dodgerblue', 'mediumblue'),
            ('o', self.ui.lm_o, 'dodgerblue', 'mediumblue'),
            ('40', self.ui.lm_40, 'white', 'gray'),
            ('500', self.ui.lm_500, 'orangered', 'maroon'),
            ('1000', self.ui.lm_1000, 'gold', 'rgb(136, 73, 16)'),
            ('sifa', self.ui.lm_sifa, 'white', 'gray')
        ]:
            if current_state[statevar] != new_state[statevar] or \
                new_state[statevar] in [zusimsg.LMZUSTAND.BLINKEN, zusimsg.LMZUSTAND_MIT_INVERS.BLINKEND_INVERS]:

                lamp_state = new_state[statevar]
                if lamp_state in led_off_states:
                    uielement.setStyleSheet("color: black; background-color: %s;" % off_color)
                else:
                    uielement.setStyleSheet("color: black; background-color: %s;" % on_color)

        self.setUpdatesEnabled(True)

    def update_ui(self):
        if self.zusiClient is None:
            return

        self.setUpdatesEnabled(False)
        self.update_text()

        if self.zusiClient.connected:
            self.ui.connectButton.setText("Disconnect")
        else:
            self.ui.connectButton.setText("Connect")

        self.setUpdatesEnabled(True)

    def update_text(self):
        if zusimsg.DATA_PROG in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.DATA_PROG]
    
            self.ui.fahrplan.setText(str(state.zugdateiname))
            self.ui.zugnummer.setText(str(state.zugnummer))
            self.ui.ladezustand.setText(str(state.ladepause))
        
        if zusimsg.DATA_FTD in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.DATA_FTD]

            if state.uhrzeit_stunde is not None and state.uhrzeit_minute is not None:
                stunde = int(state.uhrzeit_stunde)
                minute = state.uhrzeit_minute
                sekunde = int((minute - int(minute))*0.6*100)
                minute = int(minute)
                self.ui.uhrzeit.setText("%s:%s:%s" % (str(stunde).zfill(2), str(minute).zfill(2), str(sekunde).zfill(2)))

            if state.geschwindigkeit:
                self.ui.geschwindigkeit.setText(str(int(round(state.geschwindigkeit*3.6))))
            if self.ui.sollgeschwindigkeit_check.isChecked() and state.streckenvmax:
                self.ui.sollgeschwindigkeit.setText(str(int(state.streckenvmax*3.6)))
            else:
                self.ui.sollgeschwindigkeit.clear()

            if state.z_koordinate:
                if self.z_inc == 0 or self.z_inc > 3:
                    self.z_inc = 0
                    previous_z = self.last_z_value
                    new_z = state.z_koordinate
                    diff = new_z - previous_z
                    self.last_z_value = new_z
                    self.ui.steigung.setText(str(round(diff, 2)))
                self.z_inc += 1

        if zusimsg.STATUS_ZUGFAHRDATEN in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_ZUGFAHRDATEN]

            if state.fahrzeuge:
                fahrzeug = state.fahrzeuge[0]
                self.ui.druckhll.setText(str(round(fahrzeug.hll_druck, 1)))
                self.ui.bremsdruck.setText(str(round(fahrzeug.bremszylinderdruck, 1)))
                self.ui.bremsdruckanzeige.setValue(int(fahrzeug.hll_druck*10))
                if fahrzeug.hll_druck > 6.0:
                    self.ui.bremsdruckanzeige.setStyleSheet('background-color: red;')
                else:
                    self.ui.bremsdruckanzeige.setStyleSheet('')

        if zusimsg.STATUS_ZUGBEEINFLUSSUNG_GRUND in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_ZUGBEEINFLUSSUNG_GRUND]

            self.ui.indusibauart.setText(state.bauart)

        if zusimsg.STATUS_INDUSI_EINSTELLUNGEN in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_INDUSI_EINSTELLUNGEN]

        if zusimsg.STATUS_INDUSI_BETRIEBSDATEN in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_INDUSI_BETRIEBSDATEN]

            self.ui.indusistatus.setText(str(state.zustand.name if state.zustand is not None else ''))
            self.ui.indusizwangsbremsung.setText(str(state.zwangsbremsung.name if state.zwangsbremsung is not None else ''))
            self.ui.indusizusatzinfo.setText(str(state.zusatzinfo_melderbild.name if state.zusatzinfo_melderbild is not None else ''))

        if zusimsg.STATUS_SIFA in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_SIFA]

            self.ui.sifabauart.setText(state.bauart)
            status = "NORMAL"
            if state.lm == zusimsg.LMZUSTAND.AN:
                status = "LAMPE AN"
            if state.hupe is not None and state.hupe != zusimsg.STATUS_SIFA_HUPE.HUPE_AUS:
                status = state.hupe.name
            self.ui.sifastatus.setText(status)

        if zusimsg.STATUS_NOTBREMSSYSTEM in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_NOTBREMSSYSTEM]

            self.ui.nbuebauart.setText(state.bauart)
            self.ui.nbuestatus.setText(str(state.status.name if state.status is not None else ''))

        if zusimsg.STATUS_TUEREN in self.zusiClient.local_state:
            state = self.zusiClient.local_state[zusimsg.STATUS_TUEREN]

            self.ui.tuerenlinks.setText(str(state.links.name if state.links is not None else ''))
            if state.links == zusimsg.TUEREN_SEITE.SCHLIESSEND:
                self.ui.tuerenlinks.setStyleSheet('background-color: yellow;')
            elif state.links in [zusimsg.TUEREN_SEITE.OEFFNEND, zusimsg.TUEREN_SEITE.OFFEN]:
                self.ui.tuerenlinks.setStyleSheet('background-color: green;')
            else:
                self.ui.tuerenlinks.setStyleSheet('')
            self.ui.tuerenrechts.setText(str(state.rechts.name if state.rechts is not None else ''))
            if state.rechts == zusimsg.TUEREN_SEITE.SCHLIESSEND:
                self.ui.tuerenrechts.setStyleSheet('background-color: yellow;')
            elif state.rechts in [zusimsg.TUEREN_SEITE.OEFFNEND, zusimsg.TUEREN_SEITE.OFFEN]:
                self.ui.tuerenrechts.setStyleSheet('background-color: green;')
            else:
                self.ui.tuerenrechts.setStyleSheet('')
            self.ui.tuerwahlschalter.setText(str(state.seitenwahl.name if state.seitenwahl is not None else ''))

        self.ui.autosifastatus.setText(str(self.autosifa_state.name))

    def reset_textfields(self):
        self.ui.geschwindigkeit.clear()
        self.ui.druckhll.clear()
        self.ui.indusistatus.clear()
        self.ui.sifastatus.clear()
        self.ui.uhrzeit.clear()
        self.ui.nbuestatus.clear()
        self.ui.sifabauart.clear()
        self.ui.indusibauart.clear()
        self.ui.nbuebauart.clear()
        self.ui.indusizwangsbremsung.clear()
        self.ui.indusizusatzinfo.clear()
        self.ui.sollgeschwindigkeit.clear()
        self.ui.tuerenlinks.clear()
        self.ui.tuerenrechts.clear()
        self.ui.tuerwahlschalter.clear()
        self.ui.zugnummer.clear()
        self.ui.fahrplan.clear()
        self.ui.ladezustand.clear()
        self.ui.autosifastatus.clear()
        self.ui.steigung.clear()

    @Slot()
    def on_tueren_links_clicked(self):
        if self.zusiClient is None:
            return

        if self.timer_tueren_rechts_delayed.isActive() or self.timer_tueren_links_delayed.isActive():
            return

        msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.TUEREN, zusimsg.INPUT_TASTATURKOMMANDO.TuerenLi_Down,
                            zusimsg.INPUT_TASTATURAKTION.Default, tastatur_schalterposition=0)
        self.zusiClient.send_input(msg)
        self.timer_tueren_links_delayed.start(100)

    def tueren_links_delayed(self):
        msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.TUEREN, zusimsg.INPUT_TASTATURKOMMANDO.TuerenLi_Up,
                            zusimsg.INPUT_TASTATURAKTION.Default, tastatur_schalterposition=0)
        self.zusiClient.send_input(msg)

    @Slot()
    def on_tueren_rechts_clicked(self):
        if self.zusiClient is None:
            return

        if self.timer_tueren_rechts_delayed.isActive() or self.timer_tueren_links_delayed.isActive():
            return

        msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.TUEREN, zusimsg.INPUT_TASTATURKOMMANDO.TuerenRe_Down,
                            zusimsg.INPUT_TASTATURAKTION.Default, tastatur_schalterposition=0)
        self.zusiClient.send_input(msg)
        self.timer_tueren_rechts_delayed.start(100)

    def tueren_rechts_delayed(self):
        msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.TUEREN, zusimsg.INPUT_TASTATURKOMMANDO.TuerenRe_Up,
                            zusimsg.INPUT_TASTATURAKTION.Default, tastatur_schalterposition=0)
        self.zusiClient.send_input(msg)

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
            msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.SIFA, zusimsg.INPUT_TASTATURKOMMANDO.Unbestimmt, zusimsg.INPUT_TASTATURAKTION.Down, tastatur_schalterposition=0)
            self.zusiClient.send_input(msg)
            self.autosifa_state = AutoSifaState.SEND_PEDAL_UP
        elif self.autosifa_state == AutoSifaState.SEND_PEDAL_UP:
            msg = zusimsg.INPUT(zusimsg.INPUT_TASTATURZUORDNUNG.SIFA, zusimsg.INPUT_TASTATURKOMMANDO.Unbestimmt, zusimsg.INPUT_TASTATURAKTION.Up, tastatur_schalterposition=0)
            self.zusiClient.send_input(msg)
            self.autosifa_state = AutoSifaState.WAITING_FOR_REQUEST

    @Slot()
    def on_connectButton_clicked(self):
        if self.zusiClient is None:
            self.timer_led_update.start(250)
            self.timer_ui_update.start(250)
            self.timer_autosifa.start(500)
            self.zusiThread = threading.Thread(target=lambda: self.run_zusi_loop(), daemon=True)
            self.zusiThread.start()
        else:
            if not self.zusiClient.connected:
                self.zusiThread = threading.Thread(target=lambda: self.run_zusi_loop(), daemon=True)
                self.zusiThread.start()
            else:
                self.zusiClient.disconnect()

    def run_zusi_loop(self):
        asyncio.set_event_loop(self.zusiLoop)
        self.zusiLoop.call_soon(lambda: self.connect_zusi())
        self.zusiLoop.run_forever()

    def connect_zusi(self):
        self.zusiClient = ZusiClient(self.ui.zusi_ip.text(), 1436, "ZusiData Display", "1.0")
        self.zusiClient.request_status(
            displays=[
                zusimsg.FAHRPULT_ANZEIGEN.GESCHWINDIGKEIT,
                zusimsg.FAHRPULT_ANZEIGEN.UHRZEIT_STUNDE,
                zusimsg.FAHRPULT_ANZEIGEN.UHRZEIT_MINUTE,
                zusimsg.FAHRPULT_ANZEIGEN.STRECKENVMAX,
                zusimsg.FAHRPULT_ANZEIGEN.Z_KOORDINATE,
                zusimsg.FAHRPULT_ANZEIGEN.STATUS_ZUGFAHRDATEN,
                zusimsg.FAHRPULT_ANZEIGEN.STATUS_NOTBREMSSYSTEM,
                zusimsg.FAHRPULT_ANZEIGEN.STATUS_TUEREN,
                zusimsg.FAHRPULT_ANZEIGEN.STATUS_SIFA,
                zusimsg.FAHRPULT_ANZEIGEN.STATUS_ZUGBEEINFLUSSUNG
            ],
            control=True,
            programdata=[
                zusimsg.PROGRAMMDATEN.ZUGDATEI,
                zusimsg.PROGRAMMDATEN.ZUGNUMMER,
                zusimsg.PROGRAMMDATEN.LADEPAUSE,
            ]
        )
        loop = asyncio.get_event_loop()
        loop.create_task(self.zusiClient.connect())
