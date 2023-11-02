import socket
import argparse
from queue import Queue
import threading


class Client:
    def __init__(self, file, number_of_threads):
        self.host = socket.gethostname()
        self.port = 8080
        self.urls = self.get_urls(file)
        self.number_of_threads = number_of_threads

    @staticmethod
    def get_urls(file):
        queue_of_urls = Queue()
        with open(file, 'r') as file:
            for line in file:
                queue_of_urls.put(line.strip())
        return queue_of_urls

    def send_requests(self):
        sock = socket.socket()
        sock.connect((self.host, self.port))
        while True:
            url = self.urls.get()
            sock.send(url.encode())
            data = sock.recv(4096).decode()
            print(data)

    def run(self):
        client_threads = [threading.Thread(target=self.send_requests) for _ in range(self.number_of_threads)]
        for thread in client_threads:
            thread.start()

        for thread in client_threads:
            thread.join()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('threads', type=int)
    parser.add_argument('urls_file')
    return parser


if __name__ == '__main__':
    input_parser = create_parser()
    args = input_parser.parse_args()
    urls_file = args.urls_file
    threads = args.threads
    client = Client(urls_file, threads)
    client.run()
