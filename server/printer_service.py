import instax
import socketio

SOCKETIO_ROLE = "client" 
SOCKETIO_SERVER_ADDRESS = "127.0.0.1"
SOCKETIO_SERVER_PORT = 8099

# SocketIO setup
sio = socketio.Client()
sio.connect('http://'+SOCKETIO_SERVER_ADDRESS+':'+str(SOCKETIO_SERVER_PORT))

# Instax setup
myInstax = instax.SP2(ip="192.168.0.251", port=8080, pinCode=4782,
                      timeout=10)
info = myInstax.getPrinterInformation()

# SocketIO handlers - TODO
@sio.on('printjob')
def on_message(data):
    print('Print job received')