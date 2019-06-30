from pysnmp.smi.rfc1902 import *
from pysnmp.hlapi import *


def snmp_get():
    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(SnmpEngine(),
            CommunityData('private'),
            UdpTransportTarget(('10.', 161)),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.4.1.25506.8.35.2.1.1.1.3.91'),
                      OctetString(b'\x00\x40\xC0\x00\x00\x80\x0B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
        )
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
    return varBinds


snmp_get()

#