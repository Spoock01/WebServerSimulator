from Utils.Utils import USER_REQUEST
from Utils.Utils import ROUTES
import json
import os
from os import path
from pathlib import Path
from Response import Response
from Logger import Logger
from Utils.Utils import STATUS_200
from Utils.Utils import STATUS_204
from Utils.Utils import STATUS_404

ROOT_DIR = os.path.dirname(os.path.abspath(''))


class Parser:

    def __init__(self, client_message, client_socket, user_address, lock):
        self.client_socket = client_socket
        self.client_message = client_message
        self.user_address = user_address
        self.header = list()
        self.request_content = list()
        self.logger = Logger(lock)

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
        self.logger.write_log()

    def _response(self):

        self.logger.set_user_address(user_address=self.user_address[0])
        request = self.header[0].split(' ')

        if request[USER_REQUEST] == 'GET':
            self.get_request(request)

        elif request[USER_REQUEST] == 'POST':
            self.post_request(request)
        else:
            print('Não é get nem post')

    def get_request(self, request):

        response = Response()
        response.append_header('content-type: text/HTML\n'.encode())

        file_path = Path(ROOT_DIR + '/Folders' + request[1])

        print('File in: {} => {}'.format(file_path, request[1]))

        if path.exists(file_path):
            response.set_status_code((STATUS_200 + '\n').encode())
            response.append_body(self._open_file(file_path))
        else:
            response.set_status_code((STATUS_404 + '\n').encode())
            response.append_body(self._open_file(ROOT_DIR + '/Folders/notfound404.htm'))

        self.logger.set_status_response(response.get_status())
        self.logger.set_request_type(request[USER_REQUEST])
        self.client_socket.send(response.get_response())

    def post_request(self, request):
        response = Response()

        response.append_header('content-type: text/HTML\n'.encode())
        if request[1] in ROUTES:
            response.set_status_code((STATUS_204 + '\n').encode())
        else:
            response.set_status_code((STATUS_404 + '\n').encode())
            response.append_body(self._open_file(ROOT_DIR + '/Folders/notfound404.htm'))

        self.logger.set_status_response(response.get_status())
        self.logger.set_request_type(request[USER_REQUEST])
        self.client_socket.send(response.get_response())

    def _open_file(self, _path):
        data = b''

        with open(Path(_path), 'r', encoding='utf-8', errors='ignore') as rf:
            for line in rf:
                data += line.encode()

        return data
