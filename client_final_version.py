import socket
import pickle
class client():
    def __init__(self, ip, port):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection = False
        self.camera_connection = False
        self.client_sock.connect((ip, int(port)))
        if (self.client_sock.recv(2048)).decode() == "You are connected to server":
            self.server_connection = True
    def connect_to_camera(self, ip, port, login, password):
        if self.server_connection:
            data = [ip, port, login, password]
            data = pickle.dumps(data)
            self.client_sock.sendall(data)
            if self.client_sock.recv(2048).decode() ==  'You are connected to camera':
                self.camera_connection = True         
        else:
            print('You are not connected to server')
    def command_to_camera(self, command, velocity , timeout):
        if self.camera_connection:
                data = command + ' ' + str(velocity) + ' ' + str(timeout)
                self.client_sock.sendall(data.encode())
                answer = self.client_sock.recv(2048).decode()
                if answer != 'Success':
                    print(answer)
        else:
            print("You are not connected to camera")
    def disconnect_from_camera(self):
        if self.camera_connection: 
            command = "exit"
            self.client_sock.sendall(command.encode())
            self.client_sock.recv(2048).decode()
            self.camera_connection = False
        else:
            print("You are not connected to camera")
    def disconnect_from_server(self):
        if self.server_connection:
            if not self.camera_connection:
                data = bytearray()
                self.client_sock.sendall(data)
                self.client_sock.close()
                self.server_connection = False
            else:
                print("Initially you have to disconnect from camera")
        else:
            print('You are not connected to camera')
