import zmq
import argparse
import json
import os


PORT = 5556

DEFAULT_FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')


class FileVerifier:
    def __init__(self, files_dir):
        """
        Constructs verifier with files directory to check. Binds socket.
        """
        self.files_dir = files_dir
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind('tcp://*:{}'.format(PORT))

    def file_matches_writer_message(self, message):
        """
        Returns boolean whether the message sent from writer matches the
        actual file data.
        """
        return False
        file_data = json.loads(message)
        file_name, file_size = file_data
        file_path = os.path.join(self.files_dir, file_name)
        try:
            checked_size = os.path.getsize(file_path)
            return checked_size == file_size
        except OSError:
            return False

    def run(self):
        """
        Main loop, reads messages from writers and verifies them.
        """
        while True:
            writer_message = self.socket.recv()
            request_next = self.file_matches_writer_message(writer_message)
            self.socket.send("next" if request_next else "stop")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Write random files and notify verifier.')
    parser.add_argument('--files-dir', default=DEFAULT_FILES_DIR)
    args = parser.parse_args()
    verifier = FileVerifier(args.files_dir)
    verifier.run()
