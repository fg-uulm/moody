import platform

#Mockup PiCamera for testing on non-Pi systems
if platform.uname().system =="Windows":
    
    print("========== RUNNING IN MOCKUP CAMERA MODE!!! =============")

    class PiCamera(object):
        rotation = 0
        crop = [0,0,1,1]


        # default constructor 
        def __init__(self, resolution, framerate, sensor_mode):
            print("PCMock: PiCamera constructed")

        def __enter__(self):
            print("PCMock: PiCamera enter")
            return self

        def __exit__(self, resolution, framerate, sensor_mode):
            print("PCMock: PiCamera exit")
            return self

        def PiCamera(self, resolution, framerate, sensor_mode):
            print("PCMock: PiCamera created")

        def start_recording(self, output, format):
            print("PCMock: Start recording")

        def stop_recording():
            print("PCMock: Stop recording")
