# from Utils.Utils import ROUTES
import json
import os
from os import path
from pathlib import Path
from Server.Response import Response
from Server.Logger import Logger

try:
    from Utils.Utils import STATUS_200, STATUS_204, STATUS_401, STATUS_403, STATUS_404, STATUS_501
    from Utils.Utils import PROTECTED_ROUTES, AUTHORIZATION_TOKENS
    from Utils.Utils import USER_REQUEST, ROUTES
except ModuleNotFoundError:
    from Utils import STATUS_200, STATUS_204, STATUS_401, STATUS_403, STATUS_404, STATUS_501
    from Utils import PROTECTED_ROUTES, AUTHORIZATION_TOKENS 
    from Utils import USER_REQUEST, ROUTES   

ROOT_DIR = os.path.dirname(os.path.abspath('WebServer'))


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
            if request[1] in PROTECTED_ROUTES:
                if self.unauthorized_request(request):
                    self.get_request(request)
            else:
                self.get_request(request)

        elif request[USER_REQUEST] == 'POST':
            if request[1] in PROTECTED_ROUTES:
                if self.unauthorized_request(request):
                    self.post_request(request)
            else:
                self.post_request(request)
        else:
            self.not_implemented_request(request)

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
        self.logger.set_request_type(self.header[0])
        self.client_socket.send(response.get_response())

    #The POST request receives the data as JSON
    def post_request(self, request):
        response = Response()

        response.append_header('content-type: text/HTML\n'.encode())
        if request[1] in ROUTES:
            jsonData = ''.join(self.request_content).replace('\t', '')
            data = json.loads(jsonData)
            response.set_status_code((STATUS_204 + '\n').encode())
        else:
            response.set_status_code((STATUS_404 + '\n').encode())
            response.append_body(self._open_file(ROOT_DIR + '/Folders/notfound404.htm'))

        self.logger.set_status_response(response.get_status())
        self.logger.set_request_type(self.header[0])
        self.client_socket.send(response.get_response())

    def not_implemented_request(self, request):
        response = Response()

        response.append_header('content-type: text/HTML\n'.encode())
        response.set_status_code((STATUS_501 + '\n').encode())
        response.append_body(self._open_file(ROOT_DIR + '/Folders/notimplemented.htm'))

        self.logger.set_status_response(response.get_status())
        self.logger.set_request_type(self.header[0])
        self.client_socket.send(response.get_response())

    def unauthorized_request(self, request):
        response = Response()

        response.append_header('content-type: text/HTML\n'.encode())
        auth_token = self.get_authorization_token(self.header)
        if auth_token:
            if auth_token in AUTHORIZATION_TOKENS:
                return True
            else:
                print('-'*20)
                print(auth_token)
                print('-' * 20)
                self.forbidden_request(request)
                return False

        response.append_header('WWW-Authenticate: Basic realm= "System Administrator"\n'.encode())
        response.set_status_code((STATUS_401 + '\n').encode())

        self.logger.set_status_response(response.get_status())
        self.logger.set_request_type(self.header[0])
        self.client_socket.send(response.get_response())
        return False

    def forbidden_request(self, request):
        response = Response()

        response.append_header('content-type: text/HTML\n'.encode())
        response.append_body(self._open_file(ROOT_DIR + '/Folders/unauthorized.htm'))
        response.set_status_code((STATUS_403 + '\n').encode())

        self.logger.set_status_response(response.get_status())
        self.logger.set_request_type(self.header[0])
        self.client_socket.send(response.get_response())

    def get_authorization_token(self, header):
        auth = ''

        for h in header:
            if 'Authorization:' in h:
                auth = h
                break

        if not auth:
            return auth

        return auth.replace('\r', '').split(' ')[2]

    def _open_file(self, _path):
        data = b''

        with open(Path(_path), 'r', encoding='utf-8', errors='ignore') as rf:
            for line in rf:
                data += line.encode()

        return data
