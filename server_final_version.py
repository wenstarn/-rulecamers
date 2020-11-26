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
        add_in_log(string)
        client_sock.sendall('You are connected to server'.encode())
        while True:
            if serve_client(client_sock, client_address):
                break

def serve_client(client_sock, client_address):
    while True:
        try:
                data = client_sock.recv(2048)
                if not data:
                    data = None
        except:
                data = None
        if data == None or len(data) == 0:
            string = get_time() + f" User {client_address} disconnected from server\n"
            add_in_log(string)
            client_sock.close()
            return True
        else:
            camera = handle_data(data, client_address)
            if not camera.mycam:
                client_sock.sendall('You are not connected to camera'.encode())
                return False
            else: 
                client_sock.sendall('You are connected to camera'.encode())
                string = get_time() + f" User {client_address} successfully connected to camera ({camera.ip}, {camera.port})\n"
                add_in_log(string)
                while True:
                    try:
                        chunk = client_sock.recv(2048)
                        print("ffff")
                        print(chunk)
                        if not chunk:
                            chunk = None
                    except:
                        chunk = None
                    if chunk == None:
                        print("ff")
                        string = get_time() + f" User {client_address} disconnected from camera ({camera.ip}, {camera.port})\n"
                        add_in_log(string)
                        client_sock.close()
                        return False
                    else:
                        if handle_commands(chunk, camera, client_sock):
                            break    
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
    print(chunk)
    if len(chunk) == 1 and chunk[0] == "exit":
        client_sock.sendall("exit".encode())
        return True
    elif  len(chunk) == 3 and is_digit(chunk[1]) and is_digit(chunk[2]):
                        
        if  chunk[0] == "tilt":
            if not camera.move_tilt(float(chunk[1]), float(chunk[2])):
                client_sock.sendall('The command was not executed'.encode())
            else:
                client_sock.sendall('Success'.encode())
                            
        elif  chunk[0] == "pan":
            if not camera.move_pan(float(chunk[1]), float(chunk[2])):
                client_sock.sendall('The command was not executed'.encode())
            else:
                client_sock.sendall('Success'.encode())
                            
        elif chunk[0] == "zoom":
            if not camera.zoom(float(chunk[1]), float(chunk[2])):
                client_sock.sendall('The command was not executed'.encode())
            else:
                client_sock.sendall('Success'.encode())
                            
        else:
            client_sock.sendall('Invalid command'.encode())
    else:
        client_sock.sendall('Invalid command'.encode())
        
    return False
    
if __name__ == '__main__':
    run_server(port=int(sys.argv[1]))
