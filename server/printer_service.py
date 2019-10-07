import instax
import socketio
import uuid
import os
import binascii

SOCKETIO_ROLE = "client" 
SOCKETIO_SERVER_ADDRESS = "127.0.0.1"
SOCKETIO_SERVER_PORT = 8099

connected_printer = "none"
info = None
printer_obj = None

# SocketIO setup
sio = socketio.Client()
sio.connect('http://'+SOCKETIO_SERVER_ADDRESS+':'+str(SOCKETIO_SERVER_PORT))

# Printer progress callback
def printProgress(count, total, status=''):
    print(status)
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)   
    print("Progress: "+percents+" %")
    sio.emit('print_progress',{"printer":connected_printer, "percent":percents})

# SocketIO handlers - TODO
@sio.on('printjob')
def on_printjob(data):
    print('Print job received')
    # save data to tmp jpg
    tmp_name = str(uuid.uuid4())
    f = open('/tmp/'+tmp_name+'.jpg', 'w+b')
    binary_formatted = bytearray(binascii.a2b_base64(data))
    f.write(binary_formatted)
    f.close()

    # prepare for printing
    instaxImage = instax.InstaxImage(type=2)
    instaxImage.loadImage('/tmp/'+tmp_name+'.jpg')
    instaxImage.convertImage()
    # Save a copy of the converted bitmap (debugging)
    instaxImage.saveImage("/tmp/test.bmp")
    # Preview the image that is about to print
    #instaxImage.previewImage()
    encodedImage = instaxImage.encodeImage()
    print("Sending print command for "+'/tmp/'+tmp_name+'.jpg')
    #myInstax.printPhoto(encodedImage, printProgress)
    sio.emit('print_success',{"printer":connected_printer})
    print("Printing on "+connected_printer+" successful")
    os.remove('/tmp/'+tmp_name+'.jpg')
    print("Removing file successful")

@sio.on('wificonnect_success')
def on_wificonnect_success(data):
    print("Connected to printer "+data["ssid"]+", getting info...")
    connected_printer = data["ssid"]
    # Instax setup / status
    printer_obj = instax.SP2(port=8080, pinCode=4782, timeout=10)
    info = printer_obj.getPrinterInformation()
    print(info)

@sio.on('wificonnect_fail')
def on_wificonnect_fail(data):
    print("Not connected to any printer")
    connected_printer = "none"