import socket
import sys
import pickle
import camera

def run_server(port):
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind(("127.0.0.1", port))
    serv_sock.listen(5)
    while True:
        client_sock, client_address = serv_sock.accept()
        print ('Подключился', client_address)
        while True:
            client_sock.sendall('Введите IP камеры, ONVIF порт, логин и пароль'.encode())
            if serve_client(client_sock, client_address , port):
                break
            else:
                client_sock.sendall('Неудачное подключение'.encode())
            
def serve_client(client_sock, client_address, port):
    try:
            data = client_sock.recv(2048)
            if not data:
                data = None
    except:
            data = None
    if data == None:
        print ('Произошло внезапное отключение', client_address)
    else:
        obj = pickle.loads(data)
        camera = camera.ptzcam(obj[0], obj[1], obj[2], obj[3])
        if camera.mycam == None:
            return False
        else: 
            client_sock.sendall('Успешное подключение'.encode())
            while True:
                client_sock.sendall('Введите команду или exit, чтобы отключиться'.encode())
                try:
                    chunk = client_sock.recv(2048)
                    if not chunk:
                        chunk = None
                except:
                    chunk = None
                if chunk == None:
                    print ('Произошло внезапное отключение', client_address)
                    break
                else:
                    chunk = chunk.decode()
                    chunk  = chunk.split()
                    if len(chunk) == 1 and chunk[0] == "exit":
                        client_sock.sendall("exit".encode())
                        break
                    elif  len(chunk) == 3:
                        
                        if  chunk[0] == "tilt":
                            camera.move_tilt(chunk[1], chunk[2])
                            
                        elif  chunk[0] == "pan":
                            camera.move_pan(chunk[1], chunk[2])
                            
                        elif chunk[0] == "zoom":
                            camera.zoom(chunk[1], chunk[2])
                            
                        else:
                            client_sock.sendall('Неверная команда'.encode())
                    else:
                       client_sock.sendall('Неверная команда'.encode())
                       
    client_sock.close()
    print ('Отключился', client_address)
    return True
if __name__ == '__main__':
    run_server(port=int(sys.argv[1]))
