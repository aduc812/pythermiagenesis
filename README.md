# pythermiagenesis
A python library for Thermia Inverter/Mega heatpumps

This library communicates with the device using Modbus TCP or Modbus RTU.
Set BMC to Modbus TCP on your heat pump to enable TCP communication through this library.

## Install
To install modbus TCP option via pyModbusTCP:
```
pip install "pythermiagenesis[TCP] @ git+https://github.com/aduc812/pythermiagenesis.git"
```

To install modbus RTU option via pymodbus:
```
pip install "pythermiagenesis[RTU] @ git+https://github.com/aduc812/pythermiagenesis.git"
```