# import the necessary packages
from threading import Thread
import gphoto2 as gp

class SLRVideoStream:
    def __init__(self, resolution=(320, 240), framerate=32, **kwargs):
        print("Init camera")
        # SLR Setup
        self.shotRequested = False
        # GPhoto init / testing
        self.context = gp.gp_context_new()
        self.error, self.camera = gp.gp_camera_new()
        self.error = gp.gp_camera_init(self.camera, self.context)
        self.error, self.text = gp.gp_camera_get_summary(self.camera, self.context)

        # required configuration will depend on camera type!
        print('Checking camera config')
        self.config = gp.check_result(gp.gp_camera_get_config(self.camera))
        OK, image_format = gp.gp_widget_get_child_by_name(self.config, 'imageformat')
        if OK >= gp.GP_OK:
            value = gp.check_result(gp.gp_widget_get_value(image_format))
            if 'raw' in value.lower():
                print('Cannot preview raw images')
        # find the capture size class config item
        OK, capture_size_class = gp.gp_widget_get_child_by_name(
            self.config, 'capturesizeclass')
        if OK >= gp.GP_OK:
            value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
            gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
            gp.check_result(gp.gp_camera_set_config(self.camera, config))

        self.frame = None
        self.shot = None
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            camera_file = gp.check_result(gp.gp_camera_capture_preview(self.camera))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
            self.frame = memoryview(file_data)

            # if the capture indicator is set, grab full size pic
            if(self.shotRequested):
                file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
                print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
                print('Copying image to', '/tmp/still.jpg')
                camera_file = self.camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
                camera_file.save('/tmp/still.jpg')
                #self.shot = memoryview(camera_file)
                self.shotRequested = False

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.camera.exit()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def readShot(self):
        # return last shot
        return self.shot

    def requestShot(self):
        self.shotRequested = True
        while(self.shotRequested):
            pass

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True