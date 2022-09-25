from collections import namedtuple
from enum import Enum, auto

from pyzusi3.nodes import ContentType, BasicNode

class AutoNumber(Enum):
    """Used to auto-number elements from 0"""
    def __new__(cls):
        value = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

ParameterId = namedtuple("ParameterId", ['id1', 'id2', 'id3', 'id4', 'id5', 'id6'], defaults=[None] * 6)
def param_lt(self, other):
    prev_eq = False
    for paramname in ('id1', 'id2', 'id3', 'id4', 'id5', 'id6'):
        left = getattr(self, paramname) or 0
        right = getattr(other, paramname) or 0
        if left < right:
            return prev_eq

        prev_eq = left == right

    return False
def param_gt(self, other):
    prev_eq = False
    for paramname in ('id1', 'id2', 'id3', 'id4', 'id5', 'id6'):
        left = getattr(self, paramname) or 0
        right = getattr(other, paramname) or 0
        if left > right:
            return prev_eq

        prev_eq = left == right

    return False
ParameterId.__lt__ = param_lt
ParameterId.__gt__ = param_gt

LowlevelParameter = namedtuple("LowlevelParameter", ['parameterid', 'parametername', 'contenttype', 'enumtype', 'multipletimes', 'nodeasbool'], defaults=[None, None, False])
lowlevel_parameters = {}
message_index = {}

# Tipphilfen
LLP = LowlevelParameter
PID = ParameterId
llps = lowlevel_parameters
msgidx = message_index

#
# allgemeine Helfer
#

# Lampenstatus
class LMZUSTAND(Enum):
    AUS = 0
    AN = 1
    BLINKEN = 2
class LMZUSTAND_MIT_INVERS(Enum):
    AUS = 0
    AN = 1
    BLINKEND = 2
    BLINKEND_INVERS = 3
# Steuerschalter / Lufthahn
class SCHALTER(Enum):
    UNBEKANNT = 0
    AUS = 1
    EIN = 2

#
# HELLO
# Client -> Zusi
#
class ClientTyp(Enum):
    ZUSI = 1
    FAHRPULT = 2
HELLO = namedtuple("HELLO", ['protokollversion', 'clienttyp', 'clientname', 'clientversion'], defaults=[None] * 4)
llps[HELLO] = (
    LLP(PID(1), None, BasicNode),
    LLP(PID(1, 1), None, BasicNode),
    LLP(PID(1, 1, 1), 'protokollversion', ContentType.WORD),
    LLP(PID(1, 1, 2), 'clienttyp', ContentType.WORD, ClientTyp),
    LLP(PID(1, 1, 3), 'clientname', ContentType.STRING),
    LLP(PID(1, 1, 4), 'clientversion', ContentType.STRING),
)
msgidx[PID(1, 1)] = HELLO

#
# ACK_HELLO
# Zusi -> Client
#
ACK_HELLO = namedtuple("ACK_HELLO", ['zusiversion', 'verbindungsinfo', 'status', 'startdatum', 'protokollversion'], defaults=[None] * 5)
llps[ACK_HELLO] = (
    LLP(PID(1), None, BasicNode),
    LLP(PID(1, 2), None, BasicNode),
    LLP(PID(1, 2, 1), 'zusiversion', ContentType.STRING),
    LLP(PID(1, 2, 2), 'verbindungsinfo', ContentType.STRING),
    LLP(PID(1, 2, 3), 'status', ContentType.BYTE),
    LLP(PID(1, 2, 4), 'startdatum', ContentType.DOUBLE),
    LLP(PID(1, 2, 5), 'protokollversion', ContentType.STRING),
)
msgidx[PID(1, 2)] = ACK_HELLO

#
# NEEDED_DATA
# Client -> Zusi
#
class FAHRPULT_ANZEIGEN(Enum):
    KEINE_FUNKTION = 0
    GESCHWINDIGKEIT = 1
    DRUCK_HAUPTLUFTLEITUNG = 2
    DRUCK_BREMSZYLINDER = 3
    DRUCK_HAUPTLUFTBEHAELTER = 4
    LUFTPRESSER_LAEUFT = 5
    LUFTSTROM_FBV = 6
    LUFTSTROM_ZBV = 7
    LUEFTER_AN = 8
    ZUGKRAFT_GESAMT = 9
    ZUGKRAFT_PRO_ACHSE = 10
    ZUGKRAFT_SOLL_GESAMT = 11
    ZUGKRAFT_SOLL_PRO_ACHSE = 12
    OBERSTROM = 13
    FAHRLEITUNGSSPANNUNG = 14
    MOTORDREHZAHL = 15
    UHRZEIT_STUNDE = 16
    UHRZEIT_MINUTE = 17
    UHRZEIT_SEKUNDE = 18
    HAUPTSCHALTER = 19
    TRENNSCHUETZ = 20
    FAHRSTUFE = 21
    FENSTER_3D = 22
    AFB_SOLLGESCHWINDIGKEIT = 23
    DRUCK_HILFSBEHAELTER = 24
    ZURUECKGELEGTER_GESAMTWEG = 25
    LM_GETRIEBE = 26
    LM_SCHLEUDERN = 27
    LM_GLEITEN = 28
    LM_MG_BREMSE = 29
    LM_H_BREMSE = 30
    LM_R_BREMSE = 31
    LM_HOCHABBREMSUNG = 32
    LM_SCHNELLBREMSUNG = 33
    STATUS_NOTBREMSSYSTEM = 34
    LM_UHRZEIT = 35
    LM_DREHZAHLVERSTELLUNG = 36
    LM_FAHRTRICHTUNG_VOR = 37
    LM_FAHRTRICHTUNG_ZURUECK = 38
    LM_FAHRTRICHTUNG_M = 39
    # XXX HINTERGRUNDBILD = 40
    MOTORDREHMOMENT = 41
    MOTORLAST_NORMIERT = 42
    TUNNEL = 43
    SCHIENENSTOSS_WEICHE = 44
    STAHLBRUECKE = 45
    STEINBRUECKE = 46
    X_KOORDINATE = 47
    Y_KOORDINATE = 48
    Z_KOORDINATE = 49
    UTM_REFERENZPUNKT_X = 50
    UTM_REFERENZPUNKT_Y = 51
    UTM_ZONE = 52
    UTM_ZONE_2 = 53
    AFB_AN = 54
    FAHRPULTINTERN_01 = 55
    FAHRPULTINTERN_02 = 56
    FAHRPULTINTERN_03 = 57
    FAHRPULTINTERN_04 = 58
    FAHRPULTINTERN_05 = 59
    FAHRPULTINTERN_06 = 60
    FAHRPULTINTERN_07 = 61
    FAHRPULTINTERN_08 = 62
    FAHRPULTINTERN_09 = 63
    FAHRPULTINTERN_10 = 64
    FAHRPULTINTERN_11 = 65
    FAHRPULTINTERN_12 = 66
    FAHRPULTINTERN_13 = 67
    FAHRPULTINTERN_14 = 68
    FAHRPULTINTERN_15 = 69
    FAHRPULTINTERN_16 = 70
    FAHRPULTINTERN_17 = 71
    FAHRPULTINTERN_18 = 72
    FAHRPULTINTERN_19 = 73
    FAHRPULTINTERN_20 = 74
    DATUM = 75
    GLEISKRUEMUNG = 76
    STRECKENVMAX = 77
    ZUGKRAFTVORSCHLAG_AUTOPILOT = 78
    BESCHLEUNIGUNG_X = 79
    BESCHLEUNIGUNG_Y = 80
    BESCHLEUNIGUNG_Z = 81
    DREHBESCHLEUNIGUNG_X = 82
    DREHBESCHLEUNIGUNG_Y = 83
    DREHBESCHLEUNIGUNG_Z = 84
    STROMABNEHMER = 85
    LM_FEDERSPEICHERBREMSE_ANGELEGT = 86
    ZUSTAND_FEDERSPEICHERBREMSE = 87
    STW_LM_GETRIEBE = 88
    STW_LM_SCHLEUDERN = 89
    STW_LM_GLEITEN = 90
    STW_LM_H_BREMSE = 91
    STW_LM_R_BREMSE = 82
    STW_LM_DREHZAHLVERSTELLUNG = 93
    DRUCK_ZEITBEHAELTER = 94
    GESCHWINDIGKEIT_ABSOLUT = 95
    ZUG_IST_ENTGLEIST = 96
    KILOMETRIEUNG = 97
    MOTORSTROM = 98
    MOTORSPANNUNG = 99
    STATUS_SIFA = 100
    STATUS_ZUGBEEINFLUSSUNG = 101
    STATUS_TUEREN = 102
    FAHRPULTINTERN_21 = 103
    FAHRPULTINTERN_22 = 104
    FAHRPULTINTERN_23 = 105
    FAHRPULTINTERN_24 = 106
    FAHRPULTINTERN_25 = 107
    FAHRPULTINTERN_26 = 108
    FAHRPULTINTERN_27 = 109
    FAHRPULTINTERN_28 = 110
    FAHRPULTINTERN_29 = 111
    FAHRPULTINTERN_30 = 112
    FAHRPULTINTERN_31 = 113
    FAHRPULTINTERN_32 = 114
    FAHRPULTINTERN_33 = 115
    FAHRPULTINTERN_34 = 116
    FAHRPULTINTERN_35 = 117
    FAHRPULTINTERN_36 = 118
    FAHRPULTINTERN_37 = 119
    FAHRPULTINTERN_38 = 120
    FAHRPULTINTERN_39 = 121
    FAHRPULTINTERN_40 = 122
    STW_LUEFTER_AN = 123
    STW_ZUGKRAFT_GESAMT = 124
    STW_ZUGKRAFT_PRO_ACHSE = 125
    STW_ZUGKRAFT_SOLL_GESAMT = 126
    STW_ZUGKRAFT_SOLL_PRO_ACHSE = 127
    STW_OBERSTROM = 128
    STW_FAHRLEITUNGSSPANNUNG = 129
    STW_MOTORDREHZAHL_1 = 130
    STW_HAUPTSCHALTER = 131
    STW_TRENNSCHUETZ = 132
    STW_FAHRSTUFE = 133
    STW_MOTORDREHMOMENT_1 = 134
    STW_MOTORLAST_NORMIERT = 135
    STW_STROMABNEHMER = 136
    STW_MOTORSTROM_1 = 137
    STW_MOTORSPANNUNG_1 = 138
    GESCHWINDIGKEIT_ABSOLUT_MIT_SCHLEUDERN = 139
    BATTERIEHAUPTSCHALTER_AUS = 140
    STATUS_FAHRZEUG = 141
    STATUS_ZUGVERBAND = 142
    BREMSPROBEFUNKTION = 143
    ZUG_UND_BREMSKRAFT_NORMIERT = 144
    STW_ZUG_UND_BREMSKRAFT_NORMIERT = 145
    STATUS_WEICHEN = 146
    ZUG_UND_BREMSKRAFT_ABSOLUT_NORMIERT = 147
    STW_ZUG_UND_BREMSKRAFT_ABSOLUT_NORMIERT = 148
    FAHRZEUGINTERN_01 = 149
    FAHRZEUGINTERN_02 = 150
    FAHRZEUGINTERN_03 = 151
    FAHRZEUGINTERN_04 = 152
    FAHRZEUGINTERN_05 = 153
    FAHRZEUGINTERN_06 = 154
    FAHRZEUGINTERN_07 = 155
    FAHRZEUGINTERN_08 = 156
    FAHRZEUGINTERN_09 = 157
    FAHRZEUGINTERN_10 = 158
    FAHRZEUGINTERN_11 = 159
    FAHRZEUGINTERN_12 = 160
    FAHRZEUGINTERN_13 = 161
    FAHRZEUGINTERN_14 = 162
    FAHRZEUGINTERN_15 = 163
    FAHRZEUGINTERN_16 = 164
    FAHRZEUGINTERN_17 = 165
    FAHRZEUGINTERN_18 = 166
    FAHRZEUGINTERN_19 = 167
    FAHRZEUGINTERN_20 = 168
    STATUS_LM_ZUSIPISPLAY = 169
    AUSSENHELLIGKEIT = 170
    STATUS_ZUGFAHRDATEN = 171
    FUEHRERSTAND_DEAKTIVIERT = 172
    SOLLDRUCK_HL = 173
    STW_MOTORDREHZAHL_2 = 174
    STW_MOTORDREHMOMENT_2 = 175
    STW_MOTORSTROM_2 = 176
    STW_MOTORSPANNUNG_2_ = 177
class PROGRAMMDATEN(Enum):
    ZUGDATEI = 1
    ZUGNUMMER = 2
    LADEPAUSE = 3
    BUCHFAHRPLAN_XML = 4
    NEU_UEBERNOMMEN = 5
    BUCHFAHRPLAN_TIFF = 6
    BUCHFAHRPLAN_PDF = 7
    BREMSZETTEL_PDF = 8
    WAGENLISTE_PDF = 9
    LA_PDF = 10
    STRECKENBUCH_PDF = 11
    ERSATZFAHRPLAN_PDF = 12
NEEDED_DATA = namedtuple("NEEDED_DATA", ['anzeigen', 'bedienung', 'programmdaten'], defaults=[None] * 3)
llps[NEEDED_DATA] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 3), None, BasicNode),
    LLP(PID(2, 3, 0x0a), None, BasicNode),
    LLP(PID(2, 3, 0x0a, 1), 'anzeigen', ContentType.WORD, FAHRPULT_ANZEIGEN, multipletimes=True),
    LLP(PID(2, 3, 0x0b), 'bedienung', BasicNode, nodeasbool=True),
    LLP(PID(2, 3, 0x0c), None, BasicNode),
    LLP(PID(2, 3, 0x0c, 1), 'programmdaten', ContentType.WORD, PROGRAMMDATEN, multipletimes=True),
)
msgidx[PID(2, 3)] = NEEDED_DATA

#
# ACK_NEEDED_DATA
# Zusi -> Client
#
ACK_NEEDED_DATA = namedtuple("ACK_NEEDED_DATA", ['status'], defaults=[None])
llps[ACK_NEEDED_DATA] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 4), None, BasicNode),
    LLP(PID(2, 4, 1), 'status', ContentType.BYTE),
)
msgidx[PID(2, 4)] = ACK_NEEDED_DATA

#
# DATA_FTD
# Zusi -> Client
#
DATA_FTD = namedtuple("DATA_FTD", ['geschwindigkeit', 'druck_hauptluftleitung', 'druck_bremszylinder', 'druck_hauptluftbehaelter', 'luftpresser_laeuft', 'luftstrom_fbv', 'luftstrom_zbv', 'luefter_an', 'zugkraft_gesamt', 'zugkraft_pro_achse', 'zugkraft_soll_gesamt', 'zugkraft_soll_pro_achse', 'oberstrom', 'fahrleitungsspannung', 'motordrehzahl', 'uhrzeit_stunde', 'uhrzeit_minute', 'uhrzeit_sekunde', 'hauptschalter', 'trennschuetz', 'fahrstufe', 'fenster_3d', 'afb_sollgeschwindigkeit', 'druck_hilfsbehaelter', 'zurueckgelegter_gesamtweg', 'lm_getriebe', 'lm_schleudern', 'lm_gleiten', 'lm_mg_bremse', 'lm_h_bremse', 'lm_r_bremse', 'lm_hochabbremsung', 'lm_schnellbremsung', 'lm_uhrzeit', 'lm_drehzahlverstellung', 'lm_fahrtrichtung_vor', 'lm_fahrtrichtung_zurueck', 'lm_fahrtrichtung_m', 'motordrehmoment', 'motorlast_normiert', 'tunnel', 'schienenstoss_weiche', 'stahlbruecke', 'steinbruecke', 'x_koordinate', 'y_koordinate', 'z_koordinate', 'utm_referenzpunkt_x', 'utm_referenzpunkt_y', 'utm_zone', 'utm_zone_2', 'afb_an', 'fahrpultintern_01', 'fahrpultintern_02', 'fahrpultintern_03', 'fahrpultintern_04', 'fahrpultintern_05', 'fahrpultintern_06', 'fahrpultintern_07', 'fahrpultintern_08', 'fahrpultintern_09', 'fahrpultintern_10', 'fahrpultintern_11', 'fahrpultintern_12', 'fahrpultintern_13', 'fahrpultintern_14', 'fahrpultintern_15', 'fahrpultintern_16', 'fahrpultintern_17', 'fahrpultintern_18', 'fahrpultintern_19', 'fahrpultintern_20', 'datum', 'gleiskruemung', 'streckenvmax', 'zugkraftvorschlag_autopilot', 'beschleunigung_x', 'beschleunigung_y', 'beschleunigung_z', 'drehbeschleunigung_x', 'drehbeschleunigung_y', 'drehbeschleunigung_z', 'stromabnehmer', 'lm_federspeicherbremse_angelegt', 'zustand_federspeicherbremse', 'stw_lm_getriebe', 'stw_lm_schleudern', 'stw_lm_gleiten', 'stw_lm_h_bremse', 'stw_lm_r_bremse', 'stw_lm_drehzahlverstellung', 'druck_zeitbehaelter', 'geschwindigkeit_absolut', 'zug_ist_entgleist', 'kilometrieung', 'motorstrom', 'motorspannung', 'fahrpultintern_21', 'fahrpultintern_22', 'fahrpultintern_23', 'fahrpultintern_24', 'fahrpultintern_25', 'fahrpultintern_26', 'fahrpultintern_27', 'fahrpultintern_28', 'fahrpultintern_29', 'fahrpultintern_30', 'fahrpultintern_31', 'fahrpultintern_32', 'fahrpultintern_33', 'fahrpultintern_34', 'fahrpultintern_35', 'fahrpultintern_36', 'fahrpultintern_37', 'fahrpultintern_38', 'fahrpultintern_39', 'fahrpultintern_40', 'stw_luefter_an', 'stw_zugkraft_gesamt', 'stw_zugkraft_pro_achse', 'stw_zugkraft_soll_gesamt', 'stw_zugkraft_soll_pro_achse', 'stw_oberstrom', 'stw_fahrleitungsspannung', 'stw_motordrehzahl_1', 'stw_hauptschalter', 'stw_trennschuetz', 'stw_fahrstufe', 'stw_motordrehmoment_1', 'stw_motorlast_normiert', 'stw_stromabnehmer', 'stw_motorstrom_1', 'stw_motorspannung_1', 'geschwindigkeit_absolut_mit_schleudern', 'batteriehauptschalter_aus', 'bremsprobefunktion', 'zug_und_bremskraft_normiert', 'stw_zug_und_bremskraft_normiert', 'zug_und_bremskraft_absolut_normiert', 'stw_zug_und_bremskraft_absolut_normiert', 'fahrzeugintern_01', 'fahrzeugintern_02', 'fahrzeugintern_03', 'fahrzeugintern_04', 'fahrzeugintern_05', 'fahrzeugintern_06', 'fahrzeugintern_07', 'fahrzeugintern_08', 'fahrzeugintern_09', 'fahrzeugintern_10', 'fahrzeugintern_11', 'fahrzeugintern_12', 'fahrzeugintern_13', 'fahrzeugintern_14', 'fahrzeugintern_15', 'fahrzeugintern_16', 'fahrzeugintern_17', 'fahrzeugintern_18', 'fahrzeugintern_19', 'fahrzeugintern_20', 'aussenhelligkeit', 'fuehrerstand_deaktiviert', 'solldruck_hl', 'stw_motordrehzahl_2', 'stw_motordrehmoment_2', 'stw_motorstrom_2', 'stw_motorspannung_2_'], defaults=[None] * 167)
llps[DATA_FTD] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 10), None, BasicNode),
    LLP(PID(2, 10, 0x01), 'geschwindigkeit', ContentType.SINGLE),
    LLP(PID(2, 10, 0x02), 'druck_hauptluftleitung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x03), 'druck_bremszylinder', ContentType.SINGLE),
    LLP(PID(2, 10, 0x04), 'druck_hauptluftbehaelter', ContentType.SINGLE),
    LLP(PID(2, 10, 0x05), 'luftpresser_laeuft', ContentType.SINGLE),
    LLP(PID(2, 10, 0x06), 'luftstrom_fbv', ContentType.SINGLE),
    LLP(PID(2, 10, 0x07), 'luftstrom_zbv', ContentType.SINGLE),
    LLP(PID(2, 10, 0x08), 'luefter_an', ContentType.SINGLE),
    LLP(PID(2, 10, 0x09), 'zugkraft_gesamt', ContentType.SINGLE),
    LLP(PID(2, 10, 0x0a), 'zugkraft_pro_achse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x0b), 'zugkraft_soll_gesamt', ContentType.SINGLE),
    LLP(PID(2, 10, 0x0c), 'zugkraft_soll_pro_achse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x0d), 'oberstrom', ContentType.SINGLE),
    LLP(PID(2, 10, 0x0e), 'fahrleitungsspannung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x0f), 'motordrehzahl', ContentType.SINGLE),
    LLP(PID(2, 10, 0x10), 'uhrzeit_stunde', ContentType.SINGLE),
    LLP(PID(2, 10, 0x11), 'uhrzeit_minute', ContentType.SINGLE),
    LLP(PID(2, 10, 0x12), 'uhrzeit_sekunde', ContentType.SINGLE),
    LLP(PID(2, 10, 0x13), 'hauptschalter', ContentType.SINGLE),
    LLP(PID(2, 10, 0x14), 'trennschuetz', ContentType.SINGLE),
    LLP(PID(2, 10, 0x15), 'fahrstufe', ContentType.SINGLE),
    LLP(PID(2, 10, 0x16), 'fenster_3d', ContentType.SINGLE),
    LLP(PID(2, 10, 0x17), 'afb_sollgeschwindigkeit', ContentType.SINGLE),
    LLP(PID(2, 10, 0x18), 'druck_hilfsbehaelter', ContentType.SINGLE),
    LLP(PID(2, 10, 0x19), 'zurueckgelegter_gesamtweg', ContentType.SINGLE),
    LLP(PID(2, 10, 0x1a), 'lm_getriebe', ContentType.SINGLE),
    LLP(PID(2, 10, 0x1b), 'lm_schleudern', ContentType.SINGLE),
    LLP(PID(2, 10, 0x1c), 'lm_gleiten', ContentType.SINGLE),
    LLP(PID(2, 10, 0x1d), 'lm_mg_bremse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x1e), 'lm_h_bremse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x1f), 'lm_r_bremse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x20), 'lm_hochabbremsung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x21), 'lm_schnellbremsung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x23), 'lm_uhrzeit', ContentType.SINGLE),
    LLP(PID(2, 10, 0x24), 'lm_drehzahlverstellung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x25), 'lm_fahrtrichtung_vor', ContentType.SINGLE),
    LLP(PID(2, 10, 0x26), 'lm_fahrtrichtung_zurueck', ContentType.SINGLE),
    LLP(PID(2, 10, 0x27), 'lm_fahrtrichtung_m', ContentType.SINGLE),
    LLP(PID(2, 10, 0x29), 'motordrehmoment', ContentType.SINGLE),
    LLP(PID(2, 10, 0x2a), 'motorlast_normiert', ContentType.SINGLE),
    LLP(PID(2, 10, 0x2b), 'tunnel', ContentType.SINGLE),
    LLP(PID(2, 10, 0x2c), 'schienenstoss_weiche', ContentType.SINGLE),
    LLP(PID(2, 10, 0x2d), 'stahlbruecke', ContentType.SINGLE),
    LLP(PID(2, 10, 0x2e), 'steinbruecke', ContentType.SINGLE),
    LLP(PID(2, 10, 0x2f), 'x_koordinate', ContentType.SINGLE),
    LLP(PID(2, 10, 0x30), 'y_koordinate', ContentType.SINGLE),
    LLP(PID(2, 10, 0x31), 'z_koordinate', ContentType.SINGLE),
    LLP(PID(2, 10, 0x32), 'utm_referenzpunkt_x', ContentType.SINGLE),
    LLP(PID(2, 10, 0x33), 'utm_referenzpunkt_y', ContentType.SINGLE),
    LLP(PID(2, 10, 0x34), 'utm_zone', ContentType.SINGLE),
    LLP(PID(2, 10, 0x35), 'utm_zone_2', ContentType.SINGLE),
    LLP(PID(2, 10, 0x36), 'afb_an', ContentType.SINGLE),
    LLP(PID(2, 10, 0x37), 'fahrpultintern_01', ContentType.SINGLE),
    LLP(PID(2, 10, 0x38), 'fahrpultintern_02', ContentType.SINGLE),
    LLP(PID(2, 10, 0x39), 'fahrpultintern_03', ContentType.SINGLE),
    LLP(PID(2, 10, 0x3a), 'fahrpultintern_04', ContentType.SINGLE),
    LLP(PID(2, 10, 0x3b), 'fahrpultintern_05', ContentType.SINGLE),
    LLP(PID(2, 10, 0x3c), 'fahrpultintern_06', ContentType.SINGLE),
    LLP(PID(2, 10, 0x3d), 'fahrpultintern_07', ContentType.SINGLE),
    LLP(PID(2, 10, 0x3e), 'fahrpultintern_08', ContentType.SINGLE),
    LLP(PID(2, 10, 0x3f), 'fahrpultintern_09', ContentType.SINGLE),
    LLP(PID(2, 10, 0x40), 'fahrpultintern_10', ContentType.SINGLE),
    LLP(PID(2, 10, 0x41), 'fahrpultintern_11', ContentType.SINGLE),
    LLP(PID(2, 10, 0x42), 'fahrpultintern_12', ContentType.SINGLE),
    LLP(PID(2, 10, 0x43), 'fahrpultintern_13', ContentType.SINGLE),
    LLP(PID(2, 10, 0x44), 'fahrpultintern_14', ContentType.SINGLE),
    LLP(PID(2, 10, 0x45), 'fahrpultintern_15', ContentType.SINGLE),
    LLP(PID(2, 10, 0x46), 'fahrpultintern_16', ContentType.SINGLE),
    LLP(PID(2, 10, 0x47), 'fahrpultintern_17', ContentType.SINGLE),
    LLP(PID(2, 10, 0x48), 'fahrpultintern_18', ContentType.SINGLE),
    LLP(PID(2, 10, 0x49), 'fahrpultintern_19', ContentType.SINGLE),
    LLP(PID(2, 10, 0x4a), 'fahrpultintern_20', ContentType.SINGLE),
    LLP(PID(2, 10, 0x4b), 'datum', ContentType.SINGLE),
    LLP(PID(2, 10, 0x4c), 'gleiskruemung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x4d), 'streckenvmax', ContentType.SINGLE),
    LLP(PID(2, 10, 0x4e), 'zugkraftvorschlag_autopilot', ContentType.SINGLE),
    LLP(PID(2, 10, 0x4f), 'beschleunigung_x', ContentType.SINGLE),
    LLP(PID(2, 10, 0x50), 'beschleunigung_y', ContentType.SINGLE),
    LLP(PID(2, 10, 0x51), 'beschleunigung_z', ContentType.SINGLE),
    LLP(PID(2, 10, 0x52), 'drehbeschleunigung_x', ContentType.SINGLE),
    LLP(PID(2, 10, 0x53), 'drehbeschleunigung_y', ContentType.SINGLE),
    LLP(PID(2, 10, 0x54), 'drehbeschleunigung_z', ContentType.SINGLE),
    LLP(PID(2, 10, 0x55), 'stromabnehmer', ContentType.SINGLE),
    LLP(PID(2, 10, 0x56), 'lm_federspeicherbremse_angelegt', ContentType.SINGLE),
    LLP(PID(2, 10, 0x57), 'zustand_federspeicherbremse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x58), 'stw_lm_getriebe', ContentType.SINGLE),
    LLP(PID(2, 10, 0x59), 'stw_lm_schleudern', ContentType.SINGLE),
    LLP(PID(2, 10, 0x5a), 'stw_lm_gleiten', ContentType.SINGLE),
    LLP(PID(2, 10, 0x5b), 'stw_lm_h_bremse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x5c), 'stw_lm_r_bremse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x5d), 'stw_lm_drehzahlverstellung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x5e), 'druck_zeitbehaelter', ContentType.SINGLE),
    LLP(PID(2, 10, 0x5f), 'geschwindigkeit_absolut', ContentType.SINGLE),
    LLP(PID(2, 10, 0x60), 'zug_ist_entgleist', ContentType.SINGLE),
    LLP(PID(2, 10, 0x61), 'kilometrieung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x62), 'motorstrom', ContentType.SINGLE),
    LLP(PID(2, 10, 0x63), 'motorspannung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x67), 'fahrpultintern_21', ContentType.SINGLE),
    LLP(PID(2, 10, 0x68), 'fahrpultintern_22', ContentType.SINGLE),
    LLP(PID(2, 10, 0x69), 'fahrpultintern_23', ContentType.SINGLE),
    LLP(PID(2, 10, 0x6a), 'fahrpultintern_24', ContentType.SINGLE),
    LLP(PID(2, 10, 0x6b), 'fahrpultintern_25', ContentType.SINGLE),
    LLP(PID(2, 10, 0x6c), 'fahrpultintern_26', ContentType.SINGLE),
    LLP(PID(2, 10, 0x6d), 'fahrpultintern_27', ContentType.SINGLE),
    LLP(PID(2, 10, 0x6e), 'fahrpultintern_28', ContentType.SINGLE),
    LLP(PID(2, 10, 0x6f), 'fahrpultintern_29', ContentType.SINGLE),
    LLP(PID(2, 10, 0x70), 'fahrpultintern_30', ContentType.SINGLE),
    LLP(PID(2, 10, 0x71), 'fahrpultintern_31', ContentType.SINGLE),
    LLP(PID(2, 10, 0x72), 'fahrpultintern_32', ContentType.SINGLE),
    LLP(PID(2, 10, 0x73), 'fahrpultintern_33', ContentType.SINGLE),
    LLP(PID(2, 10, 0x74), 'fahrpultintern_34', ContentType.SINGLE),
    LLP(PID(2, 10, 0x75), 'fahrpultintern_35', ContentType.SINGLE),
    LLP(PID(2, 10, 0x76), 'fahrpultintern_36', ContentType.SINGLE),
    LLP(PID(2, 10, 0x77), 'fahrpultintern_37', ContentType.SINGLE),
    LLP(PID(2, 10, 0x78), 'fahrpultintern_38', ContentType.SINGLE),
    LLP(PID(2, 10, 0x79), 'fahrpultintern_39', ContentType.SINGLE),
    LLP(PID(2, 10, 0x7a), 'fahrpultintern_40', ContentType.SINGLE),
    LLP(PID(2, 10, 0x7b), 'stw_luefter_an', ContentType.SINGLE),
    LLP(PID(2, 10, 0x7c), 'stw_zugkraft_gesamt', ContentType.SINGLE),
    LLP(PID(2, 10, 0x7d), 'stw_zugkraft_pro_achse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x7e), 'stw_zugkraft_soll_gesamt', ContentType.SINGLE),
    LLP(PID(2, 10, 0x7f), 'stw_zugkraft_soll_pro_achse', ContentType.SINGLE),
    LLP(PID(2, 10, 0x80), 'stw_oberstrom', ContentType.SINGLE),
    LLP(PID(2, 10, 0x81), 'stw_fahrleitungsspannung', ContentType.SINGLE),
    LLP(PID(2, 10, 0x82), 'stw_motordrehzahl_1', ContentType.SINGLE),
    LLP(PID(2, 10, 0x83), 'stw_hauptschalter', ContentType.SINGLE),
    LLP(PID(2, 10, 0x84), 'stw_trennschuetz', ContentType.SINGLE),
    LLP(PID(2, 10, 0x85), 'stw_fahrstufe', ContentType.SINGLE),
    LLP(PID(2, 10, 0x86), 'stw_motordrehmoment_1', ContentType.SINGLE),
    LLP(PID(2, 10, 0x87), 'stw_motorlast_normiert', ContentType.SINGLE),
    LLP(PID(2, 10, 0x88), 'stw_stromabnehmer', ContentType.SINGLE),
    LLP(PID(2, 10, 0x89), 'stw_motorstrom_1', ContentType.SINGLE),
    LLP(PID(2, 10, 0x8a), 'stw_motorspannung_1', ContentType.SINGLE),
    LLP(PID(2, 10, 0x8b), 'geschwindigkeit_absolut_mit_schleudern', ContentType.SINGLE),
    LLP(PID(2, 10, 0x8c), 'batteriehauptschalter_aus', ContentType.SINGLE),
    LLP(PID(2, 10, 0x8f), 'bremsprobefunktion', ContentType.SINGLE),
    LLP(PID(2, 10, 0x90), 'zug_und_bremskraft_normiert', ContentType.SINGLE),
    LLP(PID(2, 10, 0x91), 'stw_zug_und_bremskraft_normiert', ContentType.SINGLE),
    LLP(PID(2, 10, 0x93), 'zug_und_bremskraft_absolut_normiert', ContentType.SINGLE),
    LLP(PID(2, 10, 0x94), 'stw_zug_und_bremskraft_absolut_normiert', ContentType.SINGLE),
    LLP(PID(2, 10, 0x95), 'fahrzeugintern_01', ContentType.SINGLE),
    LLP(PID(2, 10, 0x96), 'fahrzeugintern_02', ContentType.SINGLE),
    LLP(PID(2, 10, 0x97), 'fahrzeugintern_03', ContentType.SINGLE),
    LLP(PID(2, 10, 0x98), 'fahrzeugintern_04', ContentType.SINGLE),
    LLP(PID(2, 10, 0x99), 'fahrzeugintern_05', ContentType.SINGLE),
    LLP(PID(2, 10, 0x9a), 'fahrzeugintern_06', ContentType.SINGLE),
    LLP(PID(2, 10, 0x9b), 'fahrzeugintern_07', ContentType.SINGLE),
    LLP(PID(2, 10, 0x9c), 'fahrzeugintern_08', ContentType.SINGLE),
    LLP(PID(2, 10, 0x9d), 'fahrzeugintern_09', ContentType.SINGLE),
    LLP(PID(2, 10, 0x9e), 'fahrzeugintern_10', ContentType.SINGLE),
    LLP(PID(2, 10, 0x9f), 'fahrzeugintern_11', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa0), 'fahrzeugintern_12', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa1), 'fahrzeugintern_13', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa2), 'fahrzeugintern_14', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa3), 'fahrzeugintern_15', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa4), 'fahrzeugintern_16', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa5), 'fahrzeugintern_17', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa6), 'fahrzeugintern_18', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa7), 'fahrzeugintern_19', ContentType.SINGLE),
    LLP(PID(2, 10, 0xa8), 'fahrzeugintern_20', ContentType.SINGLE),
    LLP(PID(2, 10, 0xaa), 'aussenhelligkeit', ContentType.SINGLE),
    LLP(PID(2, 10, 0xac), 'fuehrerstand_deaktiviert', ContentType.SINGLE),
    LLP(PID(2, 10, 0xad), 'solldruck_hl', ContentType.SINGLE),
    LLP(PID(2, 10, 0xae), 'stw_motordrehzahl_2', ContentType.SINGLE),
    LLP(PID(2, 10, 0xaf), 'stw_motordrehmoment_2', ContentType.SINGLE),
    LLP(PID(2, 10, 0xb0), 'stw_motorstrom_2', ContentType.SINGLE),
    LLP(PID(2, 10, 0xb1), 'stw_motorspannung_2_', ContentType.SINGLE)

)
msgidx[PID(2, 10)] = DATA_FTD

#
# STATUS_NOTBREMSSYSTEM
# Zusi -> Client (Submessage)
#
class STATUS_NB_UEBERBRUECKUNG(Enum):
    NBU_AUS = 0
    NBU_BEREIT = 1
    NOTBREMSE_GEZOGEN = 2
    NOTBREMSE_WIRKT_NBU_BEREIT = 3
    NBU_AKTIVIERT_NOTBREMSE_GEBRUECKT = 4
    NOTBREMSE_WIRKT_NBU_AUS = 5
    NBU_DAUERAKTIV = 6
class STATUS_NB_TEST(Enum):
    NORMAL = 0
    TEST_AKTIV = 1
STATUS_NOTBREMSSYSTEM = namedtuple("STATUS_NOTBREMSSYSTEM", ['bauart', 'status', 'm_system_bereit', 'm_notbremsung', 'modus', 'lm_system_bereit', 'lm_notbremsung'], defaults=[None] * 7)
llps[STATUS_NOTBREMSSYSTEM] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x22), None, BasicNode),
    LLP(PID(2, 0x0a, 0x22, 1), 'bauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x22, 2), 'status', ContentType.BYTE, STATUS_NB_UEBERBRUECKUNG),
    LLP(PID(2, 0x0a, 0x22, 3), 'm_system_bereit', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x22, 4), 'm_notbremsung', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x22, 5), 'modus', ContentType.BYTE, STATUS_NB_TEST),
    LLP(PID(2, 0x0a, 0x22, 6), 'lm_system_bereit', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x22, 7), 'lm_notbremsung', ContentType.BYTE, LMZUSTAND)
)
msgidx[PID(2, 0x0a, 0x22)] = STATUS_NOTBREMSSYSTEM

#
# STATUS_SIFA
# Zusi -> Client (Submessage)
#
class STATUS_SIFA_HUPE(Enum):
    HUPE_AUS = 0
    HUPE_WARNUNG = 1
    HUPE_ZWANGSBREMSUNG = 2
STATUS_SIFA = namedtuple("STATUS_SIFA", ['bauart', 'lm', 'hupe', 'hauptschalter', 'stoerschalter', 'lufthahn', 'weg'], defaults=[None] * 7)
llps[STATUS_SIFA] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x64), None, BasicNode),
    LLP(PID(2, 0x0a, 0x64, 1), 'bauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x64, 2), 'lm', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x64, 3), 'hupe', ContentType.BYTE, STATUS_SIFA_HUPE),
    LLP(PID(2, 0x0a, 0x64, 4), 'hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x64, 5), 'stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x64, 6), 'lufthahn', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x64, 7), 'weg', ContentType.SINGLE)
)
msgidx[PID(2, 0x0a, 0x64)] = STATUS_SIFA

#
# STATUS_ZUGBEEINFLUSSUNG (Grundblock)
# Zusi -> Client (Submessage)
#
STATUS_ZUGBEEINFLUSSUNG_GRUND = namedtuple("STATUS_ZUGBEEINFLUSSUNG", ['bauart'], defaults=[None])
llps[STATUS_ZUGBEEINFLUSSUNG_GRUND] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 1), 'bauart', ContentType.STRING)
)
msgidx[PID(2, 0x0a, 0x65)] = STATUS_ZUGBEEINFLUSSUNG_GRUND

#
# STATUS_INDUSI_EINSTELLUNGEN
# Zusi -> Client (Submessage) 
#
class INDUSI_ZUGART(Enum):
    UNBEKANNT = 0
    NICHT_BESTIMMT = 1
    U = 2
    M = 3
    O = 4
    S_BAHN = 5
class INDUSI_SYSTEMSTATUS(Enum):
    AUSGESCHALTET = 0
    ABGESCHALTET = 1
    UNTERDRUECKT = 2
    AKTIV = 3
class INDUSI_MODUS(Enum):
    UNDEFINIERT = 0
    GRUNDDATEN = 4
    ERSATZZUGDATEN = 5
    NORMALBETRIEB = 6
class INDUSI_KLARTEXTMELDUNGEN(Enum):
    KEINE_MOEGLICH = 0
    MOEGLICH_ABER_NICHT_AKTIV = 1
    AKTIV = 2
    NUR_KLARTEXTMELDUNGEN = 3
class INDUSI_FUNKTIONSPRUEFUNG_STARTEN(Enum):
    ZUSI_SOLL_STARTEN = 1
    WURDE_QUITTIERT = 2
    WURDE_NICHT_QUITTIERT = 3
class INDUSI_STOERSCHALTERBAURT(Enum):
    LEUCHTDRUCKTASTER = 0
    DREHSCHALTER = 1
STATUS_INDUSI_EINSTELLUNGEN = namedtuple("STATUS_INDUSI_EINSTELLUNGEN", [
    'zugart', 'hauptschalter', 'indusi_stoerschalter', 'luftabsperhan', 'systemstatus', 'bauart',
    'tfnr', 'zugnummer', 'e_brh', 'e_bra', 'e_zugart', 'a_brh', 'a_bra', 'a_zugart', 'a_modus', 'klartextmeldungen', 'funktionspruefung_starten', 'indusi_stoerschalterbauart',
    'g_brh', 'g_bra', 'g_zl', 'g_vmz', 'g_zugart', 'e_zl', 'e_vmz', 'a_zl', 'a_vmz', 'lzb_stoerschalter', 'lzb_stoerschalterbaurt', 'lzb_systemstatus',
    ], defaults=([None] * 30))
llps[STATUS_INDUSI_EINSTELLUNGEN] = (
    # Indusi Analogsysteme und Basisdaten
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 1), 'zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 7), 'hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 8), 'indusi_stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0a), 'luftabsperhan', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0d), 'systemstatus', ContentType.BYTE, INDUSI_SYSTEMSTATUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0e), 'bauart', ContentType.STRING),
    # Indusi I60R/I80/PZB90
    LLP(PID(2, 0x0a, 0x65, 2, 2), 'tfnr', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 2, 3), 'zugnummer', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 2, 5), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 5, 1), 'e_brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 5, 2), 'e_bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 5, 5), 'e_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 6), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 6, 1), 'a_brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 6, 2), 'a_bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 6, 5), 'a_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 6, 6), 'a_modus', ContentType.BYTE, INDUSI_MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0b), 'klartextmeldungen', ContentType.BYTE, INDUSI_KLARTEXTMELDUNGEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0c), 'funktionspruefung_starten', ContentType.BYTE, INDUSI_FUNKTIONSPRUEFUNG_STARTEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0f), 'indusi_stoerschalterbauart', ContentType.BYTE, INDUSI_STOERSCHALTERBAURT),
    # LZB
    LLP(PID(2, 0x0a, 0x65, 2, 4), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 4, 1), 'g_brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 4, 2), 'g_bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 4, 3), 'g_zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 4, 4), 'g_vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 4, 5), 'g_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 5, 3), 'e_zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 5, 4), 'e_vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 6, 3), 'a_zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 6, 4), 'a_vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 9), 'lzb_stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x10), 'lzb_stoerschalterbaurt', ContentType.BYTE, INDUSI_STOERSCHALTERBAURT),
    LLP(PID(2, 0x0a, 0x65, 2, 0x11), 'lzb_systemstatus', ContentType.BYTE, INDUSI_SYSTEMSTATUS),
)
msgidx[PID(2, 0x0a, 0x65, 2)] = STATUS_INDUSI_EINSTELLUNGEN

#
# STATUS_INDUSI_BETRIEBSDATEN
# Zusi -> Client (Submessage) 
#
class INDUSI_ZUSTAND(Enum):
    UNBEKANNT = 0
    AUSGESCHALTET = 1
    ABGESCHALTET_GESTOERT = 2
    HLL_DRUCK_NIEDRIG = 3
    AUFFORDERUNG_ZUGDATENEINGABE = 4
    NORMALBETRIEB = 5
    FUNKTIONSPRUEFUNG = 6
    FUNKTIONSPRUEFUNG_QUITTIERUNG_FEHLT = 7
class INDUSI_ZWANGSBREMSUNG(Enum):
    KEINE_ZWANGSBREMSUNG = 0
    WACHSAM = 1
    TAUSEND_HZ = 2
    FUENFHUNDERT_HZ = 3
    ZWEITAUSEND_HZ = 4
    KEIN_HALT_NACH_BEFREIUNG = 5
    FZ_VMAX = 6
    FUNKTIONSPRUEFUNG = 7
    FUENFHUNDERT_HZ_NACH_BEFREIUNG = 8
    LZB_HALT_UEBERFAHREN = 9
    LZB_RECHNERAUSFALL = 10
    LZB_NOTHALT_UEBERFAHREN = 11
    LZB_UEBERTRAGUNGSAUSFALL = 12
    V_UEBERSCHREITUNG_NACH_LZB_AUSFALL = 13
    RICHTUNGSSCHALTER_VERLEGT = 14
    LZB_RUECKROLLUEBERWACHUNG = 25
    LZB_UEBERSCHREITUNG_200M_NACH_BEFEHL40_BLINKT = 26
    ALLGEMEINE_STOERUNG = 27
    STROMVERSORGUNG_FEHLT = 28
class INDUSI_HUPE(Enum):
    AUS = 0
    HUPE = 1
    ZWANGSBREMSUNG = 2
class INDUSI_PZB90_ZUSATZINFO_MELDERBILD(Enum):
    NORMALZUSTAND = 0
    TAUSEND_HZ_NACH_700M = 1
    RESTRIKTIV = 2
    RESTRIKTIV_1000HZ = 3
    RESTRIKTIV_500HZ = 4
    PRUEFABLAUF = 5
class INDUSI_LZB_ZUSTAND(Enum):
    KEINE_FUEHRUNG = 0
    NORMAL = 1
    NOTHALT = 2
    HALT_UEBERFAHREN = 3
    RECHNERAUSFALL = 4
    NACHFAHRAUFTAG = 5
    FUNKTIONSPRUEFUNG = 6
class INDUSI_LZB_ENDE_VERFAHREN(Enum):
    EINGELETITET = 1
    QUITTIERT = 2
class INDUSI_LZB_FALSCHFAHRAUFTRAG(Enum):
    EINGELETITET = 1
    QUITTIERT = 2
class INDUSI_LZB_VORSICHTSAUFTRAG(Enum):
    EINGELETITET = 1
    QUITTIERT = 2
    FAHRT_AUF_SICHT = 3
class INDUSI_LZB_ZIELGESCHWINDIGKEIT(Enum):
    EINGELEITET = 1
    UE_BLINKT = 2
    ERSTE_QUITTIERUNG = 3
    BEDINGUNG_2_QUTTIERUNG = 4
    ZWEITE_QUITTIERUNG = 5
    AUSFALL = 6
    BEFEHL_BLINKT = 7
class INDUSI_LZB_NOTHALT(Enum):
    NOTHALT_EMPFANGEN = 1
    NOTHALT_UEBERFAHREN = 2
    NOTHALT_AUFGEHOBEN = 3
class INDUSI_LZB_RECHNERAUSFALL(Enum):
    ALLES_DUNKEL = 1
    BEFEHLSMELDER_BLINKT = 2
    BEFEHLSMELDER_DAUERLICHT = 3
class INDUSI_LZB_EL_AUFTAG(Enum):
    HS_AUS = 1
    SA_SENKEN = 2
class INDUSI_LZB_CIR_ELKE_MODUS(Enum):
    NORMALER_MODUS = 0
    CIR_ELKE_MODUS = 1
class INDUSI_LZB_ANZEIGEMODUS(Enum):
    NORMALER_MODUS = 0
    MFA = 1
STATUS_INDUSI_BETRIEBSDATEN = namedtuple("STATUS_INDUSI_BETRIEBSDATEN", [
    'zustand', 'zwangsbremsung', 'zwangsbremsung_grund', 'm_1000hz', 'm_u', 'm_m', 'm_o', 'hupe', 'beeinflussung_1000hz', 'beeinflussung_500hz', 'beeinflussung_2000hz', 'lm_1000hz',
    'm_500hz', 'm_befehl_an', 'lm_o', 'lm_m', 'lm_u', 'lm_500hz', 'lm_befehl',
    'zusatzinfo_melderbild',
    'm_zugart_links', 'm_zugart_65', 'm_zugart_rechts', 'lm_zugart_rechts', 'lm_zugart_65', 'lm_zugart_links',
    'lzb_zustand', 'lzb_ende_verfahren', 'lzb_falschfahrauftrag', 'lzb_vorsichtsauftrag', 'lzb_zielgeschwindigkeit_ausfall', 'lzb_zielgeschwindigkeit_modus', 'lzb_zielweg_cir_elke', 'lzb_nothalt', 'lzb_nothalt_gesendet', 'lzb_rechnerausfall', 'lzb_el_auftag', 'm_h', 'm_e40', 'm_ende', 'm_b', 'm_ue', 'm_g', 'm_el', 'm_v40', 'm_s', 'm_pruef_stoer', 'lzb_sollgeschwindigkeit', 'lzb_zielgeschwindigkeit', 'lzb_zielweg', 'lm_g', 'lm_pruef_stoer', 'lzb_cir_elke_modus', 'lzb_anzeigemodus', 'lm_h', 'lm_e40', 'lm_ende', 'lm_b', 'lm_ue', 'lm_el', 'lm_v40', 'lm_s'
    ], defaults=([None] * 62))
llps[STATUS_INDUSI_BETRIEBSDATEN] = (
    # Indusi Analogsysteme und Basisdaten
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 2), 'zustand', ContentType.WORD, INDUSI_ZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 3), 'zwangsbremsung', ContentType.WORD, INDUSI_ZWANGSBREMSUNG),
    LLP(PID(2, 0x0a, 0x65, 3, 4), 'zwangsbremsung_grund', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 3, 5), 'm_1000hz',ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 6), 'm_u', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 7), 'm_m', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 8), 'm_o', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 9), 'hupe', ContentType.BYTE, INDUSI_HUPE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2c), 'beeinflussung_1000hz', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2d), 'beeinflussung_500hz', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2e), 'beeinflussung_2000hz',  ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2f), 'lm_1000hz', ContentType.BYTE, LMZUSTAND),
    # Indusi I60R/I80/PZB90
    LLP(PID(2, 0x0a, 0x65, 3, 0x0A), 'm_500hz', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0B), 'm_befehl_an', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x30), 'lm_o', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x31), 'lm_m', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x32), 'lm_u', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x33), 'lm_500hz', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x34), 'lm_befehl', ContentType.BYTE, LMZUSTAND),
    # PZB90
    LLP(PID(2, 0x0a, 0x65, 3, 0x0C), 'zusatzinfo_melderbild', ContentType.BYTE, INDUSI_PZB90_ZUSATZINFO_MELDERBILD),
    # PZB90 S-Bahn
    LLP(PID(2, 0x0a, 0x65, 3, 0x29), 'm_zugart_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2a), 'm_zugart_65', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2b), 'm_zugart_rechts', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x35), 'lm_zugart_rechts', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x36), 'lm_zugart_65', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x37), 'lm_zugart_links', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    # LZB
    LLP(PID(2, 0x0a, 0x65, 3, 0x0d), 'lzb_zustand', ContentType.WORD, INDUSI_LZB_ZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0e), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0e, 1), 'lzb_ende_verfahren', ContentType.BYTE, INDUSI_LZB_ENDE_VERFAHREN),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0f), None, BasicNode), # Ersatzauftrag aktiv
    LLP(PID(2, 0x0a, 0x65, 3, 0x10), None, BasicNode), # Falschfahrauftrag aktiv
    LLP(PID(2, 0x0a, 0x65, 3, 0x10, 1), 'lzb_falschfahrauftrag', ContentType.BYTE, INDUSI_LZB_FALSCHFAHRAUFTRAG),
    LLP(PID(2, 0x0a, 0x65, 3, 0x11), None, BasicNode), # Vorsichtsauftrag aktiv
    LLP(PID(2, 0x0a, 0x65, 3, 0x11, 1), 'lzb_vorsichtsauftrag', ContentType.BYTE, INDUSI_LZB_VORSICHTSAUFTRAG),
    LLP(PID(2, 0x0a, 0x65, 3, 0x12), None, BasicNode), # Fahrt über LZB-Halt per Befehl
    LLP(PID(2, 0x0a, 0x65, 3, 0x13), None, BasicNode), # Übertragungsausfall
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 1), 'lzb_zielgeschwindigkeit_ausfall', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 2), 'lzb_zielgeschwindigkeit_modus', ContentType.WORD, INDUSI_LZB_ZIELGESCHWINDIGKEIT),
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 3), 'lzb_zielweg_cir_elke', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x14), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x14, 1), 'lzb_nothalt', ContentType.BYTE, INDUSI_LZB_NOTHALT),
    LLP(PID(2, 0x0a, 0x65, 3, 0x14, 2), 'lzb_nothalt_gesendet', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x15), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x15, 1), 'lzb_rechnerausfall', ContentType.BYTE, INDUSI_LZB_RECHNERAUSFALL),
    LLP(PID(2, 0x0a, 0x65, 3, 0x16), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x16, 1), 'lzb_el_auftag', ContentType.BYTE, INDUSI_LZB_EL_AUFTAG),
    LLP(PID(2, 0x0a, 0x65, 3, 0x17), 'm_h', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x18), 'm_e40', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x19), 'm_ende', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1a), 'm_b', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1b), 'm_ue', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1c), 'm_g', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1d), 'm_el', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1e), 'm_v40', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1f), 'm_s', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x20), 'm_pruef_stoer', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x21), 'lzb_sollgeschwindigkeit', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x22), 'lzb_zielgeschwindigkeit', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x23), 'lzb_zielweg', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x24), 'lm_g', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x25), 'lm_pruef_stoer', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x26), 'lzb_cir_elke_modus', ContentType.BYTE, INDUSI_LZB_CIR_ELKE_MODUS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x27), 'lzb_anzeigemodus', ContentType.BYTE, INDUSI_LZB_ANZEIGEMODUS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28), None, BasicNode), # Funktionsprüfung läuft # FIXME how?????
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,1), None, BasicNode), # Alle Melder blinken
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,2), None, BasicNode), # Anzeige der Führungsgrößen
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,3), None, BasicNode), # B ist an, Ü ist aus
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,4), None, BasicNode), # Zwangsbremsung aktiv
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,5), None, BasicNode), # Quittierung erwartet
    LLP(PID(2, 0x0a, 0x65, 3, 0x38), 'lm_h', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x39), 'lm_e40', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3a), 'lm_ende', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3b), 'lm_b', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3c), 'lm_ue', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3d), 'lm_el', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3e), 'lm_v40', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3f), 'lm_s', ContentType.BYTE, LMZUSTAND)
)
msgidx[PID(2, 0x0a, 0x65, 3)] = STATUS_INDUSI_BETRIEBSDATEN

#
# STATUS_ETCS_EINSTELLUNGEN
# Zusi -> Client (Submessage) 
#
# FIXME Platzhalter, muss noch vollständig umgesetzt werden
STATUS_ETCS_EINSTELLUNGEN = namedtuple("STATUS_ETCS_EINSTELLUNGEN", ['zustand'], defaults=[None])
llps[STATUS_ETCS_EINSTELLUNGEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 4), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 4, 1), 'zustand', ContentType.BYTE)
)
msgidx[PID(2, 0x0a, 0x65, 4)] = STATUS_ETCS_EINSTELLUNGEN

#
# STATUS_ETCS_BETRIEBSDATEN
# Zusi -> Client (Submessage) 
#
# FIXME Platzhalter, muss noch vollständig umgesetzt werden
STATUS_ETCS_BETRIEBSDATEN = namedtuple("STATUS_ETCS_BETRIEBSDATEN", ['aktiver_level'], defaults=[None])
llps[STATUS_ETCS_BETRIEBSDATEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 5), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 5, 1), 'aktiver_level', ContentType.WORD)
)
msgidx[PID(2, 0x0a, 0x65, 5)] = STATUS_ETCS_BETRIEBSDATEN


#
# STATUS_ZUB_EINSTELLUNGEN
# Zusi -> Client (Submessage) 
#
class ZUB_SYSTEMSTATUS(Enum):
    AUSGESCHALTET = 0
    ABGESCHALTET = 1
    UNTERDRUECKT = 2
    AKTIV = 3
STATUS_ZUB_EINSTELLUNGEN = namedtuple("STATUS_ZUB_EINSTELLUNGEN", ['brh','zuglaenge', 'vmz', 'status', 'bauart'], defaults=[None] * 5)
llps[STATUS_ZUB_EINSTELLUNGEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 6), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 6, 1), 'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 6, 2), 'zuglaenge', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 6, 3), 'vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 6, 4), 'status', ContentType.BYTE, ZUB_SYSTEMSTATUS),
    LLP(PID(2, 0x0a, 0x65, 6, 5), 'bauart', ContentType.STRING)
)
msgidx[PID(2, 0x0a, 0x65, 6)] = STATUS_ZUB_EINSTELLUNGEN

#
# STATUS_ZUB_BETRIEBSDATEN
# Zusi -> Client (Submessage) 
#
STATUS_ZUB_BETRIEBSDATEN = namedtuple("STATUS_ZUB_BETRIEBSDATEN", ['aktiver_level'], defaults=[None])
llps[STATUS_ZUB_BETRIEBSDATEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 7), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 7, 1), 'm_gnt', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 2), 'm_gnt_ue', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 3), 'm_gnt_g', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 4), 'm_gnt_s', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 5), 'm_gnt_gst', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 6), 'm_gnt_gst_stoer', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 7), 'lm_gnt_ue', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 7, 8), 'lm_gnt_g', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 7, 9), 'lm_gnt_s', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 7, 0x0a), 'zwangsbremsung', ContentType.WORD, INDUSI_ZWANGSBREMSUNG),
    LLP(PID(2, 0x0a, 0x65, 7, 0x0b), 'zwangsbremsung_aktiv', ContentType.BYTE)
)
msgidx[PID(2, 0x0a, 0x65, 7)] = STATUS_ZUB_BETRIEBSDATEN

#
# STATUS_ZBS_EINSTELLUNGEN
# Zusi -> Client (Submessage) 
#
# FIXME Platzhalter, muss noch vollständig umgesetzt werden
STATUS_ZBS_EINSTELLUNGEN = namedtuple("STATUS_ZBS_EINSTELLUNGEN", ['index'], defaults=[None])
llps[STATUS_ZBS_EINSTELLUNGEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 8), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 8, 1), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 8, 1, 1), 'zustand', ContentType.WORD)
)
msgidx[PID(2, 0x0a, 0x65, 8)] = STATUS_ZBS_EINSTELLUNGEN

#
# STATUS_ZBS_BETRIEBSDATEN
# Zusi -> Client (Submessage) 
#
# FIXME Platzhalter, muss noch vollständig umgesetzt werden
STATUS_ZBS_BETRIEBSDATEN = namedtuple("STATUS_ZBS_BETRIEBSDATEN", ['betriebszustand'], defaults=[None])
llps[STATUS_ZBS_BETRIEBSDATEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 9), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 9, 1), 'betriebszustand', ContentType.WORD)
)
msgidx[PID(2, 0x0a, 0x65, 9)] = STATUS_ZBS_BETRIEBSDATEN

#
# STATUS_FAHRSPERRE_EINSTELLUNGEN
# Zusi -> Client (Submessage) 
#
STATUS_FAHRSPERRE_EINSTELLUNGEN = namedtuple("STATUS_FAHRSPERRE_EINSTELLUNGEN", ['stoerschalter', 'hauptschalter', 'systemstatus', 'bauart', 'zugneustart'], defaults=[None] * 5)
llps[STATUS_FAHRSPERRE_EINSTELLUNGEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 0x0a, 1), 'stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 0x0a, 2), 'hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 0x0a, 3), 'systemstatus', ContentType.BYTE, INDUSI_SYSTEMSTATUS),
    LLP(PID(2, 0x0a, 0x65, 0x0a, 4), 'bauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 0x0a, 8), 'zugneustart', ContentType.STRING)
)
msgidx[PID(2, 0x0a, 0x65, 0x0a)] = STATUS_FAHRSPERRE_EINSTELLUNGEN

#
# STATUS_FAHRSPERRE_BETRIEBSDATEN
# Zusi -> Client (Submessage) 
#
STATUS_FAHRSPERRE_BETRIEBSDATEN = namedtuple("STATUS_FAHRSPERRE_BETRIEBSDATEN", ['melder', 'zwangsbremsung', 'zaehler_gewollte_vorbeifahrt', 'zaehler_ungewollte_vorbeifahrt'], defaults=[None] * 4)
llps[STATUS_FAHRSPERRE_BETRIEBSDATEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 0x0b), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 0x0b, 1), 'melder', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 0x0b, 1), 'zwangsbremsung', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 0x0b, 1), 'zaehler_gewollte_vorbeifahrt', ContentType.CARDINAL),
    LLP(PID(2, 0x0a, 0x65, 0x0b, 1), 'zaehler_ungewollte_vorbeifahrt', ContentType.CARDINAL)
)
msgidx[PID(2, 0x0a, 0x65, 0x0b)] = STATUS_FAHRSPERRE_BETRIEBSDATEN


#
# STATUS_TUEREN
# Zusi -> Client
#
class TUEREN_SEITE(Enum):
    ZU = 0
    OEFFNEND = 1
    OFFEN = 2
    FAHRGASTWECHSEL_ABGESCHLOSSEN = 3
    SCHLIESSEND = 4
    GESTOERT = 5
    BLOCKIERT = 6
class TUEREN_ZUSTAND(Enum):
    ALLE_ZU = 0
    MIN_EINE_OFFEN = 1
class TUEREN_SEITENWAHL(Enum):
    ZU = 0
    LINKS = 1
    RECHTS = 2
    BEIDE = 3
STATUS_TUEREN = namedtuple("STATUS_TUEREN", [
    'bauart','links', 'rechts', 'traktionssperre', 'zustand',
    'seitenwahl', 'm_links', 'm_rechts', 'lm_links', 'lm_rechts', 'm_zwnagsschliessen', 'lm_zwangsschliessen', 'm_rechts_links', 'lm_rechts_links', 'm_zentrales_oeffnen_links', 'm_zentrales_oeffnen_rechts', 'lm_zentrales_oeffnen_links', 'lm_zentrales_oeffnen_rechts', 'm_gruenschleife'
    ],defaults=[None] * 19)
llps[STATUS_TUEREN] = (
    # Grunddaten
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x66), None, BasicNode),
    LLP(PID(2, 0x0a, 0x66, 0x01),'bauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x66, 0x02),'links', ContentType.BYTE, TUEREN_SEITE),
    LLP(PID(2, 0x0a, 0x66, 0x03),'rechts', ContentType.BYTE, TUEREN_SEITE),
    LLP(PID(2, 0x0a, 0x66, 0x04),'traktionssperre', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x14),'zustand', ContentType.BYTE, TUEREN_ZUSTAND),
    # Seitenselektive Systeme (SAT, TB0, TAV, SST und S-Bahn)
    LLP(PID(2, 0x0a, 0x66, 0x05), 'seitenwahl', ContentType.BYTE, TUEREN_SEITENWAHL),
    LLP(PID(2, 0x0a, 0x66, 0x06), 'm_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x07), 'm_rechts', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x08), 'lm_links', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66, 0x09), 'lm_rechts', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66, 0x0a), 'm_zwnagsschliessen', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x0b), 'lm_zwangsschliessen', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66, 0x0c), 'm_rechts_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x0d), 'lm_rechts_links', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66, 0x0e), 'm_zentrales_oeffnen_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x0f), 'm_zentrales_oeffnen_rechts', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x10), 'lm_zentrales_oeffnen_links', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66, 0x11), 'lm_zentrales_oeffnen_rechts', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66, 0x12), 'm_gruenschleife', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 0x13), 'lm_gruenschleife', ContentType.BYTE, LMZUSTAND),
)
msgidx[PID(2, 0x0a, 0x66)] = STATUS_TUEREN

#
# STATUS_FAHRZEUG
# Zusi -> Client
#
class FAHRZEUG_NULLSTELLUNGSZWANG(Enum):
    NICHTS = 0
    NIEDRIGER_HLL_DRUCK = 1
    DYNAMISCHE_BREMSE = 2
    TRAKTIONSSPERRE = 3
class FAHRZEUG_TRAKTIONSSPERRE(Enum):
    NICHTS = 0
    FEDERSPEICHERBREMSE = 1
    TUERSYSTEM = 2
    BREMSPROBE_LAUFT = 3
    SIFA_ASUGESCHALTET = 4
class FAHRZEUG_SCHALTERSTATUS(Enum):
    UNBEKANNT = 0
    DEAKTIVIERT = 1
    NORMALZUSTAND = 2
class FAHRZEUG_SANDER(Enum):
    INAKTIV = 1
    AKTIV = 2
class FAHRZEUG_BREMSPROBEZUSTAND(Enum):
    NORMALBETRIEB = 0
    AKTIV = 1
STATUS_FAHRZEUG = namedtuple("STATUS_FAHRZEUG", ['grund_nullstellungszwang', 'grund_traktionssperre', 'status_fahrschalter', 'status_dynamische_bremse', 'sanderzustand', 'bremsprobezustand', 'stellung_richtungsschalter'],defaults=[None] * 7)
llps[STATUS_FAHRZEUG] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8d), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8d,0x01), 'grund_nullstellungszwang', ContentType.WORD, FAHRZEUG_NULLSTELLUNGSZWANG),
    LLP(PID(2, 0x0a, 0x8d,0x02), 'grund_traktionssperre', ContentType.WORD, FAHRZEUG_TRAKTIONSSPERRE),
    LLP(PID(2, 0x0a, 0x8d,0x03), 'status_fahrschalter', ContentType.BYTE, FAHRZEUG_SCHALTERSTATUS),
    LLP(PID(2, 0x0a, 0x8d,0x04), 'status_dynamische_bremse', ContentType.BYTE, FAHRZEUG_SCHALTERSTATUS),
    LLP(PID(2, 0x0a, 0x8d,0x06), 'sanderzustand', ContentType.BYTE, FAHRZEUG_SANDER),
    LLP(PID(2, 0x0a, 0x8d,0x07), 'bremsprobezustand', ContentType.WORD, FAHRZEUG_BREMSPROBEZUSTAND),
    LLP(PID(2, 0x0a, 0x8d,0x08), 'stellung_richtungsschalter', ContentType.WORD)
)
msgidx[PID(2, 0x0a, 0x8d)] = STATUS_FAHRZEUG

#
# STATUS_ZUGVERBAND
# Zusi -> Client
class ZV_BREMSART(Enum):
    KEINE = 0
    G = 1
    P = 2
    P_MG = 3
    R = 4
    R_MG = 5
    BREMSE_AUS = 6
    H = 7
    E = 8
    E160 = 9
class ZV_TRAKTIONSMODUS(Enum):
    EIGENER_TF = 0
    MEHRFACHTRAKTION = 1
    KALT = 2
class ZV_DREHUNG_FZ(Enum):
    FZ_NICHT_GEDREHT = 0
    FZ_GEDREHT = 1
class ZV_FUEHRERSTAND(Enum):
    EINE_DATEI_FUER_BEIDE_RICHTUNGEN = 0
    FZ_HAT_KEINEN_FUEHRERSATAND = 1
    NUR_VORWAERTS = 1
    SPERATE_DATEIEN = 3
class ZV_BREMSBAUART(Enum):
    UNDEFINIERT = 0
    SCHEIBENBREMSE = 1
    GRAUGUSS = 2
    K_BREMSSOHLE = 3
    LL_BREMSSOHLE = 4
    MATROSSOW_BREMSE = 5
class ZV_BATTERIEHAUPTSCHALTER(Enum):
    DREHTATSTER = 0
    KEINER = 1
    HEBELL = 2
    DRUCKTASTER = 3
class ZV_STROMABNEHMERWAHLSCHALTER(Enum):
    KEINER = 0
    DREHSCHALTER = 1
    LUFTABSPERRHAN = 2
class ZV_BREMSSTELLUNG(Enum):
    NICHT_WIRKSAM = 0
    WIRKSAM = 1
class ZV_FAHRZEUG_VERBUND(Enum):
    EIGENSTAENDIG = 0
    FAHRZEUGTEIL_OHNE_FAHRZEUGSTATUS = 1
class ZV_LOKSTATUS(Enum):
    UNBEKANNT = 0
    FZ_IST_LOK = 1
    FZ_IST_KEINE_LOK = 2
class ZV_TUERSCHALTER(Enum):
    KEINER = 0
    DREHTASTER = 1
class ZV_ANTRIEBSTYP(Enum):
    UNBESTIMMT = 0
    EINFACHES_ANTRIEBSMODELL = 1
    DIESEL_ELEKTRISCH_DREHSTROM = 2
    DIESEL_ELEKTRISCH_GLEICHSTROM  = 3
    DIESEL_HYDRAULISCH = 4
    DIESEL_MECHANISCH = 5
    ELEKTRISCH_DREHSTROM = 6
    ELEKTRISCH_REIHENSCHLUSS = 7
class ZV_STROMTYP(Enum):
    OHNE = 0
    UNBESTIMMT = 1
    _15KV_16HZ = 2
    _25KV_50HZ = 3
    _1500VDC = 4
    _1200VDC_STROMSCHIENE_HAMBURG = 5
    _3KVDC = 6
    _750VDC_STROMSCHIENE_BERLIN =7
class ZV_BREMSTYP(Enum):
    UNBESTIMMT = 0
    ELEKTRISCH_DREHSTROM = 1
    ELEKTRISCH_REIHENSCHLUSS = 2
    RETARDER = 3
class ZV_AKTIV(Enum):
    AKTIV = 0
    NICHT_AKIV = 1
class ZV_LASTABHAENIGE_BREMSE(Enum):
    AUTOMAITSCHE_LASTABREMSUNG = 0
    KEINE_AUTOMATISCHE_LASTABREMSUNG = 1
class ZV_ZUGTYP(Enum):
    GUETERZUG = 0
    REISEZUG = 1
STATUS_ZUGVERBAND = namedtuple("STATUS_ZUGVERBAND",['fz_dateiname', 'beschreibung', 'vorgabe_bremsstellung', 'bauart_zugbeeinflussungssystem', 'fz_vmax', 'baureihe', 'farbgebung', 'traktionsmodus', 'stromabnehmerschaltung', 'maximaler_bremszylinder_druck', 'nvr_nr', 'sitzplaetze_1_klasse', 'sitzplaetze_2_klasse', 'fz_drehung', 'fz_gattung', 'fuehrerstandsmodus', 'fz_laenge', 'fz_masse', 'ladungsmasse', 'bremsbauart', 'bremsmasse_handbremse', 'aktive_bremsmasse', 'aktive_bremssmasse_inkl_dynamische', 'anzahl_achsen', 'bauart_batteriehauptschalter', 'bauart_stromabnehmerwahlschalter', 'bremsstellung', 'zugehoerige_bremsmasse', 'bremsstellung_wirksam', 'bezeichnung_bremsbauart', 'grafik_seitenansicht', 'hbl', 'fz_verbund', 'lokstatus', 'interne_fz_nr', 'gefahrgutkenzeichen', 'bauart_tuersystem', 'bauart_tuerwachlschalter', 'antriebstyp', 'stromtyp_antriebssystem', 'antrieb_aktiv', 'bremstyp', 'stromtyp_bremse', 'bremse_aktiv', 'lastabhaehnige_bremse', 'zugtyp'],defaults=[None] * 46)
llps[STATUS_ZUGVERBAND] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x01), 'fz_dateiname', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x02), 'beschreibung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x03), 'vorgabe_bremsstellung', ContentType.WORD, ZV_BREMSART),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x04), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x04, 0x01), 'bauart_zugbeeinflussungssystem', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x05), 'fz_vmax', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x06), 'baureihe', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x07), 'farbgebung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x08), 'traktionsmodus', ContentType.BYTE, ZV_TRAKTIONSMODUS),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x09), 'stromabnehmerschaltung', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0a), 'maximaler_bremszylinder_druck', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0b), 'nvr_nr', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0c), 'sitzplaetze_1_klasse', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0d), 'sitzplaetze_2_klasse', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0e), 'fz_drehung', ContentType.BYTE, ZV_DREHUNG_FZ),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0f), 'fz_gattung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x10), 'fuehrerstandsmodus', ContentType.BYTE, ZV_FUEHRERSTAND),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x11), 'fz_laenge', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x12), 'fz_masse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x13), 'ladungsmasse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x14), 'bremsbauart', ContentType.BYTE, ZV_BREMSBAUART),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x15), 'bremsmasse_handbremse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x16), 'aktive_bremsmasse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x17), 'aktive_bremssmasse_inkl_dynamische', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x18), 'anzahl_achsen', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x19), 'bauart_batteriehauptschalter', ContentType.BYTE, ZV_BATTERIEHAUPTSCHALTER),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1a), 'bauart_stromabnehmerwahlschalter', ContentType.BYTE, ZV_STROMABNEHMERWAHLSCHALTER),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b, 0x01), 'bremsstellung', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b, 0x02), 'zugehoerige_bremsmasse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b, 0x03), 'bremsstellung_wirksam', ContentType.BYTE, ZV_BREMSSTELLUNG),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1c), 'bezeichnung_bremsbauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1d), 'grafik_seitenansicht', ContentType.FILE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1e), 'hbl', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1f), 'fz_verbund', ContentType.BYTE, ZV_FAHRZEUG_VERBUND),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x20), 'lokstatus', ContentType.BYTE, ZV_LOKSTATUS),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x21), 'interne_fz_nr', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x22), 'gefahrgutkenzeichen', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x23), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x23, 0x01), 'bauart_tuersystem', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x24), 'bauart_tuerwachlschalter', ContentType.BYTE, ZV_TUERSCHALTER),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25, 0x01), 'antriebstyp', ContentType.BYTE, ZV_ANTRIEBSTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25, 0x02), 'stromtyp_antriebssystem', ContentType.BYTE, ZV_STROMTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25, 0x03), 'antrieb_aktiv', ContentType.BYTE, ZV_AKTIV),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26, 0x01), 'bremstyp', ContentType.BYTE, ZV_BREMSTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26, 0x02), 'stromtyp_bremse', ContentType.BYTE, ZV_STROMTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26, 0x03), 'bremse_aktiv', ContentType.BYTE, ZV_AKTIV),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x27), 'lastabhaehnige_bremse', ContentType.BYTE, ZV_LASTABHAENIGE_BREMSE),
    LLP(PID(2, 0x0a, 0x8e, 0x02), 'zugtyp', ContentType.BYTE, ZV_ZUGTYP)
)
msgidx[PID(2, 0x0a, 0x8e)] = STATUS_ZUGVERBAND

#
# STATUS_WEICHEN
# Zusi -> Client
#
class WEICHEN_BAUART(Enum):
    UNDEFINIERT = 0
    HANDWEICHE_RECHTS = 1
    HANDWEICHE_LINKS = 2
    EOW_RECHTS = 3
    EOW_LINKS = 4
    HAND_DKW_GRUNDSTELLUNG_LINKS = 5
    HAND_DKW_GRUNDSTELLUNG_RECHTS = 6
    EOW_DKW_GRUNDSTELLUNG_LINKS = 7
    EOW_DKW_GRUNDSTELLUNG_RECHTS = 8
    HAND_GLEISSPERRE = 9
    EOW_GLEISSPERRE = 10
    HET = 11
    UT = 12
    ZLB = 13
class WEICHEN_TYP(Enum):
    UNDEFINIERT = 0
    OHNE_GRUNDSTELLUNG = 1
    GRUNDSTELLUNG_RECHTS_WEISS = 2
    GRUNDSTELLUNG_LINKS_WEISS = 3
    GRUNDSTELLUNG_RECHTS_gelb = 4
    GRUNDSTELLUNG_LINKS_gelb = 5
class WEICHEN_LAGE(Enum):
    ZUSI_GRUNDSTELLUNG_SPITZ_BEFAHREN = 0
    NICHT_IN_GRUNDSTELLUNG_SPITZ_BEFAHREN = 1
    ZUSI_GRUNDSTELLUNG_STUMPF_BEFAHREN = 2
    NICHT_IN_GRUNDSTELLUNG_STUMPF_BEFAHREN = 3
class WEICHEN_FAHRTRICHTUNG(Enum):
    UNDEFINIERT = 0
    SPITZ_BEFAHREN = 1
    STUMPF_BEFAHREN = 2
class WEICHEN_UMLAUFMODUS_STUMPFBEFAHRUNG(Enum):
    UNDEFINIERT = 0
    WEICHE_LAUEFT_AUTOMATISCH_UM = 1
    WEICHE_MUSS_GESTELLT_WERDEN = 2
STATUS_WEICHEN = namedtuple("STATUS_WEICHEN", ['weichen'], defaults=[None])
STATUS_WEICHEN_WEICHE = namedtuple("STATUS_WEICHEN_WEICHE", ['bezeichnung', 'bauart', 'typ', 'aktuelle_lage', 'fahrtrichtung', 'umlaufmodus'], defaults=[None] * 6)
llps[STATUS_WEICHEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x92), None, BasicNode),
    LLP(PID(2, 0x0a, 0x92, 0x01), 'weichen', BasicNode, multipletimes=STATUS_WEICHEN_WEICHE),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x01), 'bezeichnung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x02), 'bauart', ContentType.INTEGER, WEICHEN_BAUART),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x03), 'typ', ContentType.INTEGER, WEICHEN_TYP),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x04), 'aktuelle_lage', ContentType.BYTE, WEICHEN_LAGE),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x05), 'fahrtrichtung', ContentType.BYTE, WEICHEN_FAHRTRICHTUNG),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x06), 'umlaufmodus', ContentType.BYTE, WEICHEN_UMLAUFMODUS_STUMPFBEFAHRUNG),
)
llps[STATUS_WEICHEN_WEICHE] = llps[STATUS_WEICHEN]
msgidx[PID(2, 0x0a, 0x92,0x01)] = STATUS_WEICHEN

#
# STATUS_LM_ZUSIDISPLAY
# Zusi -> Client
#
class ZUSIDISPLAY_RAHMEN_MODUS(Enum):
    GRAFIK_OHNE_RAHMEN = 0
    GRAFIK_MIT_RAHMEN = 1
    GRAFIK_MIT_TASTEN = 2
STATUS_LM_ZUSIDISPLAY = namedtuple("STATUS_LM_ZUSIDISPLAY", ['displays'], defaults=[None])
STATUS_LM_ZUSIDISPLAY_DISPLAY = namedtuple("STATUS_LM_ZUSIDISPLAY_DISPLAY", ['name', 'modus', 'breite', 'hoehe'], defaults=[None] * 4)
llps[STATUS_LM_ZUSIDISPLAY] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9, 0x01), 'displays', BasicNode, multipletimes=STATUS_LM_ZUSIDISPLAY_DISPLAY),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x01), 'name', ContentType.STRING),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x02), 'modus', ContentType.BYTE, ZUSIDISPLAY_RAHMEN_MODUS),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x03), 'breite', ContentType.WORD),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x04), 'hoehe', ContentType.WORD),
)
llps[STATUS_LM_ZUSIDISPLAY_DISPLAY] = llps[STATUS_LM_ZUSIDISPLAY]
msgidx[PID(2, 0x0a, 0xa9)] = STATUS_LM_ZUSIDISPLAY

#
# STATUS_ZUGFAHRDATEN
# Zusi -> Client
#
class ZUGFAHRDATEN_ABSPERRHAEHNE_HLL(Enum):
    STANDARD = 0
    HAN_VORNE_OFFEN = 1
    HAN_HINTEN_OFFEN = 2
    BEIDE_HAEHNE_OFFEN = 3
    BEIDE_HAEHNE_ZU = 4
    STANDARD_WIEDERHERSTELLEN = 5
STATUS_ZUGFAHRDATEN = namedtuple("STATUS_ZUGFAHRDATEN", ['fahrzeuge'], defaults=[None])
STATUS_ZUGFAHRDATEN_FAHRZEUG = namedtuple("STATUS_ZUGFAHRDATEN_FAHRZEUG",['bremszylinderdruck', 'hll_druck', 'zugkraft', 'motordrehzahl_1', 'maximal_moegliche_zugkraft', 'maximale_dynamische_bremskraft', 'absperrhaehne_hll', 'motordrehzahl_2'],defaults=[None,None,None,None,None,None,None,None])
llps[STATUS_ZUGFAHRDATEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0xab), None, BasicNode),
    LLP(PID(2, 0x0a, 0xab, 0x01), 'fahrzeuge', BasicNode, multipletimes=STATUS_ZUGFAHRDATEN_FAHRZEUG),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x01),'bremszylinderdruck', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x02),'hll_druck',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x03),'zugkraft',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x04),'motordrehzahl_1',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x05),'maximal_moegliche_zugkraft',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x06),'maximale_dynamische_bremskraft',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x07),'absperrhaehne_hll',ContentType.BYTE, ZUGFAHRDATEN_ABSPERRHAEHNE_HLL),
    LLP(PID(2, 0x0a, 0xab, 0x01, 0x0a),'motordrehzahl_2',ContentType.SINGLE),
)
llps[STATUS_ZUGFAHRDATEN_FAHRZEUG] = llps[STATUS_ZUGFAHRDATEN]
msgidx[PID(2, 0x0a, 0xab)] = STATUS_ZUGFAHRDATEN

#
# DATA_OPERATION
# Zusi -> Client
#
class DATAOPS_TASTATURZUORDNUNG(AutoNumber):
    KEINE = ()
    FAHRSCHALTER = ()
    DYNAMISCHE_BREMSE = ()
    AFB_TEMPOMAT = ()
    FUEHRERBREMSVENTIL = ()
    ZUSATZBREMSVENTIL = ()
    GANG = ()
    RICHTUNGSSCHALTER = ()
    STUFENSCHALTER = ()
    SANDER = ()
    TUEREN = ()
    LICHT = ()
    PFEIFE = ()
    GLOCKE = ()
    LUEFTER = ()
    ZUGBEEINFLUSSUNG = ()
    SIFA = ()
    HAUPTSCHALTER = ()
    GRUPPENSCHALTER = ()
    SCHLEUDERSCHUTZ = ()
    MG_BREMSE = ()
    LOKBREMSE_ENTLUEFTEN = ()
    FAHRPULTINTERN_01 = ()
    FAHRPULTINTERN_02 = ()
    FAHRPULTINTERN_03 = ()
    FAHRPULTINTERN_04 = ()
    FAHRPULTINTERN_05 = ()
    FAHRPULTINTERN_06 = ()
    FAHRPULTINTERN_07 = ()
    FAHRPULTINTERN_08 = ()
    FAHRPULTINTERN_09 = ()
    FAHRPULTINTERN_10 = ()
    FAHRPULTINTERN_11 = ()
    FAHRPULTINTERN_12 = ()
    FAHRPULTINTERN_13 = ()
    FAHRPULTINTERN_14 = ()
    FAHRPULTINTERN_15 = ()
    FAHRPULTINTERN_16 = ()
    FAHRPULTINTERN_17 = ()
    FAHRPULTINTERN_18 = ()
    FAHRPULTINTERN_19 = ()
    FAHRPULTINTERN_20 = ()
    PROGRAMMSTEUERNG = ()
    STROMABNEHMER = ()
    FUEHRERSTANDSSICHT = ()
    LUFTPRESSER_AUS = ()
    ZUGFUNK = ()
    LZB = ()
    FAHRPULTINTERN_21 = ()
    FAHRPULTINTERN_22 = ()
    FAHRPULTINTERN_23 = ()
    FAHRPULTINTERN_24 = ()
    FAHRPULTINTERN_25 = ()
    FAHRPULTINTERN_26 = ()
    FAHRPULTINTERN_27 = ()
    FAHRPULTINTERN_28 = ()
    FAHRPULTINTERN_29 = ()
    FAHRPULTINTERN_30 = ()
    FAHRPULTINTERN_31 = ()
    FAHRPULTINTERN_32 = ()
    FAHRPULTINTERN_33 = ()
    FAHRPULTINTERN_34 = ()
    FAHRPULTINTERN_35 = ()
    FAHRPULTINTERN_36 = ()
    FAHRPULTINTERN_37 = ()
    FAHRPULTINTERN_38 = ()
    FAHRPULTINTERN_39 = ()
    FAHRPULTINTERN_40 = ()
    NOTAUS = ()
    FEDERSPEICHERBREMSE = ()
    BATTERIEHAUPTSCHALTER_AUS = ()
    NOTBREMSUEBERBRUECKUNG = ()
    BREMSPROBEFUNKTION = ()
    LEISTUNG_AUS = ()
    FAHRZEUGINTERN_01 = ()
    FAHRZEUGINTERN_02 = ()
    FAHRZEUGINTERN_03 = ()
    FAHRZEUGINTERN_04 = ()
    FAHRZEUGINTERN_05 = ()
    FAHRZEUGINTERN_06 = ()
    FAHRZEUGINTERN_07 = ()
    FAHRZEUGINTERN_08 = ()
    FAHRZEUGINTERN_09 = ()
    FAHRZEUGINTERN_10 = ()
    FAHRZEUGINTERN_11 = ()
    FAHRZEUGINTERN_12 = ()
    FAHRZEUGINTERN_13 = ()
    FAHRZEUGINTERN_14 = ()
    FAHRZEUGINTERN_15 = ()
    FAHRZEUGINTERN_16 = ()
    FAHRZEUGINTERN_17 = ()
    FAHRZEUGINTERN_18 = ()
    FAHRZEUGINTERN_19 = ()
    FAHRZEUGINTERN_20 = ()
    FUEHRERTISCH_DEAKTIVIEREN = ()
class DATAOPS_TASTATURKOMMANDO(AutoNumber):
    """Aus Doku übernommen"""
    Unbestimmt = ()
    FahrschalterAuf_Down = ()
    FahrschalterAuf_Up = ()
    FahrschalterAb_Down = ()
    FahrschalterAb_Up = ()
    FahrschalterGrundstellung = ()
    FahrschalterEinAus_Down = ()
    FahrschalterEinAus_Up = ()
    DynBremseAuf_Down = ()
    DynBremseAuf_Up = ()
    DynBremseAb_Down = ()
    DynBremseAb_Up = ()
    DynBremseGrundstellung = ()
    DynBremseEinAus_Down = ()
    DynBremseEinAus_Up = ()
    AFBAuf_Down = ()
    AFBAuf_Up = ()
    AFBAb_Down = ()
    AFBAb_Up = ()
    AFBGrundstellung = ()
    AFBEinAus_Down = ()
    AFBEinAus_Up = ()
    GangAuf_Down = ()
    GangAuf_Up = ()
    GangAb_Down = ()
    GangAb_Up = ()
    GangGrundstellung = ()
    FbvAuf_Down = ()
    FbvAuf_Up = ()
    FbvAb_Down = ()
    FbvAb_Up = ()
    Angleicher_Down = ()
    Angleicher_Up = ()
    ZbvAuf_Down = ()
    ZbvAuf_Up = ()
    ZbvAb_Down = ()
    ZbvAb_Up = ()
    Mg_Down = ()
    Mg_Up = ()
    RischaAuf_Down = ()
    RischaAuf_Up = ()
    RischaAb_Down = ()
    RischaAb_Up = ()
    StufenschalterAuf_Down = ()
    StufenschalterAuf_up = ()
    StufenschalterAb_Down = ()
    StufenschalterAb_Up = ()
    Sand_Down = ()
    Sand_Up = ()
    Schleuderschutz_Down = ()
    Schleuderschutz_Up = ()
    PZBWachsam_Down = ()
    PZBWachsam_Up = ()
    PZBFrei_Down = ()
    PZBFrei_Up = ()
    PZBBefehl_Down = ()
    PZBBefehl_Up = ()
    Sifa_Down = ()
    Sifa_Up = ()
    TuerenTaster_Down = ()
    TuerenTaster_Up = ()
    TuerenLi_Down = ()
    TuerenLi_Up = ()
    TuerenRe_Down = ()
    TuerenRe_Up = ()
    TuerenZu_Down = ()
    TuerenZu_Up = ()
    Licht_Down = ()
    Licht_Up = ()
    Pfeife_Down = ()
    Pfeife_Up = ()
    Glocke_Down = ()
    Glocke_Up = ()
    Luefter_Down = ()
    Luefter_Up = ()
    MotorAuf_Down = ()
    MotorAuf_Up = ()
    MotorAb_Down = ()
    MotorAb_Up = ()
    HauptschalterEin_Down = ()
    HauptschalterEin_Up = ()
    HauptschalterAus_Down = ()
    HauptschalterAus_Up = ()
    SAAuf_Down = ()
    SAAuf_Up = ()
    SAAb_Down = ()
    SAAb_Up = ()
    Fst1_Down = ()
    Fst1_Up = ()
    Fst2_Down = ()
    Fst2_Up = ()
    Fst3_Down = ()
    Fst3_Up = ()
    Fst4_Down = ()
    Fst4_Up = ()
    LuftpresserAus_Down = ()
    LuftpresserAus_Up = ()
    FunkGabel_Down = ()
    FunkGabel_Up = ()
    FunkSprechknopf_Down = ()
    FunkSprechknopf_Up = ()
    LZB_G_Down = ()
    LZB_G_Up = ()
    LZB_Stoer_Down = ()
    LZB_Stoer_Up = ()
    LZB_Nothalt_Down = ()
    LZB_Nothalt_Up = ()
    Nothalt_Down = ()
    Nothalt_Up = ()
    FederspeicherAuf_Down = ()
    FederspeicherAuf_Up = ()
    FederspeicherAb_Down = ()
    FederspeicherAb_Up = ()
    BatterieHSAusAuf_Down = ()
    BatterieHSAusAuf_Up = ()
    BatterieHSAusAb_Down = ()
    BatterieHSAusAb_Up = ()
    NBUeAus_Down = ()
    NBUeAus_Up = ()
    NBUeQuittierung_Down = ()
    NBUeQuittierung_Up = ()
    NBUeTest_Down = ()
    NBUeTest_Up = ()
    Bremsprobe_Down = ()
    Bremsprobe_Up = ()
    LeistungAus_Down = ()
    LeistungAus_Up = ()
    ETCSQuittieren_Down = ()
    ETCSQuittieren_Up = ()
    TischAuf_Down = ()
    TischAuf_Up = ()
    TischAus_Down = ()
    TischAus_Up = ()
    SifaPruefmodus_Down = ()
    SifaPruefmodus_Up = ()
    SifaFusspedal_Down = ()
    SifaFusspedal_Up = ()
class DATAOPS_TASTATURAKTION(AutoNumber):
    Default = ()
    Down = ()
    Up = ()
    Auf_Down = ()
    Auf_Up = ()
    Ab_Down = ()
    Ab_Up = ()
    Absolut = ()
    Absolut1000er = ()
class DATAOPS_SCHALTERFUNKTION(AutoNumber):
    NICHTS = ()
    FAHRSTUFE = ()
    FAHRSTUFE_SCHNELLAUS = ()
    FAHRSTUFE_AUFSCHALTEN = ()
    FAHRSTUFE_KONSTANT = ()
    FAHRSTUFE_ABSCHALTEN = ()
    DYN_BREMSE_STUFE = ()
    DYN_BREMSE_0 = ()
    DYN_BREMSE_AUFSCHALTEN = ()
    DYN_BREMSE_KONSTANT = ()
    DYN_BREMSE_ABSCHALTEN = ()
    AFB = ()
    AFB_0 = ()
    AFB_AUF = ()
    AFB_AB = ()
    AFB_EIN_AUS = ()
    ZUGKRAFT_ABSOLUT = ()
    ZUGKRAFT_SCHNELLAUS = ()
    ZUGKRAFT_AUFSCHALTEN = ()
    ZUGKRAFT_KONSTANT = ()
    ZUGKRAFT_ABSCHALTEN = ()
    HLL_FUELLEN = ()
    HLL_FESTE_STUFE = ()
    HLL_ABSCHLUSS = ()
    HLL_MITTEL = ()
    HLL_SCHNELLBREMSUNG = ()
    ANGLEICHER = ()
    ZBV_LOESEN = ()
    ZBV_MITTEL = ()
    ZBV_BREMSEN = ()
    GANGWAHL = ()
    GANGWAHL_0 = ()
    GANGWAHL_AUF = ()
    GANGWAHL_FAHREN = ()
    GANGWAHL_AB = ()
    RICHTUNGSSCHALTER_V = ()
    RICHTUNGSSCHALTER_M = ()
    RICHTUNGSSCHALTER_0 = ()
    RICHTUNGSSCHALTER_R = ()
    STUFENSCHALTER_LG = ()
    STUFENSCHALTER_0 = ()
    STUFENSCHALTER_SG = ()
    GRUPPENSCHALTER_STOP = ()
    GRUPPENSCHALTER_AUS = ()
    GRUPPENSCHALTER_EIN = ()
    GRUPPENSCHALTER_START = ()
    STROMABNEHMER_AB = ()
    STROMABNEHMER_MITTE = ()
    STROMABNEHMER_AUF = ()
    HAUPTSCHALTER_AUS = ()
    HAUPTSCHALTER_MITTE = ()
    HAUPTSCHALTER_EIN = ()
    MG_BREMSE = ()
    SANDEN = ()
    UNBENUTZT_01 = ()
    UNBENUTZT_02 = ()
    LOKBREMSE_ENTLUEFTEN = ()
    LUEFTER = ()
    FAHRPULTINTERN_01 = ()
    FAHRPULTINTERN_02 = ()
    FAHRPULTINTERN_03 = ()
    FAHRPULTINTERN_04 = ()
    FAHRPULTINTERN_05 = ()
    FAHRPULTINTERN_06 = ()
    FAHRPULTINTERN_07 = ()
    FAHRPULTINTERN_08 = ()
    FAHRPULTINTERN_09 = ()
    FAHRPULTINTERN_10 = ()
    FAHRPULTINTERN_11 = ()
    FAHRPULTINTERN_12 = ()
    FAHRPULTINTERN_13 = ()
    FAHRPULTINTERN_14 = ()
    FAHRPULTINTERN_15 = ()
    FAHRPULTINTERN_16 = ()
    FAHRPULTINTERN_17 = ()
    FAHRPULTINTERN_18 = ()
    FAHRPULTINTERN_19 = ()
    FAHRPULTINTERN_20 = ()
    WANDLERFUELLUNG = ()
    LUFTPRESSER_AUS = ()
    NOTAUS = ()
    FAHRPULTINTERN_21 = ()
    FAHRPULTINTERN_22 = ()
    FAHRPULTINTERN_23 = ()
    FAHRPULTINTERN_24 = ()
    FAHRPULTINTERN_25 = ()
    FAHRPULTINTERN_26 = ()
    FAHRPULTINTERN_27 = ()
    FAHRPULTINTERN_28 = ()
    FAHRPULTINTERN_29 = ()
    FAHRPULTINTERN_30 = ()
    FAHRPULTINTERN_31 = ()
    FAHRPULTINTERN_32 = ()
    FAHRPULTINTERN_33 = ()
    FAHRPULTINTERN_34 = ()
    FAHRPULTINTERN_35 = ()
    FAHRPULTINTERN_36 = ()
    FAHRPULTINTERN_37 = ()
    FAHRPULTINTERN_38 = ()
    FAHRPULTINTERN_39 = ()
    FAHRPULTINTERN_40 = ()
    FEDERSPEICHER_ANLEGEN = ()
    FEDERSPEICHER_MITTE = ()
    FEDERSPEICHER_LOESEN = ()
    FEDERSPEICHER_UMSCHALTEN = ()
    BATTERIEHAUPTSCHALTER_AUS = ()
    BATTERIEHAUPTSCHALTER_MITTE = ()
    BATTERIEHAUPTSCHALTER_EIN = ()
    FAHRSCHALTER_DEAKTIVIEREN = ()
    DYNAMISCHE_BREMSE_DEAKTIVIEREN = ()
    COMPUTERBREMSE_BREMSKRAFT = ()
    COMPUTERBREMSE_AUFSCHALTEN = ()
    COMPUTERBREMSE_KONSTANT = ()
    COMPUTERBREMSE_ABSCHALTEN = ()
    FAHRZEUGINTERN_01 = ()
    FAHRZEUGINTERN_02 = ()
    FAHRZEUGINTERN_03 = ()
    FAHRZEUGINTERN_04 = ()
    FAHRZEUGINTERN_05 = ()
    FAHRZEUGINTERN_06 = ()
    FAHRZEUGINTERN_07 = ()
    FAHRZEUGINTERN_08 = ()
    FAHRZEUGINTERN_09 = ()
    FAHRZEUGINTERN_10 = ()
    FAHRZEUGINTERN_11 = ()
    FAHRZEUGINTERN_12 = ()
    FAHRZEUGINTERN_13 = ()
    FAHRZEUGINTERN_14 = ()
    FAHRZEUGINTERN_15 = ()
    FAHRZEUGINTERN_16 = ()
    FAHRZEUGINTERN_17 = ()
    FAHRZEUGINTERN_18 = ()
    FAHRZEUGINTERN_19 = ()
    FAHRZEUGINTERN_20 = ()
    FUEHRERTISCH_DEAKTIVIERT = ()
class DATAOPS_MAUSKLICK(Enum):
    ANFANG = 0
    ENDE = 1
DATA_OPERATION = namedtuple("DATA_OPERATION", ['betaetigungen', 'kombischalter', 'mausklicks'], defaults=[None] * 3)
DATA_OPERATION_BETAETIGUNG = namedtuple("DATA_OPERATION_BETAETIGUNG", ['zuordnung', 'kommando', 'aktion', 'schalterposition', 'sonderfunktion'], defaults=[None] * 5)
DATA_OPERATION_KOMBISCHALTER = namedtuple("DATA_OPERATION_KOMBISCHALTER", ['name', 'schalterfunktionen', 'aktuelle_raste', 'mittelstellung', 'maximalstellung'], defaults=[None] * 5)
DATA_OPERATION_SCHALTERFUNKTION = namedtuple("DATA_OPERATION_SCHALTERFUNKTION", ['funktion', 'parameter'], defaults=[None] * 2)
DATA_OPERATION_MAUSKLICK = namedtuple("DATA_OPERATION_MAUSKLICK", ['meldername', 'klickstatus', 'x', 'y'], defaults=[None] * 4)
llps[DATA_OPERATION] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0b), None, BasicNode),
    LLP(PID(2, 0x0b, 1), 'betaetigungen', BasicNode, multipletimes=DATA_OPERATION_BETAETIGUNG),
    LLP(PID(2, 0x0b, 1, 1), 'zuordnung', ContentType.WORD, DATAOPS_TASTATURZUORDNUNG),
    LLP(PID(2, 0x0b, 1, 2), 'kommando', ContentType.WORD, DATAOPS_TASTATURKOMMANDO),
    LLP(PID(2, 0x0b, 1, 3), 'aktion', ContentType.WORD, DATAOPS_TASTATURAKTION),
    LLP(PID(2, 0x0b, 1, 4), 'schalterposition', ContentType.SMALLINT),
    LLP(PID(2, 0x0b, 1, 5), 'sonderfunktion', ContentType.SINGLE),
    LLP(PID(2, 0x0b, 2), 'kombischalter', BasicNode, multipletimes=DATA_OPERATION_KOMBISCHALTER),
    LLP(PID(2, 0x0b, 2, 1), 'name', ContentType.STRING),
    LLP(PID(2, 0x0b, 2, 2), 'schalterfunktionen', BasicNode, multipletimes=DATA_OPERATION_SCHALTERFUNKTION),
    LLP(PID(2, 0x0b, 2, 2, 1), 'funktion', ContentType.WORD, DATAOPS_SCHALTERFUNKTION),
    LLP(PID(2, 0x0b, 2, 2, 2), 'parameter', ContentType.SINGLE),
    LLP(PID(2, 0x0b, 2, 3), 'aktuelle_raste', ContentType.SMALLINT),
    LLP(PID(2, 0x0b, 2, 4), 'mittelstellung', ContentType.SMALLINT),
    LLP(PID(2, 0x0b, 2, 5), 'maximalstellung', ContentType.SMALLINT),
    LLP(PID(2, 0x0b, 3), 'mausklicks', BasicNode, multipletimes=DATA_OPERATION_MAUSKLICK),
    LLP(PID(2, 0x0b, 3, 1), 'meldername', ContentType.STRING),
    LLP(PID(2, 0x0b, 3, 2), 'klickstatus', ContentType.BYTE, DATAOPS_MAUSKLICK),
    LLP(PID(2, 0x0b, 3, 3), 'x', ContentType.SINGLE),
    LLP(PID(2, 0x0b, 3, 4), 'y', ContentType.SINGLE),
)
llps[DATA_OPERATION_BETAETIGUNG] = llps[DATA_OPERATION]
llps[DATA_OPERATION_KOMBISCHALTER] = llps[DATA_OPERATION]
llps[DATA_OPERATION_SCHALTERFUNKTION] = llps[DATA_OPERATION]
llps[DATA_OPERATION_MAUSKLICK] = llps[DATA_OPERATION]
msgidx[PID(2, 0x0b)] = DATA_OPERATION

#
# DATA_PROG
# Zusi -> Client
#
DATA_PROG = namedtuple("DATA_PROG", ['zugdateiname', 'zugnummer', 'ladepause', 'buchfahrplanxml', 'zuggeladen', 'buchfahrplantiff', 'buchfahrplanpdf', 'bremszettelpdf', 'wagenlistepdf', 'lapdf', 'streckenbuchpdf', 'ersatzfahrplanpdf'], defaults=[None] * 12)
llps[DATA_PROG] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0c), None, BasicNode),
    LLP(PID(2, 0x0c, 1), 'zugdateiname', ContentType.STRING),
    LLP(PID(2, 0x0c, 2), 'zugnummer', ContentType.STRING),
    LLP(PID(2, 0x0c, 3), 'ladepause', ContentType.BYTE),
    LLP(PID(2, 0x0c, 4), 'buchfahrplanxml', ContentType.FILE),
    LLP(PID(2, 0x0c, 5), 'zuggeladen', ContentType.BYTE),
    LLP(PID(2, 0x0c, 6), 'buchfahrplantiff', ContentType.FILE),
    LLP(PID(2, 0x0c, 7), 'buchfahrplanpdf', ContentType.FILE),
    LLP(PID(2, 0x0c, 8), 'bremszettelpdf', ContentType.FILE),
    LLP(PID(2, 0x0c, 9), 'wagenlistepdf', ContentType.FILE),
    LLP(PID(2, 0x0c, 0x0a), 'lapdf', ContentType.FILE),
    LLP(PID(2, 0x0c, 0x0b), 'streckenbuchpdf', ContentType.FILE),
    LLP(PID(2, 0x0c, 0x0c), 'ersatzfahrplanpdf', ContentType.FILE),
)
msgidx[PID(2, 0x0c)] = DATA_PROG

#
# INPUT
# Client -> Zusi
#
INPUT = namedtuple("INPUT", [
    'tastatur_zuordnung', 'tastatur_kommando', 'tastatur_aktion', 'tastatur_schalterposition', 'tastatur_sonderfunktion',
    'indusi_zugart', 'indusi_hauptschalter', 'indusi_stoerschalter', 'indusi_luftabsperrhahn', 'indusi_systemstatus', 'indusi_bauart', 'indusi_tfnr', 'indusi_zugnummer', 'indusi_e_brh', 'indusi_e_bra', 'indusi_e_zugart', 'indusi_a_brh', 'indusi_a_bra', 'indusi_a_zugart', 'indusi_a_modus', 'indusi_klartextmeldungen', 'indusi_funktionspruefung_starten', 'indusi_stoerschalterbauart',
    'lzb_g_brh', 'lzb_g_bra', 'lzb_g_zl', 'lzb_g_vmz', 'lzb_g_zugart', 'lzb_e_zl', 'lzb_e_vmz', 'lzb_a_zl', 'lzb_a_vmz', 'lzb_stoerschalter', 'lzb_stoerschalterbaurt', 'lzb_systemstatus',
    'fahrsp_stoerschalter', 'fahrsp_hauptschalter', 'fahrsp_systemstatus', 'fahrsp_bauart', 'fahrsp_zugneustart',
    'zugfunk_notruf',
    'sifa_hauptschalter', 'sifa_stoerschalter', 'sifa_lufthahn', 'sifa_weglaengenmesser_aktivieren',
    'bremsprobe',
    'bremse_fernsteuerung_aktivieren', 'bremse_druck_hll', 'bremse_druck_bremszylinder',
    'weiche_statusabfrage', 'weiche_bezeichnung', 'weiche_stellung',
    'tempomat_sollwert',
    'stromabnehmer_fahrzeugnr', 'stromabnehmer_bitmuster', 'stromabnehmer_absperrhaehne',
    'bremsstellung_fahrzeugnr', 'bremsstellung_stellung', 'bremsstellung_indirektebremse', 'bremsstellung_absperrhahn',
    'pdf_bremszettel', 'pdf_wagenliste', 'pdf_la', 'pdf_streckenbuch', 'pdf_ersatzfahrplan',
    'tueren_status',
    'antrieb_deaktivieren', 'antrieb_aktivieren',
    'dyn_bremse_deaktivieren', 'dyn_bremse_aktivieren',
    'zbs_deaktivieren', 'zbs_aktivieren'
], defaults=[None] * 72)
llps[INPUT] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x010a), None, BasicNode),
    # Tastatureingaben
    LLP(PID(2, 0x010a, 1), None, BasicNode),
    LLP(PID(2, 0x010a, 1, 1), 'tastatur_zuordnung', ContentType.WORD, DATAOPS_TASTATURZUORDNUNG),
    LLP(PID(2, 0x010a, 1, 2), 'tastatur_kommando', ContentType.WORD, DATAOPS_TASTATURKOMMANDO),
    LLP(PID(2, 0x010a, 1, 3), 'tastatur_aktion', ContentType.WORD, DATAOPS_TASTATURAKTION),
    LLP(PID(2, 0x010a, 1, 4), 'tastatur_schalterposition', ContentType.SMALLINT),
    LLP(PID(2, 0x010a, 1, 5), 'tastatur_sonderfunktion', ContentType.SINGLE),
    # Indusi Analogsysteme und Basisdaten
    LLP(PID(2, 0x010a, 2), None, BasicNode),
    LLP(PID(2, 0x010a, 2, 2), None, BasicNode),
    LLP(PID(2, 0x010a, 2, 2, 1), 'indusi_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x010a, 2, 2, 7), 'indusi_hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 2, 2, 8), 'indusi_stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 2, 2, 0x0a), 'indusi_luftabsperrhahn', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 2, 2, 0x0d), 'indusi_systemstatus', ContentType.BYTE, INDUSI_SYSTEMSTATUS),
    LLP(PID(2, 0x010a, 2, 2, 0x0e), 'indusi_bauart', ContentType.STRING),
    # Indusi I60R/I80/PZB90
    LLP(PID(2, 0x010a, 2, 2, 2), 'indusi_tfnr', ContentType.STRING),
    LLP(PID(2, 0x010a, 2, 2, 3), 'indusi_zugnummer', ContentType.STRING),
    LLP(PID(2, 0x010a, 2, 2, 5), None, BasicNode),
    LLP(PID(2, 0x010a, 2, 2, 5, 1), 'indusi_e_brh', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 5, 2), 'indusi_e_bra', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 5, 5), 'indusi_e_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x010a, 2, 2, 6), None, BasicNode),
    LLP(PID(2, 0x010a, 2, 2, 6, 1), 'indusi_a_brh', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 6, 2), 'indusi_a_bra', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 6, 5), 'indusi_a_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x010a, 2, 2, 6, 6), 'indusi_a_modus', ContentType.BYTE, INDUSI_MODUS),
    LLP(PID(2, 0x010a, 2, 2, 0x0b), 'indusi_klartextmeldungen', ContentType.BYTE, INDUSI_KLARTEXTMELDUNGEN),
    LLP(PID(2, 0x010a, 2, 2, 0x0c), 'indusi_funktionspruefung_starten', ContentType.BYTE, INDUSI_FUNKTIONSPRUEFUNG_STARTEN),
    LLP(PID(2, 0x010a, 2, 2, 0x0f), 'indusi_stoerschalterbauart', ContentType.BYTE, INDUSI_STOERSCHALTERBAURT),
    # LZB
    LLP(PID(2, 0x010a, 2, 2, 4), None, BasicNode),
    LLP(PID(2, 0x010a, 2, 2, 4, 1), 'lzb_g_brh', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 4, 2), 'lzb_g_bra', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 4, 3), 'lzb_g_zl', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 4, 4), 'lzb_g_vmz', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 4, 5), 'lzb_g_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x010a, 2, 2, 5, 3), 'lzb_e_zl', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 5, 4), 'lzb_e_vmz', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 6, 3), 'lzb_a_zl', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 6, 4), 'lzb_a_vmz', ContentType.WORD),
    LLP(PID(2, 0x010a, 2, 2, 9), 'lzb_stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 2, 2, 0x10), 'lzb_stoerschalterbaurt', ContentType.BYTE, INDUSI_STOERSCHALTERBAURT),
    LLP(PID(2, 0x010a, 2, 2, 0x11), 'lzb_systemstatus', ContentType.BYTE, INDUSI_SYSTEMSTATUS),
    # ETCS
    # FIXME Platzhalter
    # ZBS
    # FIXME Platzhalter
    # Fahrsperre
    LLP(PID(2, 0x010a, 2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x010a, 2, 0x0a, 1), 'fahrsp_stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 2, 0x0a, 2), 'fahrsp_hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 2, 0x0a, 3), 'fahrsp_systemstatus', ContentType.BYTE, INDUSI_SYSTEMSTATUS),
    LLP(PID(2, 0x010a, 2, 0x0a, 4), 'fahrsp_bauart', ContentType.STRING),
    LLP(PID(2, 0x010a, 2, 0x0a, 8), 'fahrsp_zugneustart', ContentType.STRING),
    # Zugfunk
    LLP(PID(2, 0x010a, 3), None, BasicNode),
    LLP(PID(2, 0x010a, 3, 1), 'zugfunk_notruf', ContentType.BYTE),
    # Sifa
    LLP(PID(2, 0x010a, 4), None, BasicNode),
    LLP(PID(2, 0x010a, 4, 1), 'sifa_hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 4, 2), 'sifa_stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 4, 3), 'sifa_lufthahn', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x010a, 4, 4), 'sifa_weglaengenmesser_aktivieren', ContentType.BYTE),
    # Bremsprobe
    LLP(PID(2, 0x010a, 7), None, BasicNode),
    LLP(PID(2, 0x010a, 7, 1), 'bremsprobe', ContentType.BYTE),
    # Bremse steuern
    LLP(PID(2, 0x010a, 8), None, BasicNode),
    LLP(PID(2, 0x010a, 8, 1), 'bremse_fernsteuerung_aktivieren', ContentType.BYTE),
    LLP(PID(2, 0x010a, 8, 1), 'bremse_druck_hll', ContentType.SINGLE),
    LLP(PID(2, 0x010a, 8, 1), 'bremse_druck_bremszylinder', ContentType.SINGLE),
    # Weiche stellen
    LLP(PID(2, 0x010a, 9), None, BasicNode),
    LLP(PID(2, 0x010a, 9, 1), None, BasicNode),
    LLP(PID(2, 0x010a, 9, 1, 1), 'weiche_statusabfrage', ContentType.BYTE),
    LLP(PID(2, 0x010a, 9, 2), None, BasicNode),
    LLP(PID(2, 0x010a, 9, 2, 1), 'weiche_bezeichnung', ContentType.STRING),
    LLP(PID(2, 0x010a, 9, 2, 1), 'weiche_stellung', ContentType.BYTE),
    # Tempomat
    LLP(PID(2, 0x010a, 0x0a), None, BasicNode),
    LLP(PID(2, 0x010a, 0x0a, 1), 'tempomat_sollwert', ContentType.SINGLE),
    # Stromabnehmer
    LLP(PID(2, 0x010a, 0x0b), None, BasicNode),
    LLP(PID(2, 0x010a, 0x0b, 1), 'stromabnehmer_fahrzeugnr', ContentType.WORD),
    LLP(PID(2, 0x010a, 0x0b, 2), 'stromabnehmer_bitmuster', ContentType.BYTE),
    LLP(PID(2, 0x010a, 0x0b, 3), 'stromabnehmer_absperrhaehne', ContentType.BYTE),
    # Bremse einstellen
    LLP(PID(2, 0x010a, 0x0c), None, BasicNode),
    LLP(PID(2, 0x010a, 0x0c, 1), 'bremsstellung_fahrzeugnr', ContentType.WORD),
    LLP(PID(2, 0x010a, 0x0c, 2), 'bremsstellung_stellung', ContentType.BYTE),
    LLP(PID(2, 0x010a, 0x0c, 3), 'bremsstellung_indirektebremse', ContentType.BYTE),
    LLP(PID(2, 0x010a, 0x0c, 4), 'bremsstellung_absperrhahn', ContentType.BYTE, ZUGFAHRDATEN_ABSPERRHAEHNE_HLL),
    # PDFs
    LLP(PID(2, 0x010a, 0x0d), 'pdf_bremszettel', ContentType.FILE),
    LLP(PID(2, 0x010a, 0x0e), 'pdf_wagenliste', ContentType.FILE),
    LLP(PID(2, 0x010a, 0x0f), 'pdf_la', ContentType.FILE),
    LLP(PID(2, 0x010a, 0x10), 'pdf_streckenbuch', ContentType.FILE),
    LLP(PID(2, 0x010a, 0x11), 'pdf_ersatzfahrplan', ContentType.FILE),
    # Türsystem
    # FIXME Enum might be wrong, cannot be tested right now
    LLP(PID(2, 0x010a, 0x12), 'tueren_status', ContentType.SMALLINT, TUEREN_SEITE, multipletimes=True),
    # Antriebe
    LLP(PID(2, 0x010a, 0x13), 'antrieb_deaktivieren', ContentType.BYTE, multipletimes=True),
    LLP(PID(2, 0x010a, 0x14), 'antrieb_aktivieren', ContentType.BYTE, multipletimes=True),
    # Dynamische Bremse
    LLP(PID(2, 0x010a, 0x15), 'dyn_bremse_deaktivieren', ContentType.BYTE, multipletimes=True),
    LLP(PID(2, 0x010a, 0x16), 'dyn_bremse_aktivieren', ContentType.BYTE, multipletimes=True),
    # ZBS
    LLP(PID(2, 0x010a, 0x17), 'zbs_deaktivieren', ContentType.BYTE, multipletimes=True),
    LLP(PID(2, 0x010a, 0x18), 'zbs_aktivieren', ContentType.BYTE, multipletimes=True)
)
msgidx[PID(2, 0x010a)] = INPUT
# Just to ease with autocomplete
INPUT_TASTATURZUORDNUNG = DATAOPS_TASTATURZUORDNUNG
INPUT_TASTATURKOMMANDO = DATAOPS_TASTATURKOMMANDO
INPUT_TASTATURAKTION = DATAOPS_TASTATURAKTION
INPUT_SCHALTER = SCHALTER
INPUT_INDUSI_FUNKTIONSPRUEFUNG_STARTEN = INDUSI_FUNKTIONSPRUEFUNG_STARTEN
INPUT_INDUSI_KLARTEXTMELDUNGEN = INDUSI_KLARTEXTMELDUNGEN
INPUT_INDUSI_MODUS = INDUSI_MODUS
INPUT_INDUSI_STOERSCHALTERBAURT = INDUSI_STOERSCHALTERBAURT
INPUT_INDUSI_SYSTEMSTATUS = INDUSI_SYSTEMSTATUS
INPUT_INDUSI_ZUGART = INDUSI_ZUGART
INPUT_ZUGFAHRDATEN_ABSPERRHAEHNE_HLL = ZUGFAHRDATEN_ABSPERRHAEHNE_HLL

#
# CONTROL
# Client -> Zusi
#
class CONTROL_STATE(Enum):
    UMSCHALTEN = -1
    AUS = 0
    EIN = 1
class CONTROL_SEITE(Enum):
    LINKS = 0
    RECHTS = 1
CONTROL = namedtuple("CONTROL", ['pause', 'neustart_zugnummer', 'start_dateiname', 'start_zugnummer', 'simulationsende', 'fahrplan_neustart', 'zugwahl_nach_neustart', 'zeitsprung', 'zeitraffer', 'blickpunkt_standard', 'fahrzeugbild_hoehe', 'fahrzeugbild_seite'], defaults=[None] * 12)
llps[CONTROL] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x010b), None, BasicNode),
    LLP(PID(2, 0x010b, 1), None, BasicNode),
    LLP(PID(2, 0x010b, 1, 1), 'pause', ContentType.SHORTINT),
    LLP(PID(2, 0x010b, 2), None, BasicNode),
    LLP(PID(2, 0x010b, 2, 1), 'neustart_zugnummer', ContentType.STRING),
    LLP(PID(2, 0x010b, 3), None, BasicNode),
    LLP(PID(2, 0x010b, 3, 1), 'start_dateiname', ContentType.STRING),
    LLP(PID(2, 0x010b, 3, 2), 'start_zugnummer', ContentType.STRING),
    LLP(PID(2, 0x010b, 4), 'simulationsende', BasicNode, nodeasbool=True),
    LLP(PID(2, 0x010b, 5), 'fahrplan_neustart', BasicNode, nodeasbool=True),
    LLP(PID(2, 0x010b, 6), None, BasicNode),
    LLP(PID(2, 0x010b, 6, 1), 'zugwahl_nach_neustart', ContentType.STRING),
    LLP(PID(2, 0x010b, 7), None, BasicNode),
    LLP(PID(2, 0x010b, 7, 1), 'zeitsprung', ContentType.SHORTINT),
    LLP(PID(2, 0x010b, 8), None, BasicNode),
    LLP(PID(2, 0x010b, 8, 1), 'zeitraffer', ContentType.SHORTINT),
    LLP(PID(2, 0x010b, 0x0d), 'blickpunkt_standard', BasicNode),
    LLP(PID(2, 0x010b, 0x0e), None, BasicNode),
    LLP(PID(2, 0x010b, 0x0e, 1), 'fahrzeugbild_hoehe', ContentType.WORD),
    LLP(PID(2, 0x010b, 0x0e, 2), 'fahrzeugbild_seite', ContentType.WORD, CONTROL_SEITE),
)
msgidx[PID(2, 0x010b)] = CONTROL
