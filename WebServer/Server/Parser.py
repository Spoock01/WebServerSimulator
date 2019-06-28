class Parser:

    def __init__(self, client_message):
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

        for index, line in enumerate(self.header):
            print('Line:{:<10}Header Content:{}'.format(index, line))

        for index, line in enumerate(self.request_content):
            print('Line:{:<10}Request Content:{}'.format(index, line))
