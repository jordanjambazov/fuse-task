import zmq
import time


PORT = 5556


class FileVerifier:
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind('tcp://*:{}'.format(PORT))

    def run(self):
        while True:
            writer_message = self.socket.recv()
            print "Received message is: {}".format(writer_message)
            self.socket.send("go")
            time.sleep(1)


if __name__ == '__main__':
    verifier = FileVerifier()
    verifier.run()
