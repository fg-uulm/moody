import io
import os
import sys
import picamera
import logging
import socketserver
import urllib
import json
import math
import time
import threading
import engineio
import socketio
import eventlet
import platform
import gphoto2 as gp
import binascii

from io import BytesIO
from threading import Condition
from http import server
from PIL import Image

SOCKETIO_ROLE = "client" 
# SOCKETIO_SERVER_ADDRESS = "192.168.2.90"
SOCKETIO_SERVER_ADDRESS = "192.168.2.192"
SOCKETIO_SERVER_PORT = 8099

# Class encapsulating main camera application logic
class CameraControl():
    lock = threading.RLock()

    # Clamping Helper
    @staticmethod
    def clamp(n, minn, maxn):
        return max(min(maxn, n), minn)

    # Float comparison helper
    @staticmethod
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.02):
        if rel_tol < 0 or abs_tol < 0:
            raise ValueError("tolerances must be non-negative")

        if a == b:
            return True

        if math.isinf(a) or math.isinf(b):
            return False

        diff = math.fabs(b - a)
        result = (((diff <= math.fabs(rel_tol * b)) or
                   (diff <= math.fabs(rel_tol * a))) or
                  (diff <= abs_tol))
        return result

    # Set absolute crop from json
    @staticmethod
    def setAbsolutePosition(abspos):
        crop_to_apply = json.loads(abspos)
        logging.info("Applying absolute crop: "+str(crop_to_apply))
        current_crop = list(camera.crop)
        for idx,coord in enumerate(current_crop):
            current_crop[idx] = CameraControl.clamp(crop_to_apply[idx],0.0,1.0)                 
        camera.crop = current_crop
        return current_crop

    # Set relative crop from json
    @staticmethod
    def setRelativePosition(relpos):
        success = False
        crop_to_apply = json.loads(relpos)
        logging.info("Applying relative crop: "+str(crop_to_apply))
        current_crop = list(camera.crop)

        for idx,coord in enumerate(current_crop):
            current_crop[idx] = CameraControl.clamp((current_crop[idx] + crop_to_apply[idx]),0.0,1.0)

        current_crop[2] = current_crop[3] #make sure ratio is correct
        current_crop[0] = CameraControl.clamp(current_crop[0], 0.0, (1.0 - current_crop[2]))
        current_crop[1] = CameraControl.clamp(current_crop[1], 0.0, (1.0 - current_crop[3]))

        logging.info("Crop after all corrections: "+str(current_crop))

        for idx,coord in enumerate(current_crop):
            if(not CameraControl.isclose(current_crop[idx], camera.crop[idx])):
                success = True

        camera.crop = current_crop
        return success, camera.crop

    # Set zoom factor
    @staticmethod
    def setZoom(factor):
        success = False
        factor = float(factor)
        logging.info("Applying zoom: "+str(factor))
        current_crop = list(camera.crop)
        current_factor = 1.0/current_crop[3]
        target_factor = current_factor + factor
        dimdiff = 1 / target_factor - current_crop[3]

        # apply
        current_crop[0] = CameraControl.clamp(camera.crop[0]-(dimdiff/2),0.0,1.0)
        current_crop[1] = CameraControl.clamp(camera.crop[1]-(dimdiff/2),0.0,1.0)
        current_crop[2] = CameraControl.clamp(1/target_factor,0.0,1.0)
        current_crop[3] = CameraControl.clamp(1/target_factor,0.0,1.0)                

        # sanity checks
        current_crop[2] = current_crop[3] #make sure ratio is correct
        current_crop[0] = CameraControl.clamp(current_crop[0], 0.0, (1.0 - current_crop[2]))
        current_crop[1] = CameraControl.clamp(current_crop[1], 0.0, (1.0 - current_crop[3]))

        logging.info("Crop after all corrections: "+str(current_crop))

        for idx,coord in enumerate(current_crop):
            if(not CameraControl.isclose(current_crop[idx], camera.crop[idx])):
                success = True

        camera.crop = current_crop

        return success, camera.crop

    # Trigger reboot
    @staticmethod
    def doReboot():
        logging.info("REBOOT")
        if (platform.uname().system !="Windows"):
            os.system('sudo reboot')
        else:
            logging.warning("NO REAL REBOOT - WINDOWS MOCKUP MODE")

    # Trigger shutdown
    @staticmethod
    def doShutdown():
        logging.info("SHUTDOWN")
        if (platform.uname().system !="Windows"):
            os.system('sudo shutdown -h now')
        else:
            logging.warning("NO REAL SHUTDOWN - WINDOWS MOCKUP MODE")


# Helper class for streaming camera data to http
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


# Class for handling incoming http requests (routing to app logic)
class StreamingHandler(server.BaseHTTPRequestHandler):    

    def do_GET(self):                
        # Respond to mjpg GET requests
        # Answer request
        if self.path[:12] == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            try:
                while True:                
                    with CameraControl.lock:
                        camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
                        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
                    # image?
                    frame = memoryview(file_data)

                    s_file_jpgdata = BytesIO(frame)
                    s_im = Image.open(s_file_jpgdata)
                    s_out = s_im.transpose(Image.ROTATE_270)
                    buffer = BytesIO()
                    s_out.save(buffer,format="JPEG")                 
                    s_outdata = buffer.getvalue()
                    
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(s_outdata))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(s_outdata)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        # Respond to still jpg GET requests
        elif self.path[:10] == "/still.jpg":
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            try:                
                with CameraControl.lock:
                    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
                    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
                    print('Copying image to', '/tmp/still.jpg')
                    camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
                    camera_file.save('/tmp/still.jpg')
                f = open('/tmp/still.jpg', "rb")
                frame = f.read()
                f.close()
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', len(frame))
                self.end_headers()
                self.wfile.write(frame)
                self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))        

        elif self.path[:2] == '/?':
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # Prepare response object
            resp_obj = {'action': 'null', 'crop':camera.crop, 'result':'true'}
            
            # Parse incoming params
            params = dict(urllib.parse.parse_qsl(self.path.split("?")[1], True))
            for key,value in params.items():
                logging.info(key + " = " + value)

            # Param actions (route to app logic)
            if("action" in params):
                if(params.get("action") == "abspos"):
                    resp_obj["action"] = "abspos"
                    resp_obj["result"] = "true"
                    resp_obj["crop"] = CameraControl.setAbsolutePosition(params.get("crop"))

                elif(params.get("action") == "relpos"):
                    
                    hasSuccess, newCrop = CameraControl.setRelativePosition(params.get("crop"))

                    # result obj
                    resp_obj["action"] = "relpos"
                    resp_obj["result"] = hasSuccess
                    resp_obj["crop"] = newCrop

                elif(params.get("action") == "zoom"):                    
                    
                    hasSuccess, newCrop = CameraControl.setZoom(params.get("factor"))

                    # result obj
                    resp_obj["action"] = "zoom"
                    resp_obj["result"] = hasSuccess
                    resp_obj["crop"] = newCrop

                elif(params.get("action") == "reboot"):
                    
                    CameraControl.doReboot()

                    #result obj
                    resp_obj["action"] = "reboot"
                    resp_obj["result"] = "true"
                    del resp_obj["crop"]

                elif(params.get("action") == "shutdown"):
                    
                    CameraControl.doShutdown()

                    #result obj
                    resp_obj["action"] = "shutdown"
                    resp_obj["result"] = "true"
                    del resp_obj["crop"]

                elif(params.get("action") == "update"):

                    logging.info("UPDATE - not implemented")
                    
                    #result obj
                    resp_obj["action"] = "update"
                    resp_obj["result"] = "false"
                    del resp_obj["crop"]
                    
            self.wfile.write(bytes(json.dumps(resp_obj), 'utf8'))    
        else:
            logging.info("Path requested: " +self.path)
            self.send_error(404)
            self.end_headers()


# Class for handling incoming socket.io requests (routing to app logic)
class SimoreCamNamespace(socketio.ClientNamespace):

    def on_connect(self, env=None, sid="clientMode"):
        self.emit("REGISTER_CLIENT", "camslr")
        logging.info("CONNECT")
        print("SIO CONNECT")

    def on_disconnect(self, env=None, sid="clientMode"):
        logging.info("DISCONNECT")

    def on_capture(self, data):
        logging.warn("SIO: Capture event")
        with CameraControl.lock:
            file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
            print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
            print('Copying image to', '/tmp/still.jpg')
            self.emit("captured","null");
            camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
            camera_file.save('/tmp/still.jpg')
            f = open('/tmp/still.jpg', "rb")
            frame = f.read()
            f.close()
            print('Reading to file data')
            file_jpgdata = BytesIO(frame)
            im = Image.open(file_jpgdata)
            print('Transposing')
            out = im.transpose(Image.ROTATE_270)
            size = 600,900
            out.thumbnail(size)
            print('Coding and sending')
            buffer = BytesIO()
            out.save(buffer,format="JPEG")                 
            outdata = buffer.getvalue()
            frame_str = binascii.b2a_base64(outdata).decode('utf-8')
            print('Emit')
            self.emit("picture",frame_str);

    def on_abspos_event(self, data):
        logging.info("SIO: AbsPos event")

        resp_obj = {'action': 'null', 'crop':camera.crop, 'result':'true'}
        resp_obj["action"] = "abspos"
        resp_obj["result"] = "true"
        resp_obj["crop"] = CameraControl.setAbsolutePosition(data)
        self.emit("camera_response", json.dumps(resp_obj))

    def on_relpos_event(self, data):
        logging.info(data)
        logging.info("SIO: Relpos event")

        resp_obj = {'action': 'null', 'crop':camera.crop, 'result':'true'}
        
        hasSuccess, newCrop = CameraControl.setRelativePosition(data)

        # result obj
        resp_obj["action"] = "relpos"
        resp_obj["result"] = hasSuccess
        resp_obj["crop"] = newCrop
        self.emit("camera_response", json.dumps(resp_obj))

    def on_zoom_event(self, data):
        logging.info("SIO: Zoom event")

        resp_obj = {'action': 'null', 'crop':camera.crop, 'result':'true'}

        hasSuccess, newCrop = CameraControl.setZoom(data)

        # result obj
        resp_obj["action"] = "zoom"
        resp_obj["result"] = hasSuccess
        resp_obj["crop"] = newCrop

        self.emit("camera_response", json.dumps(resp_obj))

    def on_reboot_event(self, data):
        logging.info("SIO: Reboot event")

        #result obj
        resp_obj = {'action': 'reboot', 'crop': 'false', 'result': 'false'}

        self.emit("camera_response", json.dumps(resp_obj))

        CameraControl.doReboot()

    def on_shutdown_event(self, data):
        logging.info("SIO: Shutdown event")

        #result obj
        resp_obj = {'action': 'shutdown', 'crop': 'false', 'result': 'false'}

        self.emit("camera_response", json.dumps(resp_obj))

        CameraControl.doShutdown()


    def on_update_event(self, data):
        logging.info("SIO: Update event")

        logging.error("UPDATE - not implemented")
                    
        #result obj
        resp_obj["action"] = "update"
        resp_obj["result"] = "false"
        del resp_obj["crop"]

        self.emit("camera_response", json.dumps(resp_obj))

    def on_echo_event(self, data):
        self.emit('resp', data)
        logging.info("SIO: Echo event")


# Helper class for HTTP server setup in thread
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Helper class for socket.io server setup in thread
class SocketIOCamServer():

    def __init__(self):
        self.sio = socketio.Server()    
        self.app = socketio.WSGIApp(self.sio, static_files={
            '/': {'content_type': 'text/html', 'filename': 'index.html'}
        })
        self.sio.register_namespace(SimoreCamNamespace())

    def serve_app(self):
        logging.info("Serve forever / SIO")
        eventlet.wsgi.server(eventlet.listen(('', 7000)), self.app)


class SocketIOCamClient():

    def __init__(self):
        self.sio = socketio.Client()    
        self.sio.register_namespace(SimoreCamNamespace())

    def connect(self):
        while self.sio.sid == None:
            try:
                self.sio.connect('http://'+SOCKETIO_SERVER_ADDRESS+':'+str(SOCKETIO_SERVER_PORT))
                print("Try connect...")
            except:
                print("Fail connect, wait 2 sec")
                time.sleep(2)

    def destroy(self):
        self.sio.disconnect()


#
########################
# Main Startup Logic ###
########################
logging.basicConfig(filename=None, level=logging.WARN,
        format='%(asctime)s: %(levelname)5s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# HTTP Server startup
address = ('', 8097)
server = StreamingServer(address, StreamingHandler)
t1 = threading.Thread(target=server.serve_forever)
t1.daemon = True
t1.start()

# Socketio Server / Client Startup
if(SOCKETIO_ROLE == "server"):
    sioserver = SocketIOCamServer()
    t2 = threading.Thread(target=sioserver.serve_app)
    t2.daemon = True
    t2.start()    
else:
    sioclient = SocketIOCamClient()
    t2 = threading.Thread(target=sioclient.connect)
    t2.daemon = True
    t2.start()   


# SLR Setup
# GPhoto init / testing
context = gp.gp_context_new()
error, camera = gp.gp_camera_new()
error = gp.gp_camera_init(camera, context)
error, text = gp.gp_camera_get_summary(camera, context)
#print('Summary')
#print('=======')
#print(text.text)

# required configuration will depend on camera type!
print('Checking camera config')
config = gp.check_result(gp.gp_camera_get_config(camera))
OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
if OK >= gp.GP_OK:
    value = gp.check_result(gp.gp_widget_get_value(image_format))
    if 'raw' in value.lower():
        print('Cannot preview raw images')
# find the capture size class config item
OK, capture_size_class = gp.gp_widget_get_child_by_name(
    config, 'capturesizeclass')
if OK >= gp.GP_OK:
    value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
    gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
    gp.check_result(gp.gp_camera_set_config(camera, config))


# Fire up final (hackyhacky)
try:
    output = StreamingOutput()
    logging.info("Serve forever")
    while True:
        logging.info("--- Server is alive")
        time.sleep(30)

except:
    sys.exc_info()[0]
    raise

finally:
    logging.info("Fail / Exit")
    sioclient.destroy()

