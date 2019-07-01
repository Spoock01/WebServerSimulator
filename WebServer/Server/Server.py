import socket
import time
import threading
from socket import AF_INET, SOCK_STREAM

from Server.Handler import ConnectionHandler
from Utils.Utils import LOG_FILE

try:
    from Utils.Utils import PORT
    from Utils.Utils import HOST
except ModuleNotFoundError:
    from Utils import PORT, HOST

def run_server():
    server = socket.socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen(5)

    # Creating log file
    with open((LOG_FILE), 'a+') as f:
        f.write('Server started at: ' + str(time.strftime('{%d-%m-%Y %H:%M:%S}')) + '\n')

    while True:
        print('Waiting for connection...\n\n')
        lock = threading.Lock()
        (client_socket, address) = server.accept()
        client = ConnectionHandler(client_socket, address)
        threading.Thread(target=client.run, args=(lock, )).start()
