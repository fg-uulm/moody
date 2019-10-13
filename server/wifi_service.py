import socketio
import subprocess
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni

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
def on_wificonnect(data):
    print('SIO: Connect to wifi '+data)

    # create supplicant file
    try:
        sio.emit('printer_connected', 'None')
        # Delete old file
        print("Delete old file")
        proc = subprocess.Popen('sudo rm /etc/wpa_supplicant/wpa_supplicant.conf',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(5)
        print("Deleted.")

        # Copy respective template to supp
        print("Installing new file")
        if(data == "silver"):
            proc = subprocess.Popen('sudo cp /etc/wpa_supplicant/wpa_supplicant.conf.silver /etc/wpa_supplicant/wpa_supplicant.conf',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(2)
        elif(data  == "gold"):
            proc = subprocess.Popen('sudo cp /etc/wpa_supplicant/wpa_supplicant.conf.gold /etc/wpa_supplicant/wpa_supplicant.conf',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(2)
        print("Installed.")

        # reset wifi PHY and everything
        proc = subprocess.Popen('sudo /etc/init.d/dhcpcd restart',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(5)
        print("DHCPCD restarted.")

        # reset dhcp
        proc = subprocess.Popen('sudo dhclient -v -r wlan0',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(5)    
        print("DHCP Lease released.")

        # renew dhcp
        proc = subprocess.Popen('sudo dhclient -v wlan0',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(15)    
        print("DHCP Lease renewed.")

        # reset wifi PHY, for real
        proc = subprocess.Popen('sudo ifconfig wlan0 down && sudo ifconfig wlan0 up',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(5)
        print("ifupdown.")

        ipAddr = ni.ifaddresses('wlan0')[AF_INET][0]['addr'];
        print("New IP is "+ipAddr)

        sio.emit("wificonnect_success", {"ssid": data, "ip": ipAddr});
        print("Notification sent")

    except Exception as e:
        print("Installing failed: "+str(e))
        sio.emit("wificonnect_fail", {"ssid": data})


# TEST
#on_wificonnect("gold")