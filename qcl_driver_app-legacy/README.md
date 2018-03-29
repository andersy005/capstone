# Quantum Cascase Laser Driver UI 

This application is built with [pyqtgraph](http://www.pyqtgraph.org/documentation/index.html) and [json-ipc](https://github.com/dhylands/json-ipc) libraries.

## Files

| File            | Description |
| --------------- | ----------- |
| json_pkt.py     | Implements JSON Packet parsing and sending. |
| dump_mem.py     | Utility function for dumping memory. |
| app_launcher.py | Main client app which runs on the host. |
| serial_port.py  | Host serial interface over UART. |