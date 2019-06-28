class Response:

    def __init__(self):
        self.response_body = b''
        self.response_header = b''
        self.status = b''

    def set_status_code(self, status_code):
        self.status = status_code

    def append_header(self, another_header):
        self.response_header += another_header

    def append_body(self, body):
        self.response_body += body

    def get_response(self):
        return self.status + self.response_header + b'\n' + self.response_body
