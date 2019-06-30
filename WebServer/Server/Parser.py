from Utils.Utils import USER_REQUEST
from Utils.Utils import ROUTES
import json
import os
from os import path
from pathlib import Path
from Response import Response

ROOT_DIR = os.path.dirname(os.path.abspath(''))

class Parser:

    def __init__(self, client_message, client_socket):
        self.client_socket = client_socket
        self.client_message = client_message
        self.header = list()
        self.request_content = list()

    def run(self):

        string = self.client_message.split('\n')
        is_header = True

        for line in string:

            if line == '\r':
                is_header = False
            else:
                if is_header:
                    self.header.append(line)
                else:
                    self.request_content.append(line)

        self._response()

    def _response(self):

        response = Response()
        request = self.header[0].split(' ')
        #
        # print('-------------------')
        # t = ''.join(self.request_content)
        # y = json.loads(t)
        # print(type(y))
        # print('-------------------')

        if request[USER_REQUEST] == 'GET':

            response.append_header('content-type: text/HTML\n'.encode())

            file_path = Path(ROOT_DIR + '/Folders' + request[1])
            # file_path = ROOT_DIR + '/Folders/' + request[1].replace('/', '')
            print('File in: {} => {}'.format(file_path, request[1]))

            if path.exists(file_path):
                response.set_status_code('HTTP/1.0 200 OK\n'.encode())
                response.append_body(open_file(file_path))
            else:
                response.set_status_code('HTTP/1.0 404 Not Found\n'.encode())
                response.append_body(open_file(ROOT_DIR + '/Folders/notfound404.htm'))

            self.client_socket.send(response.get_response())

        elif request[0] == 'POST':
            response.append_header('content-type: text/HTML\n'.encode())
            if request[1] in ROUTES:
                response.set_status_code('HTTP/1.0 200 OK\n'.encode())
            else:
                response.set_status_code('HTTP/1.0 404 Not Found\n'.encode())
                response.append_body(open_file(ROOT_DIR + '/Folders/notfound404.htm'))

            self.client_socket.send(response.get_response())
        else:
            print('Não é get nem post')


def open_file(path):
    data = b''

    with open(Path(path), 'r', encoding='utf-8', errors='ignore') as rf:
        for line in rf:
            data += line.encode()

    return data
