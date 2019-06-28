import socket
import datetime
from socket import AF_INET, SOCK_STREAM
from handler import ConnectionHandler
from Utils.Utils import PORT
from Utils.Utils import HOST

server = socket.socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

# Creating log file
with open(('../Log/Log-' + str(PORT) + '.txt'), 'w+') as f:
    f.write('Server started at: ' + str(datetime.datetime.now()))

while True:
    print('\n\nWaiting for connection...\n\n')
    (client_socket, address) = server.accept()
    client = ConnectionHandler(client_socket, address)
    client.run()
