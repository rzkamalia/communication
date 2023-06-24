import socket

# host = socket.gethostbyname(socket.gethostname()) # automatic get your prate ip address

HOST = '192.168.177.160'
PORT = 9099

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP # this socket just for accepting connection, not for talk to client
server.bind((HOST, PORT))

server.listen(5) # if more than 5 connections, we reject the new connection one

while True: 
    communication_socket, address = server.accept() 
    # communication_socket = socket that use for communication to client
    # address = the address of upcoming connection
    # for each connection we get new communication socket
    print(f'Connected to {address}.')

    message = communication_socket.recv(1024).decode('utf-8')
    print(f'Message from client is: {message}.')

    communication_socket.send(f'Thank you'.encode('utf-8'))
    communication_socket.close()
    print(f'Connection with {address} ended.')
