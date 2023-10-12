import asyncio
from ping3 import ping, verbose_ping
from pysnmp.hlapi import *

target_ip = '203.199.243.75'
community = 'Test-MaaS'


def snmpwalk():
    # SNMP parameters
    port = 161  # SNMP port (default is 161)

    # SNMP walk operation
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community,mpModel=1,contextEngineId=None),
        UdpTransportTarget((target_ip, port)),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB','sysDescr',0))
    )

    # Perform the SNMP walk
    for (errorIndication, errorStatus, errorIndex, varBinds) in iterator:
        if errorIndication:
            print(f"SNMP walk error: {errorIndication}")
            break
        elif errorStatus:
            print(f"SNMP walk error: {errorStatus}")
            break
        else:
            for varBind in varBinds:
                print(f"{varBind[0]} = {varBind[1]}")

try:
    snmpwalk()
except Exception as e:
    print(f"An error occurred: {e}")

def icmpping(target_ip):
    response_time = ping(target_ip)
    if response_time is not None:
        print(f"Response time: {response_time} ms")
    else:
        print("Host is unreachable")
    verbose_ping(target_ip)


# Perform ICMP ping
icmpping(target_ip)

