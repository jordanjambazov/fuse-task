import os
import zmq
import uuid
import random
import argparse
import json

PORT = 5556

FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')
MIN_FILE_SIZE = 5
MAX_FILE_SIZE = 4096


class FileWriter:
    """
    Writes a random number of bytes (within some configurable
    range) to a file with a file name it generated. It then sends a
    message to verifier stating that it has written the file, the
    filename and its size.
    """

    def __init__(self, files_dir, min_file_size, max_file_size):
        """
        Stores the files directory and the file size range.
        Initializes the communication socket.
        """
        self.files_dir = files_dir
        self.min_file_size = min_file_size
        self.max_file_size = max_file_size

        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:{}".format(PORT))

    @staticmethod
    def generate_file_name():
        """
        Generates random file name using UUID4.
        """
        file_name = str(uuid.uuid4())
        return file_name

    def generate_file(self):
        """
        Writes random number of bytes to a file with
        random name.
        """
        file_name = self.generate_file_name()
        file_size = random.randrange(self.min_file_size,
                                     self.max_file_size + 1)
        file_path = os.path.join(self.files_dir, file_name)
        with open(file_path, 'wb') as output_file:
            output_file.write(os.urandom(file_size))
        return json.dumps((file_name, file_size))

    def run(self):
        """
        The main loop for files generation.
        """
        while True:
            file_info = self.generate_file()
            self.socket.send(file_info)
            verifier_message = self.socket.recv()
            if verifier_message == 'next':
                continue
            else:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Write random files and notify verifier.')
    parser.add_argument('--min-file-size', type=int, default=MIN_FILE_SIZE)
    parser.add_argument('--max-file-size', type=int, default=MAX_FILE_SIZE)
    parser.add_argument('--files-dir', default=FILES_DIR)
    args = parser.parse_args()
    writer = FileWriter(args.files_dir, args.min_file_size, args.max_file_size)
    writer.run()
