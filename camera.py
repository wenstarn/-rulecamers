from onvif import ONVIFCamera
import onvif
import time 
import datetime

def add_in_log(string):
    log_file = open('log.txt', 'a', encoding='utf-8')
    log_file.write(string)
    log_file.close()
    
def get_time():
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    return f"{now:{time_format}}"

time_format = "%Y-%m-%d %H:%M:%S"

class ptzcam():
    def __init__(self, ip, port, login, password, client_address):
        self.ip = ip
        self.port = port
        self.client_address = client_address
        try:
            self.mycam = ONVIFCamera(ip, int(port), login, password)
        except onvif.exceptions.ONVIFError as inst:
            self.mycam = None
            x = inst.args
            string = get_time() + f' Client {client_address} cannot connect to camera ({self.ip}, {self.port}) ' + str(x)
            print(string)
            add_in_log(string)   
        else:
            self.media = self.mycam.create_media_service()
            self.media_profile = self.media.GetProfiles()[0]
            self.ptz = self.mycam.create_ptz_service()

            self.request = self.ptz.create_type('ContinuousMove')
            self.request.ProfileToken = self.media_profile.token
            self.request.Velocity = self.ptz.GetStatus({'ProfileToken': self.media_profile.token}).Position
                        
            self.request_ = self.ptz.create_type('Stop')
            self.request_.ProfileToken = self.media_profile.token
        
    def stop(self):
        self.request_.PanTilt = True
        self.request_.Zoom = True
        self.ptz.Stop(self.request_)

    def accomplish_move(self, timeout):
        try:
            self.ptz.ContinuousMove(self.request)
            time.sleep(timeout)
            self.stop()
        except onvif.exceptions.ONVIFError as inst:
            x = inst.args
            return x
        else:
            return 1
            
    def move_tilt(self, velocity, timeout):
        self.request.Velocity.PanTilt.x = 0.0
        self.request.Velocity.PanTilt.y = velocity
        self.request.Velocity.Zoom.x = 0.0
        self.request.Velocity.PanTilt.space = ''
        self.request.Velocity.Zoom.space = ''
        answer = self.accomplish_move(timeout) 
        if answer == 1:
            string = get_time() + f" Command move_tilt {velocity} {timeout} of User {self.client_address} for camera ({self.ip}, {self.port}) was successfully executed\n"
            print(string)
            add_in_log(string)
        else:
            string = get_time() + f" Command move_tilt {velocity} {timeout} of User {self.client_address} for camera ({self.ip}, {self.port}) was not executed " + str(answer) + "\n"
            print(string)
            add_in_log(string)
            

    def move_pan(self, velocity, timeout):
        self.request.Velocity.PanTilt.x = velocity
        self.request.Velocity.PanTilt.y = 0.0
        self.request.Velocity.Zoom.x = 0.0
        self.request.Velocity.PanTilt.space = ''
        self.request.Velocity.Zoom.space = ''
        answer = self.accomplish_move(timeout) 
        if answer == 1:
            string = get_time() + f" Command move_pan {velocity} {timeout} of User {self.client_address} for camera ({self.ip}, {self.port}) was successfully executed\n"
            print(string)
            add_in_log(string)
        else:
            string = get_time() + f" Command move_pan {velocity} {timeout} of User {self.client_address} for camera ({self.ip}, {self.port}) was not executed " + str(answer) + "\n"
            print(string)
            add_in_log(string)
        
    def zoom(self, velocity, timeout):
        self.request.Velocity.PanTilt.x = 0.0
        self.request.Velocity.PanTilt.y = 0.0
        self.request.Velocity.Zoom.x = velocity
        self.request.Velocity.PanTilt.space = ''
        self.request.Velocity.Zoom.space = ''
        answer = self.accomplish_move(timeout) 
        if answer == 1:
            string = get_time() + f" Command zoom {velocity} {timeout} of User {self.client_address} for camera ({self.ip}, {self.port}) was successfully executed\n"
            print(string)
            add_in_log(string)
        else:
            string = get_time() + f" Command zoom {velocity} {timeout} of User {self.client_address} for camera ({self.ip}, {self.port}) was not executed " + str(answer) + "\n"
            print(string)
            add_in_log(string)
