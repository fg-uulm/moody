import socketio
import subprocess

SOCKETIO_ROLE = "client" 
SOCKETIO_SERVER_ADDRESS = "127.0.0.1"
SOCKETIO_SERVER_PORT = 8099

sio = socketio.Client()
sio.connect('http://'+SOCKETIO_SERVER_ADDRESS+':'+str(SOCKETIO_SERVER_PORT))

# SocketIO handlers
@sio.event
def connect():
    print("SIO: Connected!")

@sio.on('wificonnect')
def on_message(data):
    print('SIO: Connect to wifi '+data)

    # create supplicant file
    try:
        # Delete old file
        print("Delete old file")
        proc = subprocess.Popen('sudo rm /etc/wpa_supplicant/wpa_supplicant.conf',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()
        print("Deleted.")

        # Copy respective template to supp
        print("Installing new file")
        if(data == "silver"):
            proc = subprocess.Popen('sudo cp /etc/wpa_supplicant/wpa_supplicant.conf.silver /etc/wpa_supplicant/wpa_supplicant.conf',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()
        elif(data  == "gold"):
            proc = subprocess.Popen('sudo cp /etc/wpa_supplicant/wpa_supplicant.conf.gold /etc/wpa_supplicant/wpa_supplicant.conf',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()
        print("Installed.")
    except Exception as e:
        print("Installing failed: "+str(e))

    # reset wifi PHY and everything
    proc = subprocess.Popen('sudo /etc/init.d/dhcpcd restart',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()
    print("DHCPCD restarted.")

    # reset dhcp
    proc = subprocess.Popen('sudo dhclient -v -r wlan0',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()    
    print("DHCP Lease released.")

    # renew dhcp
    proc = subprocess.Popen('sudo dhclient -v wlan0',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()    
    print("DHCP Leaser renewed.")

    sio.emit("wificonnected", data)


# TEST
on_message("silver")