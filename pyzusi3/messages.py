from collections import namedtuple
from enum import Enum

from pyzusi3.nodes import ContentType, BasicNode

ParameterId = namedtuple("ParameterId", ['id1', 'id2', 'id3', 'id4', 'id5', 'id6'], defaults=[None, None, None, None, None, None])
LowlevelParameter = namedtuple("LowlevelParameter", ['parameterid', 'parametername', 'contenttype', 'enumtype'], defaults=[None])
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
    EIN = 1
    AUS = 2

#
# HELLO
# Client -> Zusi
#
class ClientTyp(Enum):
    ZUSI = 1
    FAHRPULT = 2
HELLO = namedtuple("HELLO", ['protokollversion', 'clienttyp', 'clientname', 'clientversion'], defaults=([None] * 4))
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
ACK_HELLO = namedtuple("ACK_HELLO", ['zusiversion', 'verbindungsinfo', 'status', 'startdatum', 'protokollversion'], defaults=([None] * 5))
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
    # XXX STATUS_TUEREN = 102
    STATUS_SIFA = 100
    STATUS_ZUGBEEINFLUSSUNG = 101
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
    # XXX STATUS_FZ = 141
    # XXX STATUS_ZUGVERBAND = 142
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
    # XXX STATUS_LM_FUER_ZUSIPISPLAY = 169
    AUSSENHELLIGKEIT = 170
    # XXX STATUS_ZUGFAHRDATEN = 171
    FUEHRERSTAND_DEAKTIVIERT = 172
    SOLLDRUCK_HL = 173
    STW_MOTORDREHZAHL_2 = 174
    STW_MOTORDREHMOMENT_2 = 175
    STW_MOTORSTROM_2 = 176
    STW_MOTORSPANNUNG_2_ = 177
NEEDED_DATA = namedtuple("NEEDED_DATA", ['anzeigen', 'bedienung', 'programmdaten'], defaults=([None] * 3))
llps[NEEDED_DATA] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 3), None, BasicNode),
    LLP(PID(2, 3, 0x0a), None, BasicNode),
    LLP(PID(2, 3, 0x0a, 1), 'anzeigen', ContentType.WORD),
    LLP(PID(2, 3, 0x0b), None, BasicNode),
    LLP(PID(2, 3, 0x0b, 1), 'bedienung', ContentType.WORD),
    LLP(PID(2, 3, 0x0c), None, BasicNode),
    LLP(PID(2, 3, 0x0c, 1), 'programmdaten', ContentType.WORD),
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
DATA_FTD = namedtuple("DATA_FTD", ['geschwindigkeit', 'druck_hauptluftleitung', 'druck_bremszylinder', 'druck_hauptluftbehaelter', 'luftpresser_laeuft', 'luftstrom_fbv', 'luftstrom_zbv', 'luefter_an', 'zugkraft_gesamt', 'zugkraft_pro_achse', 'zugkraft_soll_gesamt', 'zugkraft_soll_pro_achse', 'oberstrom', 'fahrleitungsspannung', 'motordrehzahl', 'uhrzeit_stunde', 'uhrzeit_minute', 'uhrzeit_sekunde', 'hauptschalter', 'trennschuetz', 'fahrstufe', 'fenster_3d', 'afb_sollgeschwindigkeit', 'druck_hilfsbehaelter', 'zurueckgelegter_gesamtweg', 'lm_getriebe', 'lm_schleudern', 'lm_gleiten', 'lm_mg_bremse', 'lm_h_bremse', 'lm_r_bremse', 'lm_hochabbremsung', 'lm_schnellbremsung', 'lm_uhrzeit', 'lm_drehzahlverstellung', 'lm_fahrtrichtung_vor', 'lm_fahrtrichtung_zurueck', 'lm_fahrtrichtung_m', 'motordrehmoment', 'motorlast_normiert', 'tunnel', 'schienenstoss_weiche', 'stahlbruecke', 'steinbruecke', 'x_koordinate', 'y_koordinate', 'z_koordinate', 'utm_referenzpunkt_x', 'utm_referenzpunkt_y', 'utm_zone', 'utm_zone_2', 'afb_an', 'fahrpultintern_01', 'fahrpultintern_02', 'fahrpultintern_03', 'fahrpultintern_04', 'fahrpultintern_05', 'fahrpultintern_06', 'fahrpultintern_07', 'fahrpultintern_08', 'fahrpultintern_09', 'fahrpultintern_10', 'fahrpultintern_11', 'fahrpultintern_12', 'fahrpultintern_13', 'fahrpultintern_14', 'fahrpultintern_15', 'fahrpultintern_16', 'fahrpultintern_17', 'fahrpultintern_18', 'fahrpultintern_19', 'fahrpultintern_20', 'datum', 'gleiskruemung', 'streckenvmax', 'zugkraftvorschlag_autopilot', 'beschleunigung_x', 'beschleunigung_y', 'beschleunigung_z', 'drehbeschleunigung_x', 'drehbeschleunigung_y', 'drehbeschleunigung_z', 'stromabnehmer', 'lm_federspeicherbremse_angelegt', 'zustand_federspeicherbremse', 'stw_lm_getriebe', 'stw_lm_schleudern', 'stw_lm_gleiten', 'stw_lm_h_bremse', 'stw_lm_r_bremse', 'stw_lm_drehzahlverstellung', 'druck_zeitbehaelter', 'geschwindigkeit_absolut', 'zug_ist_entgleist', 'kilometrieung', 'motorstrom', 'motorspannung', 'fahrpultintern_21', 'fahrpultintern_22', 'fahrpultintern_23', 'fahrpultintern_24', 'fahrpultintern_25', 'fahrpultintern_26', 'fahrpultintern_27', 'fahrpultintern_28', 'fahrpultintern_29', 'fahrpultintern_30', 'fahrpultintern_31', 'fahrpultintern_32', 'fahrpultintern_33', 'fahrpultintern_34', 'fahrpultintern_35', 'fahrpultintern_36', 'fahrpultintern_37', 'fahrpultintern_38', 'fahrpultintern_39', 'fahrpultintern_40', 'stw_luefter_an', 'stw_zugkraft_gesamt', 'stw_zugkraft_pro_achse', 'stw_zugkraft_soll_gesamt', 'stw_zugkraft_soll_pro_achse', 'stw_oberstrom', 'stw_fahrleitungsspannung', 'stw_motordrehzahl_1', 'stw_hauptschalter', 'stw_trennschuetz', 'stw_fahrstufe', 'stw_motordrehmoment_1', 'stw_motorlast_normiert', 'stw_stromabnehmer', 'stw_motorstrom_1', 'stw_motorspannung_1', 'geschwindigkeit_absolut_mit_schleudern', 'batteriehauptschalter_aus', 'bremsprobefunktion', 'zug_und_bremskraft_normiert', 'stw_zug_und_bremskraft_normiert', 'zug_und_bremskraft_absolut_normiert', 'stw_zug_und_bremskraft_absolut_normiert', 'fahrzeugintern_01', 'fahrzeugintern_02', 'fahrzeugintern_03', 'fahrzeugintern_04', 'fahrzeugintern_05', 'fahrzeugintern_06', 'fahrzeugintern_07', 'fahrzeugintern_08', 'fahrzeugintern_09', 'fahrzeugintern_10', 'fahrzeugintern_11', 'fahrzeugintern_12', 'fahrzeugintern_13', 'fahrzeugintern_14', 'fahrzeugintern_15', 'fahrzeugintern_16', 'fahrzeugintern_17', 'fahrzeugintern_18', 'fahrzeugintern_19', 'fahrzeugintern_20', 'aussenhelligkeit', 'fuehrerstand_deaktiviert', 'solldruck_hl', 'stw_motordrehzahl_2', 'stw_motordrehmoment_2', 'stw_motorstrom_2', 'stw_motorspannung_2_'], defaults=([None] * 167))
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
STATUS_NOTBREMSSYSTEM = namedtuple("STATUS_NOTBREMSSYSTEM", ['bauart', 'status', 'system_bereit', 'notbremsung', 'modus', 'LM_system_bereit', 'LM_notbremsung'], defaults=[None, None, None, None, None, None, None])
llps[STATUS_NOTBREMSSYSTEM] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x22), None, BasicNode),
    LLP(PID(2, 0x0a, 0x22, 1), 'bauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x22, 2), 'status', ContentType.BYTE, STATUS_NB_UEBERBRUECKUNG),
    LLP(PID(2, 0x0a, 0x22, 3), 'system_bereit', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x22, 4), 'notbremsung', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x22, 5), 'modus', ContentType.BYTE, STATUS_NB_TEST),
    LLP(PID(2, 0x0a, 0x22, 6), 'LM_system_bereit', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x22, 7), 'LM_notbremsung', ContentType.BYTE, LMZUSTAND)
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
STATUS_SIFA = namedtuple("STATUS_SIFA", ['bauart', 'lm', 'hupe', 'hauptschalter', 'stoerschalter', 'lufthahn', 'weg'], defaults=[None, None, None, None, None, None, None])
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
msgidx[PID(2, 0x0a, 0x65, 1)] = STATUS_ZUGBEEINFLUSSUNG_GRUND

#
# STATUS_INDUSI_EINSTELLUNGEN
# Zusi -> Client (Submessage) 
#
class INDUSI_ZUGART(Enum):
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
STATUS_INDUSI_EINSTELLUNGEN = namedtuple("STATUS_INDUSI_EINSTELLUNGEN", ['zugart', 'hauptschalter', 'stoerschalter', 'luftabsperhan', 'systemstatus', 'bauart', 'tfnr', 'zugnummer', 'e_brh', 'e_bra', 'e_zugart', 'a_brh', 'a_bra', 'a_zugart', 'a_modus', 'klartextmeldungen', 'funktionspruefung_starten', 'stoerschalterbaurt'], defaults=([None] * 18))
llps[STATUS_INDUSI_EINSTELLUNGEN] = (
    # Indusi Analogsysteme und Basisdaten
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 1), 'zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 7), 'hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 8), 'stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0a), 'luftabsperhan', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0d), 'systemstatus', ContentType.BYTE, INDUSI_SYSTEMSTATUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0e), 'bauart', ContentType.STRING),
    # Indusi I60R/I80/PZB90
    LLP(PID(2, 0x0a, 0x65, 2, 0x02), 'tfnr', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 2, 0x03), 'zugnummer', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 0x01), 'e_brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 0x02), 'e_bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 0x05), 'e_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x01), 'a_brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x02), 'a_bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x05), 'a_zugart', ContentType.BYTE, INDUSI_ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x06), 'a_modus', ContentType.BYTE, INDUSI_MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0B), 'klartextmeldungen', ContentType.BYTE, INDUSI_KLARTEXTMELDUNGEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0C), 'funktionspruefung_starten', ContentType.BYTE, INDUSI_FUNKTIONSPRUEFUNG_STARTEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0F), 'stoerschalterbaurt', ContentType.BYTE, INDUSI_STOERSCHALTERBAURT),
)
msgidx[PID(2, 0x0a, 0x65, 2)] = STATUS_INDUSI_EINSTELLUNGEN

#
# STATUS_INDUSI_BETRIEBSDATEN
# Zusi -> Client (Submessage) 
#
class INDUSI_ZUSTAND(Enum):
    AUSGESCHALTET = 1
    ABGESCHALTET_GESTOERT = 2
    HL_DRUCK_NIDRIG = 3
    AUFFODERUNG_ZUGDATENEINGABE = 4
    NORMALBETRIEB = 5
    FUNKTIONSPRUEFUNG = 6
    FUNKTIONSPRUEFUNG_QUTIERUNG_FEHLT = 7
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
    LZB_HALT = 9
    LZB_RECHNERAUSFALL = 10
    LZB_NOTHALT = 11
    LZB_UEBERTRAGUNGSAUSFALL = 12
    V_UEBERSCHREITUNG_LZB_AUSFALL = 13
    RICHTUNGSSCHALTER_VERLEGT = 14
    LZB_RUECKROLLUEBERWACHUNG = 25
    LZB_UEBERSCHREITUNG_200M_NACH_BEFEHL = 26
    ALLGEMEINE_STOERUNG = 27
    STROMVERSORGUNG = 28
class INDUSI_HUPE(Enum):
    AUS = 0
    HUPE = 1
    ZWANGSBREMSUNG = 2
class INDUSI_ZUSATZINFO_MELDERBILD(Enum):
    NORMALZUSTAND = 0
    _1000HZ_NACH_700M = 1
    RESTREKTIV = 2
    RESTREKTIV_1000HZ = 3
    RESTREKTIV_500HZ = 4
    PRUEFABLAUF = 5
STATUS_INDUSI_BETRIEBSDATEN = namedtuple("STATUS_INDUSI_BETRIEBSDATEN", ['zustand', 'zwangsbremsung', 'zwangsbremsung_grund', 'm_1000hz', 'm_u', 'm_m', 'm_o', 'hupe', 'beeinflussung_1000hz', 'beeinflussung_500hz', 'beeinflussung_2000hz', 'lm_1000hz', 'm_500hz', 'm_befehl_an', 'lm_o', 'lm_m', 'lm_u', 'lm_500hz', 'lm_befehl', 'zusatzinfo_melderbild', 'lm_zugart_links', 'lm_zugart_65', 'lm_zugart_rechts', 'status_lm_zugart_rechts', 'status_lm_zugart_65', 'status_lm_zugart_links', ], defaults=([None] * 26))
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
    LLP(PID(2, 0x0a, 0x65, 3, 0x0C), 'zusatzinfo_melderbild', ContentType.BYTE, INDUSI_ZUSATZINFO_MELDERBILD),
    # PZB90 S-Bahn
    LLP(PID(2, 0x0a, 0x65, 3, 0x29), 'lm_zugart_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2a), 'lm_zugart_65', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2b), 'lm_zugart_rechts', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x35), 'status_lm_zugart_rechts', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x36), 'status_lm_zugart_65', ContentType.BYTE, LMZUSTAND_MIT_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x37), 'status_lm_zugart_links', ContentType.BYTE, LMZUSTAND_MIT_INVERS)
)
msgidx[PID(2, 0x0a, 0x65, 3)] = STATUS_INDUSI_BETRIEBSDATEN

#LZB
class ZUGART(Enum):
    NICHT_BESTIMMT = 1
    U = 2
    M = 3
    O = 4
class LZB_MODUS(Enum):
    UNDEFINIERT = 1
    U = 2
    M = 3
    O = 4
class STOERSCHALTER(Enum):
    LZB_ABGESCHALTET = 1
    LZB_EINGESCHALTET = 2
class LZB_KLARTEXTMELDUNG(Enum):
    NICHT_MOEGLICH = 0
    MOEGLICH_ABER_NICHT_AKTIV = 1
    AKTIV = 2
    NUR_MOEGLICH = 3
class STOERSCHALTERBAURT(Enum):
    LEUCHTDRUCKTASTER = 0
    DREHSCHALTER = 1
class SYSTEMSTATUS(Enum):
    AUSGESCHALTET = 0
    ABGESCHALTET = 1
    UNTERDRUECKT = 2
    AKTIV = 3
class ZUSTAND(Enum):
    KEINE_FUEHRUNG = 0
    NORMAL = 1
    NOTHALT = 2
    HALT_UEBERFAHREN = 3
    RECHNERAUSFALL = 4
    NACHFAHRAUFTAG = 5
    FUNKTIONSPRUEFUNG = 6
class ENDE_VERFAHREN(Enum):
    EINGELETITET = 1
    QUITTIERT = 2
class FALSCHFAHRAUFTRAG_STATUS(Enum):
    EINGELETITET = 1
    QUITTIERT = 2
class VORSICHTSAUFTRAG_STATUS(Enum):
    EINGELETITET = 1
    QUITTIERT = 2
    FAHRT_AUF_SICHT = 3
class ZIELGESCHWINDIGKEIT_STATUS(Enum):
    EINGELEITET = 1
    UE_BLINKT = 2
    ERSTE_QUITTIERUNG = 3
    BEDINGUNG_2_QUTTIERUNG = 4
    ZWEITE_QUITTIERUNG = 5
    AUSFALL = 6
    BEFEHL_BLINKT = 7
class LZB_NOTHALT(Enum):
    NOTHAL_TEMPFANGEN = 1
    NOTHALT_UEBERFAHREN = 2
    NOTHALT_AUFGEHOBEN = 3
class STATUS_LZB_RECHNERAUSFALL(Enum):
    ALLES_DUNKEL = 1
    BEFEHLSMELDER_BLINKT = 2
    BEFEHLSMELDER_DAUERLICHT = 3
class EL_AUFTAG(Enum):
    HS_AUS = 1
    SA_SENKEN = 2
class CIR_ELKE_MODUS(Enum):
    NORMALER_MODUS = 0
    CIR_ELKE_MODUS = 1
class ANZEIGEMODUS(Enum):
    NORMALER_MODUS = 0
    MFA = 1
LZB = namedtuple("LZB", ['brh','bra','zl','vmz','zugart','modus','stoerschalter','lzb_klartextmeldung','funktionspruefung_starten','stoerschalterbaurt','systemstatus','zustand','ende_verfahren','Falschfahrauftrag_status','Vorsichtsauftrag_status','zielgeschwindigkeit','zielgeschwindigkeit_status','zielweg_cir_elke','lzb_nothalt','nothalt_gesendet','status_lzb_rechnerausfall','el_auftag','melder_h','melder_e40','melder_ende','melder_b','melder_u','melder_g','melder_el','melder_v40','melder_s','melder_pruef','sollgeschwindigkeit','zielgeschwindigkeit_','zielweg','melder_g_status','melder_pruef_status','cir_elke_modus','anzeigemodus','melder_h_status','melder_e40_status','melder_ende_status','melder_b_status','melder_u_status','melder_el_status','melder_v40_status','melder_s_status'],defaults=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
llps[LZB] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x04), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x04, 1),'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x04, 2), 'bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x04, 3),  'zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x04, 4),  'vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x04, 5),  'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x04, 6), 'modus', ContentType.BYTE, INDUSI_MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 1), 'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 2), 'bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 3), 'zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 4), 'vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 5), 'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 6), 'modus', ContentType.BYTE, INDUSI_MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 1), 'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 2), 'bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 3), 'zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 4), 'vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 5), 'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 6), 'modus', ContentType.BYTE, INDUSI_MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x09), 'stoerschalter', ContentType.BYTE, STOERSCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0b), 'lzb_klartextmeldung', ContentType.BYTE, LZB_KLARTEXTMELDUNG),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0c), 'funktionspruefung_starten', ContentType.BYTE, INDUSI_FUNKTIONSPRUEFUNG_STARTEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x10), 'stoerschalterbaurt', ContentType.BYTE, STOERSCHALTERBAURT),
    LLP(PID(2, 0x0a, 0x65, 2, 0x11), 'systemstatus', ContentType.BYTE, SYSTEMSTATUS),
    LLP(PID(2, 0x0a, 0x65, 3),None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0d), 'zustand', ContentType.WORD, ZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0e), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0e, 1), 'ende_verfahren', ContentType.BYTE, ENDE_VERFAHREN),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0f), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x10), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x10, 1), 'Falschfahrauftrag_status', ContentType.BYTE, FALSCHFAHRAUFTRAG_STATUS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x11), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x11, 1), 'Vorsichtsauftrag_status', ContentType.BYTE, VORSICHTSAUFTRAG_STATUS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x12), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x13), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 1), 'zielgeschwindigkeit', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 2), 'zielgeschwindigkeit_status', ContentType.WORD, ZIELGESCHWINDIGKEIT_STATUS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 3), 'zielweg_cir_elke', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x14), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x14, 1), 'lzb_nothalt', ContentType.BYTE, LZB_NOTHALT),
    LLP(PID(2, 0x0a, 0x65, 3, 0x14, 2), 'nothalt_gesendet', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x15), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x15, 1), 'status_lzb_rechnerausfall', ContentType.BYTE, STATUS_LZB_RECHNERAUSFALL),
    LLP(PID(2, 0x0a, 0x65, 3, 0x16), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x16, 1), 'el_auftag', ContentType.BYTE, EL_AUFTAG),
    LLP(PID(2, 0x0a, 0x65, 3, 0x17), 'melder_h', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x18), 'melder_e40', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x19), 'melder_ende', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1a), 'melder_b', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1b), 'melder_u', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1c), 'melder_g', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1d), 'melder_el', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1e), 'melder_v40', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x1f), 'melder_s', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x20), 'melder_pruef', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x21), 'sollgeschwindigkeit', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x22), 'zielgeschwindigkeit_', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x23), 'zielweg', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x24), 'melder_g_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x25), 'melder_pruef_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x26), 'cir_elke_modus', ContentType.BYTE, CIR_ELKE_MODUS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x27), 'anzeigemodus', ContentType.BYTE, ANZEIGEMODUS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,1), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,3), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,4), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,5), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x38), 'melder_h_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x39), 'melder_e40_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3a), 'melder_ende_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3b), 'melder_b_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3c), 'melder_u_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3d), 'melder_el_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3e), 'melder_v40_status', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x3d), 'melder_s_status', ContentType.BYTE, LMZUSTAND)
)
msgidx[PID(2, 0x0a, 0x65, 2, 0x04)] = LZB

#ETCS

#ZUB
class STATUS(Enum):
    AUSGESCHALTET = 0
    ABGESCHALTET = 1
    UNTERDRUECKT = 2
    AKTIV = 3
ZUB = namedtuple("ZUB", ['brh','zuglaenge', 'vmz', 'status', 'bauart', 'lm_gnt', 'melder_gnt_ue', 'melder_gnt_g', 'melder_gnt_s', 'melder_gnt_gst', 'melder_gnt_gst_stoer', 'status_melder_ue', 'status_melder_gnt_'],defaults=[None, None, None, None, None])
llps[ZUB] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 6, 1),'', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 6, 2),'', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 6, 3),'', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 6, 4),'', ContentType.BYTE, STATUS),
    LLP(PID(2, 0x0a, 0x65, 6, 5),'', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 7), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 7, 1), '', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 2), '', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 3), '', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 4), '', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 5), '', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 6), '', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 7), '', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 7, 8), '', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 7, 9), '', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 7, 0x0a), '', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 7, 0x0b), '', ContentType.BYTE)
)
msgidx[PID(2, 0x0a, 0x65)] = ZUB


#ZBS


#Fahrsperre

#Status Türen
#Grundblock

class STATUS_TUEREN(Enum):
    ZU = 0
    OEFFNEND = 1
    OFEN = 2
    FAHRGASTWECHSEL_ABGESCHLOSSEN = 3
    SCHLIESSEND = 4
    GESTOERT = 5
    BLOCKIERT = 6
class TUERZUSTAND(Enum):
    ALLE_ZU = 0
    MIN_EINE_OFFEN = 1
TUEREN_GRUNDBLOCK = namedtuple("TUEREN_GRUNDBLOCK", ['bezeichnung','linke_seite', 'rechte_seite', 'traktionssperre', 'zustand'],defaults=[None, None, None, None, None])
llps[TUEREN_GRUNDBLOCK] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x66), None, BasicNode),
    LLP(PID(2, 0x0a, 0x66, 1),'bezeichnung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x66, 2),'linke_seite', ContentType.BYTE, STATUS_TUEREN),
    LLP(PID(2, 0x0a, 0x66, 3),'rechte_seite', ContentType.BYTE, STATUS_TUEREN),
    LLP(PID(2, 0x0a, 0x66, 4),'traktionssperre', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66, 14),'zustand', ContentType.BYTE, TUERZUSTAND)
)
msgidx[PID(2, 0x0a, 0x66)] = TUEREN_GRUNDBLOCK

#Seitenselktive Systeme
class FREIGABE_STATUS(Enum):
    ZU = 0
    LINKS = 1
    RECHTS = 2
    BEIDE = 3
TUEREN_SEITENSELEKTIV = namedtuple("TUEREN_SEITENSELEKTIV", ['freigabe', 'lm_links', 'lm_rechts', 'status_lm_links', 'status_lm_rechts', 'lm_zwnagsschliessen', 'status_lm_zwangsschliessen', 'lm_rechts_links', 'status_lm_rechts_links', 'zentrales_oeffnen_links', 'zentrales_oeffnen_rechts', 'status_lm_zentrales_oeffnen_links', 'status_lm_zentrales_oeffnen_rechts', 'lm_gruenschleife'],defaults=[None, None, None, None, None, None, None, None, None, None, None, None, None, None])
llps[TUEREN_SEITENSELEKTIV] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x66), None, BasicNode),
    LLP(PID(2, 0x0a, 0x66,0x05), 'freigabe', ContentType.BYTE, FREIGABE_STATUS),
    LLP(PID(2, 0x0a, 0x66,0x06), 'lm_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66,0x07), 'lm_rechts', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66,0x08), 'status_lm_links', ContentType.BYTE,LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66,0x09), 'status_lm_rechts', ContentType.BYTE,LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66,0x0a), 'lm_zwnagsschliessen', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66,0x0b), 'status_lm_zwangsschliessen', ContentType.BYTE,LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66,0x0c), 'lm_rechts_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66,0x0d), 'status_lm_rechts_links', ContentType.BYTE,LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66,0x0e), 'zentrales_oeffnen_links', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66,0x0f), 'zentrales_oeffnen_rechts', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x66,0x10), 'status_lm_zentrales_oeffnen_links', ContentType.BYTE,LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66,0x11), 'status_lm_zentrales_oeffnen_rechts', ContentType.BYTE,LMZUSTAND),
    LLP(PID(2, 0x0a, 0x66,0x12), 'lm_gruenschleife', ContentType.BYTE,LMZUSTAND)
)
msgidx[PID(2, 0x0a, 0x66)] = TUEREN_SEITENSELEKTIV

#Satus Fahrzeug
class GRUND_NULLSTELLUNGSZWANG(Enum):
    NICHTS = 0
    NIEDRIGER_HLL_DRUCK = 1
    DYNAMISCHE_BREMSE = 2
    TRAKTIONSSPERRE = 3
class GRUND_TRAKTIONSSPERRE(Enum):
    NICHTS = 0
    FEDERSPEICHERBREMSE = 1
    TUERSYSTEM = 2
    BREMSPROBE_LAUFT = 3
    SIFA_ASUGESCHALTET = 4
class STATUS_SCHALTER(Enum):
    DEAKTIVIERT = 1
    NORMALZUSTAND = 2
class SANDERZUSTAND(Enum):
    SANDET_NICHT = 1
    SANDET = 2
class BREMSPROBEZUSTAND(Enum):
    NORMALBETRIEB = 0
    AKTIV = 1

STATUS_FAHRZEUG = namedtuple("STATUS_FAHRZEUG", ['grund_nullstellungszwang', 'grund_traktionssperre', 'status_fahrschalter', 'status_dynamische_bremse', 'sanderzustand', 'bremsprobezustand', 'stellung_richtungsschalter'],defaults=[None, None, None, None, None, None, None])
llps[STATUS_FAHRZEUG] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8d), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8d,0x01), 'grund_nullstellungszwang', ContentType.WORD, GRUND_NULLSTELLUNGSZWANG),
    LLP(PID(2, 0x0a, 0x8d,0x02), 'grund_traktionssperre', ContentType.WORD, GRUND_TRAKTIONSSPERRE),
    LLP(PID(2, 0x0a, 0x8d,0x03), 'status_fahrschalter', ContentType.BYTE, STATUS_SCHALTER),
    LLP(PID(2, 0x0a, 0x8d,0x04), 'status_dynamische_bremse', ContentType.BYTE, STATUS_SCHALTER),
    LLP(PID(2, 0x0a, 0x8d,0x06), 'sanderzustand', ContentType.BYTE, SANDERZUSTAND),
    LLP(PID(2, 0x0a, 0x8d,0x07), 'bremsprobezustand', ContentType.WORD, BREMSPROBEZUSTAND),
    LLP(PID(2, 0x0a, 0x8d,0x08), 'stellung_richtungsschalter', ContentType.WORD)
)
msgidx[PID(2, 0x0a, 0x8d)] = STATUS_FAHRZEUG

#Status Zugverband

class BREMSSTELLUNG(Enum):
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
class TRAKTIONSMODUS(Enum):
    EIGENER_TF = 0
    MEHRFACHTRAKTION = 1
    KALT = 2
class DREHUNG_FZ(Enum):
    FZ_NICHT_GEDREHT = 0
    FZ_GEDREHT = 1
class FUEHRERSTAND(Enum):
    EINE_DATEI_FUER_BEIDE_RICHTUNGEN = 0
    FZ_HAT_KEINEN_FUEHRERSATAND = 1
    NUR_VORWAERTS = 1
    SPERATE_DATEIEN = 3
class BREMSBAUERT(Enum):
    UNDEFINIERT = 0
    SCHEIBENBREMSE = 1
    GRAUGUSS = 2
    K_BREMSSOHLE = 3
    LL_BREMSSOHLE = 4
    MATROSSOW_BREMSE = 5
class BAUART_BATTERIEHAUPTSCHALTER(Enum):
    DREHTATSTER = 0
    KEINER = 1
    HEBELL = 2
    DRUCKTASTER = 3
class BAUART_STROMABNEHMERWAHLSCHALTER(Enum):
    KEINER = 0
    DREHSCHALTER = 1
    LUFTABSPERRHAN = 2
class BREMSSTELLUNG_WIRKSAM(Enum):
    BREMSSTELLUNG_IST_NICHT_WIRKSAM = 0
    BREMSSTELLUNG_IST_WIRKSAM = 1
class FAHRZEUG_VERBUND(Enum):
    EIGENSTAENDIG = 0
    FAHRZEUGTEIL_OHNE_FAHRZEUGSTATUS = 1
class LOKSTATUS(Enum):
    UNBEKANNT = 0
    FZ_IST_LOK = 1
    FZ_IST_KEINE_LOK = 2
class BAUART_TUERSCHALTER(Enum):
    KEINER = 0
    DREHTASTER = 1
class ANTRIEBSTYP(Enum):
    UNBESTIMMT = 0
    EINFACHES_ANTRIEBSMODELL = 1
    DIESEL_ELEKTRISCH_DREHSTROM = 2
    DIESEL_ELEKTRISCH_GLEICHSTROM  = 3
    DIESEL_HYDRAULISCH = 4
    DIESEL_MECHANISCH = 5
    ELEKTRISCH_DREHSTROM = 6
    ELEKTRISCH_REIHENSCHLUSS = 7
class STROMTYP(Enum):
    OHNE = 0
    UNBESTIMMT = 1
    _15KV_16HZ = 2
    _25KV_50HZ = 3
    _1500VDC = 4
    _1200VDC_STROMSCHIENE_HAMBURG = 5
    _3KVDC = 6
    _750VDC_STROMSCHIENE_BERLIN =7
class BREMSTYP(Enum):
    UNBESTIMMT = 0
    ELEKTRISCH_DREHSTROM = 1
    ELEKTRISCH_REIHENSCHLUSS = 2
    RETADER = 3
class STATUS(Enum):
    AKTIV = 0
    NICHT_AKIV = 1
class LASTABHAENIGE_BREMSE(Enum):
    AUTOMAITSCHE_LASTABREMSUNG = 0
    KEINE_AUTOMATISCHE_LASTABREMSUNG = 1
class ZUGTYP(Enum):
    GZ = 0
    RZ = 1
STATUS_ZUGVERBAND = namedtuple("STATUS_ZUGVERBANDG",['fz_dateiname', 'beschreibung', 'vorgabe_bremsstellung', 'bezeichnung_zugbeeinflussungs', 'fz_vmax', 'baureihe', 'farbgebung', 'traktionsmodus', 'stromabnehmerschaltung', 'maximaler_bremszylinder_druck', 'nvr_nr', 'sitzplaetze_1_klasse', 'sitzplaetze_2_klasse', 'fz_drehung', 'fz_gattung', 'fuehrerstandsmodus', 'fz_laenge', 'fz_masse', 'ladungsmasse', 'bremsbaurt', 'bremsmasse_handbremse', 'aktive_bremsmasse', 'aktive_bremssmasse_inkl_dynamische', 'anzahl_achsen', 'bauart_batteriehauptschalter', 'bauart_stromabnehmerwahlschalter', 'bremsstellung', 'zugehoerige_Bremsmasse', 'bremsstellung_wirksam', 'bezeichnung_bremsbaurt', 'grafik_seitenansicht', 'hbl', 'fz_verbund', 'lokstatus', 'interne_fz_nr', 'gefahrgutkenzeichen', 'bezeichnung_tuersystem', 'bauart_tuerwachlschalter', 'antriebstyp', 'stromtyp_antriebssystem', 'antrieb_aktiv', 'bremstyp', 'stromtyp_bremse', 'bremse_aktiv', 'lastabhaehnige_bremse'],defaults=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
llps[STATUS_ZUGVERBAND] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e,0x01), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e,0x01, 0x01),'fz_dateiname', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e,0x01, 0x02),'beschreibung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e,0x01, 0x03),'vorgabe_bremsstellung', BREMSSTELLUNG),
    LLP(PID(2, 0x0a, 0x8e,0x01, 0x04), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e,0x01, 0x04,0x01),'bezeichnung_zugbeeinflussungs', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e,0x01, 0x04), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e,0x01, 0x5),'fz_vmax', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x06),'baureihe', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x07),'farbgebung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x08),'traktionsmodus', ContentType.BYTE, TRAKTIONSMODUS),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x09),'stromabnehmerschaltung', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0a),'maximaler_bremszylinder_druck', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0b),'nvr_nr', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0c),'sitzplaetze_1_klasse', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0d),'sitzplaetze_2_klasse', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0e),'fz_drehung', ContentType.BYTE, DREHUNG_FZ),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x0f),'fz_gattung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x10),'fuehrerstandsmodus', ContentType.BYTE, FUEHRERSTAND),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x11),'fz_laenge', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x12),'fz_masse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x13),'ladungsmasse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x14),'bremsbaurt', ContentType.BYTE, BREMSBAUERT),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x15),'bremsmasse_handbremse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x16),'aktive_bremsmasse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x17),'aktive_bremssmasse_inkl_dynamische', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x18),'anzahl_achsen', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x19),'bauart_batteriehauptschalter', ContentType.BYTE, BAUART_BATTERIEHAUPTSCHALTER),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1a),'bauart_stromabnehmerwahlschalter', ContentType.BYTE, BAUART_STROMABNEHMERWAHLSCHALTER),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b),None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b, 0x01),'bremsstellung', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b, 0x02),'zugehoerige_Bremsmasse', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b, 0x03),'bremsstellung_wirksam', ContentType.BYTE, BREMSSTELLUNG_WIRKSAM),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1b), None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1c),'bezeichnung_bremsbaurt', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1d),'grafik_seitenansicht', ContentType.FILE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1e),'hbl', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1f),'fz_verbund', ContentType.BYTE, FAHRZEUG_VERBUND),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x20),'lokstatus', ContentType.BYTE, LOKSTATUS),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x21),'interne_fz_nr', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x22),'gefahrgutkenzeichen', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x23),None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x23, 0x01),'bezeichnung_tuersystem', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x23),None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x24),'bauart_tuerwachlschalter', ContentType.BYTE, BAUART_TUERSCHALTER),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25),None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25, 0x01),'antriebstyp', ContentType.BYTE, ANTRIEBSTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25, 0x02),'stromtyp_antriebssystem', ContentType.BYTE, STROMTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25, 0x03),'antrieb_aktiv', ContentType.BYTE, STATUS),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x25),None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26),None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26, 0x01),'bremstyp', ContentType.BYTE, BREMSTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26, 0x02),'stromtyp_bremse', ContentType.BYTE, STROMTYP),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26, 0x03),'bremse_aktiv', ContentType.BYTE, STATUS),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x26),None, BasicNode),
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x27),'lastabhaehnige_bremse', ContentType.BYTE, LASTABHAENIGE_BREMSE),
    LLP(PID(2, 0x0a, 0x01),None, BasicNode),
    LLP(PID(2, 0x0a, 0x01, 0x02),'zugtyp', ContentType.BYTE, ZUGTYP)
)
msgidx[PID(2, 0x0a, 0x8e,0x01)] = STATUS_ZUGVERBAND


#Status Weichen
class BAUART(Enum):
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
class TYP(Enum):
    UNDEFINIERT = 0
    OHNE_GRUNDSTELLUNG = 1
    GRUNDSTELLUNG_RECHTS_WEISS = 2
    GRUNDSTELLUNG_LINKS_WEISS = 3
    GRUNDSTELLUNG_RECHTS_gelb = 4
    GRUNDSTELLUNG_LINKS_gelb = 5
class AKTUELLE_LAGE(Enum):
    ZUSI_GRUNDSTELLUNG_SPITZ_BEFAHREN = 0
    NICHT_IN_GRUNDSTELLUNG_SPITZ_BEFAHREN = 1
    ZUSI_GRUNDSTELLUNG_STUMPF_BEFAHREN = 2
    NICHT_IN_GRUNDSTELLUNG_STUMPF_BEFAHREN = 3
class FAHRTRICHTUNG(Enum):
    UNDEFINIERT = 0
    SPITZ_BEFAHREN = 1
    STUMPF_BEFAHREN = 2
class UMLAUFMODUS_STUMPFBEFAHRUNG(Enum):
    UNDEFINIERT = 0
    WEICHE_LAUEFT_AUTOMATISCH_UM = 1
    WEICHE_MUSS_GESTELLT_WERDEN = 2
WEICHEN = namedtuple("WEICHEN", ['bezeichnung', 'bauart', 'typ', 'aktuelle_lage', 'fahrtrichtung', 'umlaufmodus'], defaults=[None, None, None, None, None, None])
llps[WEICHEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x92), None, BasicNode),
    LLP(PID(2, 0x0a, 0x92, 0x01), None, BasicNode),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x01), 'bezeichnung', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x02), 'bauart', ContentType.INTEGER, BAUART),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x03), 'typ', ContentType.INTEGER, TYP),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x04), 'aktuelle_lage', ContentType.BYTE, AKTUELLE_LAGE),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x05), 'fahrtrichtung', ContentType.BYTE, FAHRTRICHTUNG),
    LLP(PID(2, 0x0a, 0x92, 0x01, 0x06), 'umlaufmodus', ContentType.BYTE, UMLAUFMODUS_STUMPFBEFAHRUNG),
    LLP(PID(2, 0x0a, 0x92, 0x01), None, BasicNode)
)
msgidx[PID(2, 0x0a, 0x92,0x01)] = WEICHEN



#Status LM Zusidisplay
class RAHMEN_MODUS(Enum):
    GRAFIK_OHNE_RAHMEN = 0
    GRAFIK_MIT_RAHMEN = 1
    GRAFIKMIT_TASTEN = 2

LM_ZUSIDISPLAY = namedtuple("LM_ZUSIDISPLAY", ['name', 'modus', 'breite', 'hoehe'], defaults=[None, None, None, None])
llps[LM_ZUSIDISPLAY] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9, 0x01), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x01), 'name', ContentType.STRING),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x02), 'modus', ContentType.BYTE, RAHMEN_MODUS),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x03), 'breite', ContentType.WORD),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x04), 'hoehe', ContentType.WORD),
    LLP(PID(2, 0x0a, 0xa9, 0x01), None, BasicNode)
)
msgidx[PID(2, 0x0a, 0xa9,0x01)] = LM_ZUSIDISPLAY

#Status Zug Fahrdaten
class ABSPERHAEHNE_HLL(Enum):
    STANDARD = 0
    HAN_VORNE_OFFEN = 1
    HAN_HINTEN_OFFEN = 2
    BEIDE_HAEHNE_OFFEN = 3
    BEIDE_HAEHNE_ZU = 4
STATUS_ZUG_FAHRDATEN = namedtuple("STATUS_ZUG_FAHRDATEN",['bremszylinderdruck', 'hll_druck', 'zugkraft', 'motordrehzahl_1', 'maximal_moegliche_zugkraft', 'maximale_dynamische_bremskraft', 'absperhaehne_hll', 'motordrehzahl_2'],defaults=[None,None,None,None,None,None,None,None])
llps[STATUS_ZUG_FAHRDATEN] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0xab), None, BasicNode),
    LLP(PID(2, 0x0a, 0xab,0x01), None, BasicNode),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x01),'bremszylinderdruck', ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x02),'hll_druck',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x03),'zugkraft',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x04),'motordrehzahl_1',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x05),'maximal_moegliche_zugkraft',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x06),'maximale_dynamische_bremskraft',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x07),'absperhaehne_hll',ContentType.BYTE, ABSPERHAEHNE_HLL),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x0a),'motordrehzahl_2',ContentType.SINGLE),
    LLP(PID(2, 0x0a, 0xab,0x01), None, BasicNode)
)
msgidx[PID(2, 0x0a, 0xab,0x01)] = STATUS_ZUG_FAHRDATEN
