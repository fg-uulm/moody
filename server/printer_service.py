import instax
import socketio
import uuid
import os
import binascii
import json
import time
import sys
import traceback

SOCKETIO_ROLE = "client" 
SOCKETIO_SERVER_ADDRESS = "10.0.0.25"
SOCKETIO_SERVER_PORT = 8099

connected_printer = "none"
info = None
printer_obj = None
printing = False

# SocketIO setup
sio = socketio.Client()
sio.connect('http://'+SOCKETIO_SERVER_ADDRESS+':'+str(SOCKETIO_SERVER_PORT))

# Printer progress callback
def printProgress(count, total, status=''):
    global connected_printer
    print(status)
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)   
    print("Progress: "+str(percents)+" %")
    sio.emit('print_progress',{"printer":connected_printer, "percent":percents})

#def recoverFromFailure():


# SocketIO handlers - TODO
@sio.on('printjob')
def on_printjob(data):
    global printer_obj
    global connected_printer
    global printing
    print('Print job received')
    printing = True

    try:
        printer_obj = instax.SP2(port=8080, pinCode=4782, timeout=10)

        info = printer_obj.getPrinterInformation()
        sio.emit('printer_status', json.dumps(info))
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
        printer_obj.printPhoto(encodedImage, printProgress)
        sio.emit('print_success',{"printer":connected_printer})
        print("Printing on "+connected_printer+" successful")
        printing = False
        #os.remove('/tmp/'+tmp_name+'.jpg')
        print("Removing file successful")
        info = printer_obj.getPrinterInformation()
        sio.emit('printer_status', json.dumps(info))
    except:
        print(traceback.format_exc())
        print("Fail: Printing fail, starting full recovery")
        sio.emit("broadcast", {"method":"printer_reset","payload":"null"})

@sio.on('wificonnect')
def on_wificonnect(data):
    global connected_printer
    connected_printer = "None"
    print("Not connected to printer wifi")

@sio.on('wificonnect_success')
def on_wificonnect_success(data):
    global printer_obj
    global connected_printer
    print("Connected to printer "+data["ssid"]+" wifi, getting info...")
    connected_printer = "None"
    try:
        print("Trying to connect...")
        time.sleep(20)

        #if(printer_obj != None):
            #printer_obj.close()
        # Instax setup / status
        printer_obj = instax.SP2(port=8080, pinCode=4782, timeout=10)
        info = printer_obj.getPrinterInformation()
        print(info)
        connected_printer = data["ssid"]
        sio.emit('printer_connected', connected_printer)
        sio.emit('printer_status', json.dumps(info))            
        print("Connected")
    except:
        print(traceback.format_exc())
        print("Fail: Trying again in some secs")

@sio.on('wificonnect_fail')
def on_wificonnect_fail(data):
    print("Not connected to any printer")
    connected_printer = "None"

@sio.on('CLIENT_LIST')
def on_client_list(data):
    global connected_printer
    printer_obj = instax.SP2(port=8080, pinCode=4782, timeout=10)
    info = printer_obj.getPrinterInformation()
    print(info)
    sio.emit('printer_connected', connected_printer)
    sio.emit('printer_status', json.dumps(info))            
    print("Connected")

@sio.on('request_status')
def on_request_status(data):
    return
    print("Status request received")
    global printer_obj
    global connected_printer
    global printing

    if(connected_printer == "None" or printing == True): 
        print("Cancel status request")
        return

    try:
        print("Status request from printer")
        info = printer_obj.getPrinterInformation()
        print(info)
        sio.emit('printer_connected', connected_printer)
        sio.emit('printer_status', json.dumps(info))
    except:
        print("Status failed")

# startup
on_wificonnect_success({"ssid":"silver"})