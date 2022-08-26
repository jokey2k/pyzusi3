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
    UNTERDRÜCKT = 2
    AKTIV = 3
class ZUSTAND(Enum):
    AUSGESCHALTET = 1
    ABGESCHALTET/GESTOERT = 2
    HL_DRUCK_NIDRIG = 3
    AUFFODERUNG_ZUGDATENEINGABE = 4
    NORMALBETRIEB = 5
    FUNKTIONSPRÜFUNG = 6
    FUNKTIONSPRÜFUNG_QUTIERUNG_FEHLT = 7
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
INDUSI_ANALOG = namedtuple("INDUSI_ANALOG", ['zugart', 'hauptschalter', 'stoerschalter', 'luftabsperhan', 'systemstatus', 'bauart', 'zustand', 'zwangsbremsung',
'zwangsbremsung_grund', 'lm_100HZ', 'lm_u', 'lm_m', 'lm_o', 'hupe', 'beeinflussung_1000hz', 'beeinflussung_500hz', 'beeinflussung_2000hz', 'status_lm_1000hz'], defaults=[None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
llps[INDUSI_ANALOG] = (
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
    LLP(PID(2, 0x0a, 0x65, 3, 2c), 'beeinflussung_1000hz', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 2d), 'beeinflussung_500hz', ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 2e), 'beeinflussung_2000hz',  ContentType.BYTE),
    LLP(PID(2, 0x0a, 0x65, 3, 2f), 'status_lm_1000hz', ContentType.BYTE, LMZUSTAND)
)
msgidx[PID(2, 0x0a, 0x65, 2)] = INDUSI_ANALOG
#LZB

class ZUGARTEnum):
    NICHT_BESTIMMT = 1
    U = 2
    M = 3
    O = 4
class MODUSEnum):

class STOERSCHALTEREnum):
class LZB_KLARTEXTMELDUNGEnum):
class FUNKTIONSPRUEFUNG_STARTENEnum):
class STOERSCHALTERBAURTEnum):
class SYSTEMSTATUSEnum):
class ZUSTANDEnum):
class ENDE_VERFAHRENEnum):
class FALSCHFAHRAUFTRAG_STATUSEnum):
class VOORSICHTSAUFTRAG_STATUSEnum):
class ZIELGESCHWINDIGKEIT_STATUSEnum):
class LZB_NOTHALTEnum):
class NOTHALT_GESENDETEnum):
class STATUS_LZB_RECHNERAUSFALLEnum):
class EL_AUFTAGEnum):
class CIR_ELKE_MODUSEnum):
class ANZEIGEMODUSEnum):






LZB = namedtuple("LZB", [
    'brh',
    'bra',
    'zl',
    'vmz',
    'zugart',
    'modus',
    'stoerschalter',
    'lzb_klartextmeldung',
    'funktionspruefung_starten',
    'stoerschalterbaurt',
    'systemstatus',
    'zustand',
    'ende_verfahren',
    'Falschfahrauftrag_status',
    'Voorsichtsauftrag_status',
    'zielgeschwindigkeit',
    'zielgeschwindigkeit_status',
    'zielweg_cir_elke',
    'lzb_nothalt',
    'nothalt_gesendet',
    'status_lzb_rechnerausfall',
    'el_auftag',
    'melder_h',
    'melder_e40',
    'melder_ende',
    'melder_b',
    'melder_u',
    'melder_g',
    'melder_el',
    'melder_v40',
    'melder_s',
    'melder_pruef',
    'sollgeschwindigkeit',
    'zielgeschwindigkeit',
    'zielweg',
    'melder_g_status',
    'melder_pruef_status',
    'cir_elke_modus',
    'anzeigemodus',
    'melder_h_status',
    'melder_e40_status',
    'melder_ende_status',
    'melder_b_status',
    'melder_u_status',
    'melder_el_status',
    'melder_v40_status',
    'melder_s_status',
],
defaults=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None
          ]

llps[INDUSI_ANALOG] = (
    LLP(PID(2, 0x0a, 0x65, 2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x03), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 2, 0x03, 1),'brh', ContentType.WORD
    LLP(PID(2, 0x0a, 0x65, 2, 0x03, 2) 'bra', ContentType.WORD
    LLP(PID(2, 0x0a, 0x65, 2, 0x03, 3)  'zl', ContentType.WORD
    LLP(PID(2, 0x0a, 0x65, 2, 0x03, 4)  'vmz', ContentType.WORD
    LLP(PID(2, 0x0a, 0x65, 2, 0x03, 5)  'zugart', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 2, 0x03, 6)'modus', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 2, 0x09)'stoerschalter', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 2, 0x0b) 'lzb_klartextmeldung', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 2, 0x0c) 'funktionspruefung_starten', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 2, 0x10)'stoerschalterbaurt', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 2, 0x11)'systemstatus', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3),None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x0d'zustand', ContentType.WORD
    LLP(PID(2, 0x0a, 0x65, 3, 0x0e), None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x0e, 1)'ende_verfahren', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x0f), None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x10), None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x10, 1)'Falschfahrauftrag_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x11, None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x11, 1)'Voorsichtsauftrag_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x12), None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x13), None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 1)'zielgeschwindigkeit', ContentType.SINGLE
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 2)'zielgeschwindigkeit_status', ContentType.WORD
    LLP(PID(2, 0x0a, 0x65, 3, 0x13, 3)'zielweg_cir_elke', ContentType.SINGLE
    LLP(PID(2, 0x0a, 0x65, 3, 0x14) None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x14, 1)'lzb_nothalt', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x14, 2)'nothalt_gesendet', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x15, None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x15, 1)'status_lzb_rechnerausfall', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x16), None, BasicNode)
    LLP(PID(2, 0x0a, 0x65, 3, 0x16, 1)'el_auftag', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x17)'melder_h', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x18)'melder_e40', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x19)'melder_ende', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x1a)'melder_b', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x1b)'melder_u', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x1c)'melder_g', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x1d)'melder_el', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x1e)'melder_v40', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x1f)'melder_s', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x20)'melder_pruef', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x21)'sollgeschwindigkeit', ContentType.SINGLE
    LLP(PID(2, 0x0a, 0x65, 3, 0x22)'zielgeschwindigkeit', ContentType.SINGLE
    LLP(PID(2, 0x0a, 0x65, 3, 0x23)'zielweg', ContentType.SINGLE
    LLP(PID(2, 0x0a, 0x65, 3, 0x24)'melder_g_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x25)'melder_pruef_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x26)'cir_elke_modus', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x27)'anzeigemodus', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x28), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,1), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,2), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,3), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,4), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x28,5), None, BasicNode),
    LLP(PID(2, 0x0a, 0x65, 3, 0x38)'melder_h_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x39)'melder_e40_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x3a)'melder_ende_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x3b)'melder_b_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x3c)'melder_u_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x3d)'melder_el_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x3e)'melder_v40_status', ContentType.BYTE
    LLP(PID(2, 0x0a, 0x65, 3, 0x3d)'melder_s_status', ContentType.BYTE