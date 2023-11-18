import logging

_LOGGER = logging.getLogger(__name__)

class ThermiaException(Exception):
    def __init__(self, code=None, *args, **kwargs):
        self.message = ""
        super().__init__(*args, **kwargs)
        if code is not None:
            self.code = code
            if isinstance(code, str):
                self.message = self.code
                return

class ThermiaConnectionError(ThermiaException):
    pass

def ThermiaModbusClient(*args, **kwargs):  
    """factory that returns classes from different modbus PHY's and libraries"""
    protocol = kwargs.pop('protocol', 'TCP')
    
    if (protocol == 'TCP'):
        return ThermiaModbusTCPLiteClient(*args, **kwargs)

    elif (protocol == "RTU"):
        return ThermiaModbusRTUClient (*args, **kwargs)
    else :
        _LOGGER.error(f'Unknown protocol: {self._protocol}')
        return None



class ThermiaModbusTCPLiteClient():
    """instance of pyModbusTCP.client"""
    def __init__ (self, host, port=502, unit_id=1, auto_open=True):
        from pyModbusTCP.client import ModbusClient as pyModbusTCPClient
        self._host = host
        self._port = port
        self._client = pyModbusTCPClient(host, port=port, unit_id=unit_id, auto_open=auto_open)
        self._last_error = None
    
    def assure_connecion(self):
        if not self._client.is_open():
            _LOGGER.info("Attempting to open a Modbus TCP connection to %s:%s",  self._host, self._port)
            if not self._client.open():
                raise ThermiaConnectionError(f"Failed to connect to {self._host}:{self._port}")
    def word_list_to_long(self, regs):
        from pyModbusTCP.utils import word_list_to_long as pyModbusTCP_word_list_to_long
        return pyModbusTCP_word_list_to_long(regs)

    # all other arributes we return from _client as is
    def __getattr__(self, value):
        print (f"calling {type(self._client)}.{value}") 
        return getattr(self._client, value)

class ThermiaModbusRTUClient():
    """instance of pyModbus RTU client"""

    def __init__(self, host=1, port = "/dev/serial0",  baudrate=19200, bytesize=8, 
                parity="E", stopbits=1, handle_local_echo=False):

        import pymodbus.client as ModbusClientRTU
        from  pymodbus.framer.rtu_framer import ModbusRtuFramer as rtuframer
        from pymodbus.exceptions import ModbusException
        self._port = port # serial port device, e.g. "/dev/serial0"
        self._host = host # slave address in Modbus RTU calls
        self._client = ModbusClientRTU.AsyncModbusSerialClient(
                port, 
                framer=rtuframer,
                #timeout=10,
                #retries=3,
                # retry_on_empty=False,
                # close_comm_on_error=False,.
                # strict=True,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits,
                handle_local_echo=handle_local_echo
            )

    async def assure_connecion(self):
        if not (client.connected) :
            _LOGGER.info(f"Attempting to open a Modbus RTU serial port {self._port}")
            if not await self._client.connect():
                raise ThermiaConnectionError(f"Failed to open port {self._port}")

    async def write_single_coil(self, address, value):
        from pymodbus.exceptions import ModbusException
        try:
            rr = await client.read_coils(address, value, slave = self._host)
        except ModbusException as exc:
            _LOGGER.error(f"ERROR: exception in pymodbus {exc}")
            self._last_error = 1 #exc
        if rr.isError():
            _LOGGER.error("ERROR: pymodbus returned an error!")
            raise ModbusException("ERROR: pymodbus returned an error!")
        return rr

    async def write_single_register(self, address, value):
        from pymodbus.exceptions import ModbusException
        try:
            rr = await self._client.write_register(address, value,  slave = self._host)
        except ModbusException as exc:
            _LOGGER.error(f"ERROR: exception in pymodbus {exc}")
            self._last_error = 1 #exc
        if rr.isError():
            _LOGGER.error("ERROR: pymodbus returned an error!")
            raise ModbusException("ERROR: pymodbus returned an error!")
        return rr

    async def read_coils(self, start_address, length):
        from pymodbus.exceptions import ModbusException
        try:
            rr = await self._client.read_coils(start_address, length, slave = self._host)
        except ModbusException as exc:
            _LOGGER.error(f"ERROR: exception in pymodbus {exc}")
            self._last_error = 1# exc
            return None
        if rr.isError():
            _LOGGER.error("ERROR: pymodbus returned an error!")
            self._last_error = 1# ModbusException("ERROR: pymodbus returned an error!")
            return None
        return rr.bits

    async def read_discrete_inputs(self, start_address, length):
        from pymodbus.exceptions import ModbusException
        try:
            rr =  await self._client.read_discrete_inputs(start_address, length, slave = self._host)
        except ModbusException as exc:
            _LOGGER.error(f"ERROR: exception in pymodbus {exc}")
            self._last_error = 1# exc
            return None
        if rr.isError():
            _LOGGER.error("ERROR: pymodbus returned an error!")
            self._last_error = 1# ModbusException("ERROR: pymodbus returned an error!")
            return None
        return rr.bits

    async def read_input_registers(self, start_address, length):
        from pymodbus.exceptions import ModbusException
        try:
            rr =  await self._client.read_input_registers(start_address, length, slave = self._host)
        except ModbusException as exc:
            _LOGGER.error(f"ERROR: exception in pymodbus {exc}")
            self._last_error = 1# exc
            return None
        if rr.isError():
            _LOGGER.error("ERROR: pymodbus returned an error!")
            self._last_error = 1# ModbusException("ERROR: pymodbus returned an error!")
            return None
        return rr.registers

    async def read_holding_registers(self, start_address, length):
        from pymodbus.exceptions import ModbusException
        try:
            rr =  await self._client.read_holding_registers(start_address, length, slave = self._host)
        except ModbusException as exc:
            _LOGGER.error(f"ERROR: exception in pymodbus {exc}")
            self._last_error = 1# exc
            return None
        if rr.isError():
            _LOGGER.error("ERROR: pymodbus returned an error!")
            self._last_error = 1# ModbusException("ERROR: pymodbus returned an error!")
            return None
        return rr.registers

    def last_error(self):
        return self._last_error

    def word_list_to_long(self, regs):
        output = []
        for i in range (len(regs)/2):
            val=self._client.convert_from_registers(regs[i*2],self._client.DATATYPE.INT32)
            output.append(val)
        return output

    # all other arributes we return from _client as is
    def __getattr__(self, value):
        print (f"calling {type(self._client)}.{value}") 
        return getattr(self._client, value)
    