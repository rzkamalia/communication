import socket

HOST = '192.168.254.160'
PORT = 9099

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket.connect((HOST, PORT))

socket.send("Hellow".encode('utf-8'))

# if the connection is accepting, client will recieve below message
message = socket.recv(1024).decode('utf-8')
print(f'Message from server is: {message}.')