import socket
import sys
import pickle
from camera import ptzcam
import datetime

time_format = "%Y-%m-%d %H:%M:%S"

def add_in_log(string):
    log_file = open('log.txt', 'a', encoding='utf-8')
    log_file.write(string)
    log_file.close()

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False
        
def get_time():
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    return f"{now:{time_format}}"
def run_server(port):
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind(("127.0.0.1", port))
    serv_sock.listen(5)
    while True:
        client_sock, client_address = serv_sock.accept()
        string = get_time() + ' Connected ' + str(client_address) + '\n'
        print(string)
        add_in_log(string)
        while True:
            client_sock.sendall('Enter IP, ONVIF port, username and password'.encode())
            if serve_client(client_sock, client_address , port):
                break
            else:
                client_sock.sendall('Invalid command'.encode())
           
def serve_client(client_sock, client_address, port):
    try:
            data = client_sock.recv(2048)
            if not data:
                data = None
    except:
            data = None
    if data == None:
        string = get_time() + f" User {client_address} unexpectedly disconnected\n"
        print (string)
        add_in_log(string)
        client_sock.close()
        return True
    else:
        camera = handle_data(data, client_address)
        if not camera.mycam:
            return False
        else: 
            client_sock.sendall('Successful connection'.encode())
            string = get_time() + f" User {client_address} successfully connected to camera ({camera.ip}, {camera.port})\n"
            print(string)
            add_in_log(string)
            while True:
                client_sock.sendall('Enter command or exit to disconnect'.encode())
                try:
                    chunk = client_sock.recv(2048)
                    if not chunk:
                        chunk = None
                except:
                    chunk = None
                if chunk == None:
                    string = get_time() + f" User {client_address} unexpectedly disconnected from camera ({camera.ip}, {camera.port})\n"
                    print (string)
                    add_in_log(string)
                    client_sock.close()
                    return True
                else:
                    if handle_commands(chunk, camera, client_sock):
                        break    
    client_sock.close()
    string = get_time() + f" User {client_address} finished work camera with ({camera.ip}, {camera.port})\n"
    print (string)
    add_in_log(string)
    return True

def handle_data(data, client_address):
    obj = pickle.loads(data)
    camera = ptzcam(obj[0], obj[1], obj[2], obj[3], client_address)
    return camera

def handle_commands(chunk, camera, client_sock):
    chunk = chunk.decode()
    chunk  = chunk.split()
    if len(chunk) == 1 and chunk[0] == "exit":
        client_sock.sendall("exit".encode())
        return True
    elif  len(chunk) == 3 and is_digit(chunk[1]) and is_digit(chunk[2]):
                        
        if  chunk[0] == "tilt":
            camera.move_tilt(float(chunk[1]), float(chunk[2]))
                            
        elif  chunk[0] == "pan":
            camera.move_pan(float(chunk[1]), float(chunk[2]))
                            
        elif chunk[0] == "zoom":
            camera.zoom(float(chunk[1]), float(chunk[2]))
                            
        else:
            client_sock.sendall('Invalid command'.encode())
    else:
        client_sock.sendall('Invalid command'.encode())
        
    return False
    
if __name__ == '__main__':
    run_server(port=int(sys.argv[1]))
