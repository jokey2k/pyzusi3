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