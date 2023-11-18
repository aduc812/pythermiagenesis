import asyncio
import logging
from sys import argv

from pythermiagenesis import ThermiaGenesis
from pythermiagenesis.const import ATTR_COIL_ENABLE_TAP_WATER, ATTR_HOLDING_EXTERNAL_ADDITIONAL_HEATER_START

# printer IP address/hostname
HOST = "10.0.20.8"
PORT = 502
logging.basicConfig(level=logging.DEBUG)


async def main():
    host = argv[1] if len(argv) > 1 else HOST
    port = argv[2] if len(argv) > 2 else PORT
    kind = argv[3] if len(argv) > 3 else "inverter"
    prot = argv[4] if len(argv) > 4 else "TCP"
    
    # RTU arguments; leave default for TCP connection  
    baud = int(argv[5]) if len(argv) > 5 else 19200
    btsz = int(argv[6]) if len(argv) > 6 else 8
    prty =     argv[7]  if len(argv) > 7 else "E"
    stbt = int(argv[8]) if len(argv) > 8 else 1
    echo = bool(argv[9])if len(argv) > 9 else False

    # argument kind: inverter - for Diplomat Inverter
    #                mega     - for Mega
    # argument prot: "TCP"    - for TCP/IP
    #                "RTU"    - for RTU over RS485

    thermia = ThermiaGenesis(host, protocol = prot,  port=port, kind=kind, delay=0.15,
    baudrate=baud, bytesize=btsz, parity=prty, stopbits=stbt, handle_local_echo=echo)

    try:
        await thermia.async_set(ATTR_COIL_ENABLE_TAP_WATER, False)
        #await thermia.async_set(ATTR_COIL_ENABLE_TAP_WATER, True)
        #await thermia.async_set(ATTR_HOLDING_EXTERNAL_ADDITIONAL_HEATER_START, -5)
    except (ConnectionError) as error:
        print(f"{error}")
        return

    if thermia.available:
        print(f"Data available: {thermia.available}")
        print(f"Model: {thermia.model}")
        print(f"Firmware: {thermia.firmware}")
        print(f"Sensors data: {thermia.data}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

