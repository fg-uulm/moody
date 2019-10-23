import socketio
import subprocess
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import time

SOCKETIO_ROLE = "client" 
SOCKETIO_SERVER_ADDRESS = "10.0.0.25"
SOCKETIO_SERVER_PORT = 8099

sio = socketio.Client()
sio.connect('http://'+SOCKETIO_SERVER_ADDRESS+':'+str(SOCKETIO_SERVER_PORT))


def reconnectPhy(data):
    # create supplicant file
    try:
        wifisuccess = False
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
        return True

    except Exception as e:
        print("Installing failed / PHY failed: "+str(e))
        sio.emit("wificonnect_fail", {"ssid": data})
        sio.emit("log", "wificonnect_fail PHY")
        return False


def reconnectIP(data):
    # renew dhcp
    try:
        proc = subprocess.Popen('sudo dhclient -v wlan0',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(15)    
        print("DHCP Lease renewed.")

        # reset wifi PHY, for real
        proc = subprocess.Popen('sudo ifconfig wlan0 down && sudo ifconfig wlan0 up',shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait(5)
        print("ifupdown.")

        time.sleep(5)

        ipAddr = ni.ifaddresses('wlan0')[AF_INET][0]['addr'];
        print("New IP is "+ipAddr)
        
        return True
    except Exception as e:
        print("Installing failed / IP failed: "+str(e))
        sio.emit("wificonnect_fail", {"ssid": data})
        sio.emit("log", "wificonnect_fail IP")
        return False

# SocketIO handlers
@sio.event
def connect():
    print("SIO: Connected!")

@sio.on('printer_reset')
def on_printer_reset(data):
    time.sleep(5)
    sio.emit("broadcast", {"method":"wificonnect", "payload":"silver"})

@sio.on('wificonnect')
def on_wificonnect(data):
    print('SIO: Connect to wifi '+data)
    ipAddr = "placeholder"

    if(reconnectPhy(data)):
        success = False
        count = 0
        while(not success):
            count = count + 1
            success = reconnectIP(data)
            print("Fail: Wait period "+str(count))
            time.sleep(count*count)
            if(count > 0):
                break

        if(success):        
            # Done, notify    
            sio.emit("wificonnect_success", {"ssid": data, "ip": ipAddr});
            sio.emit('printer_connected', data)
            print("Success - notification sent")
        else:
            # Done, notify    
            sio.emit("wificonnect_fail", {"ssid": data, "ip": ipAddr});
            if(data == "silver"):
                otherWifi = "gold"
            else:
                otherWifi = "silver"

            sio.emit("broadcast", {"method":"wificonnect", "payload":otherWifi});
            print("Fail - notification sent, connecting to other wifi")


# TEST
#on_wificonnect("gold")
