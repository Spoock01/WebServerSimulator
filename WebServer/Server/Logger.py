import time
import sys


try:
    from Utils.Utils import LOG_FILE
except ModuleNotFoundError:
    print(sys.path)
    from Utils import LOG_FILE

class Logger:

    def __init__(self, lock):
        self.status_response = ''
        self.user_address = ''
        self.request_type = ''
        self.lock = lock

    def set_status_response(self, status):
        self.status_response = status

    def set_user_address(self, user_address):
        self.user_address = user_address

    def set_request_type(self, request_type):
        self.request_type = request_type

    def write_log(self):

        self.lock.acquire()
        with open(LOG_FILE, 'a+') as f:
            f.write('HOUR:{:<5} USER:{:<5} REQUEST:{:<5} STATUS:{:<5}'
                    .format(time.strftime('{%d-%m-%Y %H:%M:%S}'), self.user_address, self.request_type.strip(),
                            self.status_response))
        self.lock.release()


