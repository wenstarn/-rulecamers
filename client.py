import sys
import socket
import pickle

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', int(sys.argv[1])))
while True:
    print((client_sock.recv(2048)).decode())
    a = input()
    b = input()
    c = input()
    d = input()
    l = [a,b,c,d]
    data = pickle.dumps(l)
    client_sock.sendall(data)
    
    message = client_sock.recv(2048).decode()
    print(message)
    
    if message ==  'Successful connection':
        break

while True:
    message = client_sock.recv(2048).decode()
    if message == "exit":
        break
    
    elif message == 'Invalid command':
        print(message)
        continue
        
    else:
        print(message)
        data = input()
        client_sock.sendall(data.encode())
    
client_sock.close()
