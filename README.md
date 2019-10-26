# moody
Moody, the moody photo booth

# Usage

Vue Application

```npm run serve```

Distributed Microservices

```nodemon <microservice-name>.js```


or using PM2


```pm2 start <microservice-name>.js```

```pm2 start --interpreter python3 --interpreter-args -u <microservice-name>.py```


# Currently available microservices
* alsa-vumeter.js => Listens to local mic through ALSA and sends audio level messages (RPi)
* ceiling_cam_service.py => Provides video stream for ceiling camera (RPi with PiCam)
* coin_service.js => Connects to coin receptor and sends messages when coins are inserted (RPi)
* force_print_service.py => Connects to printer via instax lib and fwds printjob messages to printer (NEW version, RPi)
* light_control_service.js => Receives light control messages (flash, level) and sends them through DMX hardware (RPi tty)
* max_to_light.js => Connects to MaxMSP to get audio levels, forwards them as audio level messages into the moody system (Win)
* outdoor_cam_service.py => Provides video stream for outdoor camera (RPi with PiCam)
* printer_service.py => Connects to printer via instax lib and fwds printjob messages to printer (OLD version, not used, RPi)
* ptt_to_max.js => Receives PTT messages from UI / video feed UI and sends them to MaxMSP through socket (Win)
* save_picture_service.js => Listens to printjobs and taken pictures and saves the pictures in it to hard disk (Win)
* sio_master.js => Socket.IO master service, the one all others connect / subscribe to (RPi, Win)
* slr_cam_service.py => Provides video stream for SLR camera and methods for taking photographs (RPi with Canon 60D)
* wifi_service.py => Reconfigures WiFi on the fly to connect to multiple printers (RPi) 
