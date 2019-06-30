from Parser import Parser
import socket


class ConnectionHandler:

    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address
        self.client_message = ''
        self.connection = True
        print('Connection start...')

    def run(self, lock):
        self.client_socket.settimeout(5)
        self._recvall()

        if self.connection:
            print('Request: ', self.client_message)
            Parser(client_message=self.client_message, client_socket=self.client_socket,
                   lock=lock, user_address=self.address).run()
            self._close_connection()

        print('\n\n')

    def _close_connection(self, timeoutexcep=False):     # End of connection

        if not timeoutexcep:
            print(self.client_message)
        else:
            print('Timeout exception! Closing connection.')

        self.connection = False
        self.client_socket.close()

    def _recvall(self):     # Reading user's message

        print('Waiting for message...')
        buff_size = 4096  # 4 KiB
        data = b''
        while True:
            try:
                part = self.client_socket.recv(buff_size)
                data += part
                if len(part) < buff_size:  # either 0 or end of data
                    print('Message received!')
                    break
            except socket.timeout:
                self._close_connection(timeoutexcep=True)
                break

        self.client_message = data.decode()

