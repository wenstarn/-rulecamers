from onvif import ONVIFCamera
import time 

class ptzcam():
    def __init__(self, ip, port, login, password):
        try:
            self.mycam = ONVIFCamera(ip, int(port), login, password)
        except:
            self.mycam = None
            raise
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
        self.ptz.ContinuousMove(self.request)
        time.sleep(timeout)
        self.stop()
        
    def move_tilt(self, velocity, timeout):
        self.request.Velocity.PanTilt.x = 0.0
        self.request.Velocity.PanTilt.y = velocity
        self.request.Velocity.Zoom.x = 0.0
        self.request.Velocity.PanTilt.space = ''
        self.request.Velocity.Zoom.space = ''
        self.accomplish_move(timeout)
        
    def move_pan(self, velocity, timeout):
        self.request.Velocity.PanTilt.x = velocity
        self.request.Velocity.PanTilt.y = 0.0
        self.request.Velocity.Zoom.x = 0.0
        self.request.Velocity.PanTilt.space = ''
        self.request.Velocity.Zoom.space = ''
        self.accomplish_move(timeout)
        
    def zoom(self, velocity, timeout):
        self.request.Velocity.PanTilt.x = 0.0
        self.request.Velocity.PanTilt.y = 0.0
        self.request.Velocity.Zoom.x = velocity
        self.request.Velocity.PanTilt.space = ''
        self.request.Velocity.Zoom.space = ''
        self.accomplish_move(timeout)
