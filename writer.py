import os
import zmq
import uuid
import time
import random
import json

PORT = 5556
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')
MIN_FILE_SIZE = 5
MAX_FILE_SIZE = 4096



class FileWriter:
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:{}".format(PORT))

    def generate_file_name(self):
        file_name = str(uuid.uuid4())
        return file_name

    def generate_file(self):
        file_name = self.generate_file_name()
        file_size = random.randrange(MIN_FILE_SIZE,
                                     MAX_FILE_SIZE + 1)
        file_path = os.path.join(FILES_DIR, file_name)
        with open(file_path, 'wb') as output_file:
            output_file.write(os.urandom(file_size))
        return json.dumps((file_name, file_size))

    def run(self):
        while True:
            file_info = self.generate_file()
            self.socket.send(file_info)
            verifier_message = self.socket.recv()
            if verifier_message == 'go':
                time.sleep(1)
            else:
                break


if __name__ == '__main__':
    writer = FileWriter()
    writer.run()
