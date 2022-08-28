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

# Lampenstatus
class LMZUSTAND(Enum):
    LM_AUS = 0
    LM_AN = 1
    LM_BLINKEN = 2

# HELLO
class ClientTyp(Enum):
    ZUSI = 1
    FAHRPULT = 2
HELLO = namedtuple("HELLO", ['protokollversion', 'clienttyp', 'clientname', 'clientversion'], defaults=[None, None, None, None])
llps[HELLO] = (
    LLP(PID(1), None, BasicNode),
    LLP(PID(1, 1), None, BasicNode),
    LLP(PID(1, 1, 1), 'protokollversion', ContentType.WORD),
    LLP(PID(1, 1, 2), 'clienttyp', ContentType.WORD, ClientTyp),
    LLP(PID(1, 1, 3), 'clientname', ContentType.STRING),
    LLP(PID(1, 1, 4), 'clientversion', ContentType.STRING),
)
msgidx[PID(1, 1)] = HELLO

# ACK_HELLO
ACK_HELLO = namedtuple("ACK_HELLO", ['zusiversion', 'verbindungsinfo', 'status', 'startdatum', 'protokollversion'], defaults=[None, None, None, None, None])
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

#Status NBÜ
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

#Sifa Status
class STATUS_SIFA_HUPE(Enum):
    HUPE_AUS = 0
    HUPE_WARNUNG = 1
    HUPE_ZWANGSBREMSUNG = 2
class SIFA_SCHALTER(Enum):
    SIFA_SCHALTER_EIN = 1
    SIFA_SCHALTER_AUS = 2
STATUS_SIFA = namedtuple("STATUS_SIFA", ['bauart', 'lm', 'hupe', 'hauptschalter', 'stoerschalter', 'Lufthan', 'weg'], defaults=[None, None, None, None, None, None, None])
llps[STATUS_SIFA] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x64), None, BasicNode),
    LLP(PID(2, 0x0a, 0x64, 1), 'bauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x64, 2), 'lm', ContentType.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x64, 3), 'hupe', ContentType.BYTE, STATUS_SIFA_HUPE),
    LLP(PID(2, 0x0a, 0x64, 4), 'hauptschalter', ContentType.BYTE, SIFA_SCHALTER),
    LLP(PID(2, 0x0a, 0x64, 5), 'stoerschalter', ContentType.BYTE, SIFA_SCHALTER),
    LLP(PID(2, 0x0a, 0x64, 6), 'lufthan', ContentType.BYTE, SIFA_SCHALTER),
    LLP(PID(2, 0x0a, 0x64, 7), 'weg', ContentType.SINGLE)
)
msgidx[PID(2, 0x0a, 0x64)] = SATUS_SIFA

#Staus Zugbeeinflussung
#Grundblock
ZUGB_GRUND = namedtuple("ZUGB_GRUND", ['bauart'], defaults=[None])
llps[ZUGB_GRUND] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 1), 'bauart', ContentType.STRING),
)
msgidx[PID(2, 0x0a, 0x65)] = ZUGB_GRUND
#Indusi Analogsysteme und Basisdaten
class ZUGART(Enum):
    NICHT_BESTIMMT = 1
    U = 2
    M = 3
    O = 4
    S-BAHN = 5
class SYSTEMSTATUS(Enum):
    AUSGESCHALTET = 0
    ABGESCHALTET = 1
    UNTERDRUECKT = 2
    AKTIV = 3
class ZUSTAND(Enum):
    AUSGESCHALTET = 1
    ABGESCHALTET/GESTOERT = 2
    HL_DRUCK_NIDRIG = 3
    AUFFODERUNG_ZUGDATENEINGABE = 4
    NORMALBETRIEB = 5
    FUNKTIONSPRUEFUNG = 6
    FUNKTIONSPRUEFUNG_QUTIERUNG_FEHLT = 7
class ZWANGSBREMSUNG(Enum):
    KEINE_ZWANGSBREMSUNG = 0
    WACHSAM = 1
    1000HZ = 2
    500HZ = 3
    2000HZ = 4
    KEIN_HALT_NACH_BEFREIUNG = 5
    FZ_VMAX = 6
    FUNKTIONSPRUEFUNG = 7
    500HZ_NACH_BEFREIUNG = 8
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
class HUPE(Enum):
    AUS = 0
    HUPE = 1
    ZWANGSBREMSUNG = 2
class SCHALTER(Enum):
    SCHALTER_AN = 1
    SCHALTER_AUS = 2
INDUSI_ANALOG = namedtuple("INDUSI_ANALOG", ['zugart', 'hauptschalter', 'stoerschalter', 'luftabsperhan', 'systemstatus', 'bauart', 'zustand', 'zwangsbremsung','zwangsbremsung_grund', 'lm_100HZ', 'lm_u', 'lm_m', 'lm_o', 'hupe', 'beeinflussung_1000hz', 'beeinflussung_500hz', 'beeinflussung_2000hz', 'status_lm_1000hz'], defaults=[None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
llps[INDUSI_ANALOG] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 1), 'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 7), 'hauptschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 8), 'stoerschalter', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0a), 'luftabsperhan', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0d), 'systemstatus', ContentType.BYTE, SCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0e), 'bauart', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 3), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 2), 'zustand', ContentType.WORD, ZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 3), 'zwangsbremsung', ContentType.WORD, ZWANGSBREMSUNG),
    LLP(PID(2, 0x0a, 0x65, 3, 4), 'zwangsbremsung_grund', ContentType.STRING),
    LLP(PID(2, 0x0a, 0x65, 3, 5), 'lm_100HZ',ContentType.
    LLP(PID(2, 0x0a, 0x65, 3, 6), 'lm_u', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 7), 'lm_m', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 8), 'lm_o', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 9), 'hupe', ContentType.BYTE, HUPE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2c), 'beeinflussung_1000hz', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2d), 'beeinflussung_500hz', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2e), 'beeinflussung_2000hz',  ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2f), 'status_lm_1000hz', ContentType.BYTE, LMZUSTAND)
)
msgidx[PID(2, 0x0a, 0x65, 2)] = INDUSI_ANALOG
#indusi I60R/I80/PZB90
class ZUGART(Enum):
    MUSS_NOCH_BESTIMMT_WERDEN = 1
    U = 2
    M = 3
    O = 4
    S_BAHN = 5
class MODUS(Enum):
    UNDEFINIERT = 0
    ERSATZZUGDATEN = 5
    NORMALBETRIEB = 6
class KLARTEXTMELDUNGEN(Enum):
    KEINE_MOEGLICH = 0
    MOEGLICH_ABER_NICHT_AKTIV = 1
    AKTIV = 2
    NUR_KLARTEXTMELDUNGEN = 3
class FUNKTIONSPRUEFUNG_STARTEN(Enum):
    ZUSI_SOLL_STARTEN = 1
    WURDE_QUITTIER = 2
    WURDE_NICHT_QUITTIERT = 3
class STOERSCHALTERBAURT(Enum):
    LEUCHTDRUCKTASTER = 0
    DREHSCHALTER = 1
class LM_BLINKEN_INVERS(Enum):
    AUS = 0
    AN = 1
    BLINKEND = 2
    BLINKEND_INVERS = 3


INDUSI = namedtuple("INDUSI", ['tf_nr','zn', 'brh','bra','zugart','modus','klartextmeldungen','funktionspruefung_starten','stoerschalterbaurt','lm_500hz','lm_befehl_an','lm_o','lm_m','lm_u','lm_500hz','lm_befehl'],defaults=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
llps[INDUSI] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x02), 'tf_nr', ContentTyp.String),
    LLP(PID(2, 0x0a, 0x65, 2, 0x03), 'zn', ContentTyp.String),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05,0x01), 'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05,0x02), 'bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05,0x05), 'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05,0x06), 'modus', ContentTyp.BYTE, MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x01), 'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x02), 'bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x05), 'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 0x06), 'modus', ContentTyp.BYTE, MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0B),'klartextmeldungen',ContentTyp.BYTE, KLARTEXTMELDUNGEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0C),'funktionspruefung_starten',ContentTyp.BYTE, FUNKTIONSPRUEFUNG_STARTEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0F), 'stoerschalterbaurt',ContentTyp.BYTE, STOERSCHALTERBAURT),
    LLP(PID(2, 0x0a, 0x65, 3), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0A),'lm_500hz',ContentTyp.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0B),'lm_befehl_an',ContentTyp.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x30),'lm_o',ContentTyp.BYTE, LM_BLINKEN_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x31),'lm_m',ContentTyp.BYTE, LM_BLINKEN_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x32),'lm_u',ContentTyp.BYTE, LM_BLINKEN_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x33),'lm_500hz',ContentTyp.BYTE, LMZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x34),'lm_befehl',ContentTyp.BYTE, LMZUSTAND)
)
msgidx[PID(2, 0x0a, 0x65, 2)] = INDUSI




#PZB90
class ZUSATZINFO_MELDERBILD(Enum):
    NORMALZUSTAND = 0
    1000HZ_NACH_700M = 1
    RESTREKTIV = 2
    RESTREKTIV_1000HZ = 3
    RESTREKTIV_500HZ = 4
    PRUEFABLAUF = 5
PZB90 = namedtuple("PZB90", ['zusatzinfo_melderbild'],defaults=[None])
llps[PZB90] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0C),'zusatzinfo_melderbild', ContentType.BYTE, ZUSATZINFO_MELDERBILD)
)
msgidx[PID(2, 0x0a, 0x65, 3)] = PZB90


#PZB90 S-Bahn
class LM_BLINKEN_INVERS(Enum):
    AUS = 0
    AN = 1
    BLINKEND = 2
    BLINKEND_INVERS = 3

PZB90_S_BAHN = namedtuple("PZB90_S_BAHN", ['lm_zugart_links', 'lm_zugart_65', 'lm_zugart_rechts', 'status_lm_zugart_rechts', 'status_lm_zugart_65', 'status_lm_zugart_links'],defaults=[None,None,None,None,None,None])
llps[PZB90] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x29),'lm_zugart_links',ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2a),'lm_zugart_65',ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x2b),'lm_zugart_rechts',ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 0x35),'status_lm_zugart_rechts',ContentType.BYTE,LM_BLINKEN_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x36),'status_lm_zugart_65',ContentType.BYTE,LM_BLINKEN_INVERS),
    LLP(PID(2, 0x0a, 0x65, 3, 0x37),'status_lm_zugart_links',ContentType.BYTE,LM_BLINKEN_INVERS)
)
msgidx[PID(2, 0x0a, 0x65, 3)] = PZB90_S_BAHN

#LZB
class ZUGART(Enum):
    NICHT_BESTIMMT = 1
    U = 2
    M = 3
    O = 4
class MODUS(Enum):
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
class FUNKTIONSPRUEFUNG_STARTEN(Enum):
    ZUSI_SOLL_STARTEN = 1
    WURDE_QUITTIER = 2
    WURDE_NICHT_QUITTIERT =3
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
LZB = namedtuple("LZB", ['brh','bra','zl','vmz','zugart','modus','stoerschalter','lzb_klartextmeldung','funktionspruefung_starten','stoerschalterbaurt','systemstatus','zustand','ende_verfahren','Falschfahrauftrag_status','Vorsichtsauftrag_status','zielgeschwindigkeit','zielgeschwindigkeit_status','zielweg_cir_elke','lzb_nothalt','nothalt_gesendet','status_lzb_rechnerausfall','el_auftag','melder_h','melder_e40','melder_ende','melder_b','melder_u','melder_g','melder_el','melder_v40','melder_s','melder_pruef','sollgeschwindigkeit','zielgeschwindigkeit','zielweg','melder_g_status','melder_pruef_status','cir_elke_modus','anzeigemodus','melder_h_status','melder_e40_status','melder_ende_status','melder_b_status','melder_u_status','melder_el_status','melder_v40_status','melder_s_status'],defaults=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
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
    LLP(PID(2, 0x0a, 0x65, 2, 0x04, 6), 'modus', ContentType.BYTE, MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 1), 'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 2), 'bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 3), 'zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 4), 'vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 5), 'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x05, 6), 'modus', ContentType.BYTE, MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 1), 'brh', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 2), 'bra', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 3), 'zl', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 4), 'vmz', ContentType.WORD),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 5), 'zugart', ContentType.BYTE, ZUGART),
    LLP(PID(2, 0x0a, 0x65, 2, 0x06, 6), 'modus', ContentType.BYTE, MODUS),
    LLP(PID(2, 0x0a, 0x65, 2, 0x09), 'stoerschalter', ContentType.BYTE, STOERSCHALTER),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0b), 'lzb_klartextmeldung', ContentType.BYTE, LZB_KLARTEXTMELDUNG),
    LLP(PID(2, 0x0a, 0x65, 2, 0x0c), 'funktionspruefung_starten', ContentType.BYTE, FUNKTIONSPRUEFUNG_STARTEN),
    LLP(PID(2, 0x0a, 0x65, 2, 0x10), 'stoerschalterbaurt', ContentType.BYTE, STOERSCHALTERBAURT),
    LLP(PID(2, 0x0a, 0x65, 2, 0x11), 'systemstatus', ContentType.BYTE, SYSTEMSTATUS),
    LLP(PID(2, 0x0a, 0x65, 3),None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0d), 'zustand', ContentType.WORD, ZUSTAND),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0e), None, BasicNode)
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
    LLP(PID(2, 0x0a, 0x65, 3, 0x22), 'zielgeschwindigkeit', ContentType.SINGLE),
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
msgidx[PID(2, 0x0a, 0x65, 2, 0x03)] = LZB

#ETCS

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
    LLP(PID(2, 0x0a, 0x66,0x12), 'lm_gruenschleife', ContentType.BYTE),LMZUSTAND)
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
    P+MG = 3
    R = 4
    R+MG = 5
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
    15KV_16HZ = 2
    25KV_50HZ = 3
    1500VDC = 4
    1200VDC_STROMSCHIENE_HAMBURG = 5
    3KVDC = 6
    750VDC_STROMSCHIENE_BERLIN =7
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
STATUS_ZUGVERBAND = namedtuple("STATUS_ZUGVERBANDG",['fz_dateiname', 'beschreibung', 'vorgabe_bremsstellung', 'bezeichnung_zugbeeinflussungs', 'fz_vmax', 'baureihe', 'farbgebung', 'traktionsmodus', 'stromabnehmerschaltung', 'maximaler_bremszylinder_druck', 'nvr_nr', 'sitzplaetze_1_klasse', 'sitzplaetze_2_klasse', 'fz_drehung', 'fz_gattung', 'fuehrerstandsmodus', 'fz_laenge', 'fz_masse', 'ladungsmasse', 'bremsbaurt', 'bremsmasse_handbremse', 'aktive_bremsmasse', 'aktive_bremssmasse_inkl_dynamische', 'anzahl_achsen', 'bauart_batteriehauptschalter', 'bauart_stromabnehmerwahlschalter', 'bremsstellung', 'zugehoerige_Bremsmasse', 'bremsstellung_wirksam', 'bezeichnung_bremsbaurt', 'grafik_seitenansicht', 'hbl', 'fz_verbund', 'lokstatus', 'interne_fz_nr', 'gefahrgutkenzeichen', 'bezeichnung_tuersystem', 'bauart_tuerwachlschalter', 'antriebstyp', 'stromtyp_antriebssystem', 'antrieb_aktiv', 'bremstyp', 'stromtyp_bremse', 'bremse_aktiv', 'lastabhaehnige_bremse'],defaults=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
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
    LLP(PID(2, 0x0a, 0x8e, 0x01, 0x1d),'grafik_seitenansicht', ContentType.DATEI),
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

LM_ZUSIDISPLAY = namedtuple("LM_ZUSIDISPLAY", ['name', 'modus', 'breite', 'höhe'], defaults=[None, None, None, None])
llps[LM_ZUSIDISPLAY] = (
    LLP(PID(2), None, BasicNode),
    LLP(PID(2, 0x0a), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9, 0x01), None, BasicNode),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x01), 'name', ContentType.STRING),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x02), 'modus', ContentType.BYTE, RAHMEN_MODUS),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x03), 'breite', ContentType.WORD),
    LLP(PID(2, 0x0a, 0xa9, 0x01, 0x04), 'höhe', ContentType.WORD),
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
    LLP(PID(2, 0x0a, 0xab,0x01, 0x01),'bremszylinderdruck', ContentType.SIGNLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x02),'hll_druck',ContentType.SIGNLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x03),'zugkraft',ContentType.SIGNLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x04),'motordrehzahl_1',ContentType.SIGNLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x05),'maximal_moegliche_zugkraft',ContentType.SIGNLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x06),'maximale_dynamische_bremskraft',ContentType.SIGNLE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x07),'absperhaehne_hll',ContentType.BYTE),
    LLP(PID(2, 0x0a, 0xab,0x01, 0x0a),'motordrehzahl_2',ContentType.SIGNLE),
    LLP(PID(2, 0x0a, 0xab,0x01), None, BasicNode)
)
msgidx[PID(2, 0x0a, 0xab,0x01)] = STATUS_ZUG_FAHRDATEN













