import sys
from onvif import ONVIFCamera
import os

class ptzcam():
    def __init__(self, ip, port, login, password):
        try:
            self.mycam = ONVIFCamera(ip, int(port), login, password)
        except:
            self.mycam = None
        else:
            self.media = self.mycam.create_media_service()
            self.media_profile = self.media.GetProfiles()[0]
            token = self.media_profile._token
            
            self.request = self.ptz.create_type('ContinuousMove')
            self.request.ProfileToken = self.media_profile._token
            
            self.request_ = self.ptz.create_type('Stop')
            self.request_.ProfileToken = self.media_profile._token
        
    def stop(self):
        self.request_.PanTilt = True
        self.request_.Zoom = True
        self.ptz.Stop(self.requests)
    
    def accomplish_move(self, timeout):
        self.ptz.ContinuousMove(self.request)
        sleep(timeout)
        self.stop()
        
    def move_tilt(self, velocity, timeout):
        self.request.Velocity.PanTilt._x = 0.0
        self.request.Velocity.PanTilt._y = velocity
        self.perform_move(timeout)
        
    def move_pan(self, velocity, timeout):
        self.request.Velocity.PanTilt._x = velocity
        self.request.Velocity.PanTilt._y = 0.0
        self.perform_move(timeout)
        
    def zoom(self, velocity, timeout):
        self.request.Velocity.Zoom._x = velocity
        self.perform_move(timeout)
