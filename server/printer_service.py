import instax
import socketio

SOCKETIO_ROLE = "client" 
SOCKETIO_SERVER_ADDRESS = "127.0.0.1"
SOCKETIO_SERVER_PORT = 8099

connected_printer = "none"
info = None
printer_obj = None

# SocketIO setup
sio = socketio.Client()
sio.connect('http://'+SOCKETIO_SERVER_ADDRESS+':'+str(SOCKETIO_SERVER_PORT))

# SocketIO handlers - TODO
@sio.on('printjob')
def on_printjob(data):
    print('Print job received')

@sio.on('wificonnect_success')
def on_wificonnect_success(data):
    print("Connected to printer "+data+", getting info...")
    connected_printer = data
    # Instax setup
    printer_obj = instax.SP2(ip="192.168.0.251", port=8080, pinCode=4782, timeout=10)
    info = printer_obj.getPrinterInformation()
    print(info)

@sio.on('wificonnect_fail')
def on_wificonnect_fail(data):
    print("Not connected to any printer")
    connected_printer = "none"