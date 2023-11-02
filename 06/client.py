import socket
import argparse
import threading


class Client:
    def __init__(self, file, number_of_threads):
        self.server_host = socket.gethostname()
        self.server_port = 8000
        self.urls = self.load_urls(file)
        self.number_of_threads = number_of_threads
        self.threads = []

    @staticmethod
    def load_urls(file_name):
        with open(file_name, 'r') as file:
            urls = file.read().splitlines()
        return urls

    def run(self):
        for _ in range(self.number_of_threads):
            thread = threading.Thread(target=self.send_request)
            self.threads.append(thread)
            thread.start()

        for thread in self.threads:
            thread.join()

    def send_request(self):
        client_socket = socket.socket()
        client_socket.connect((self.server_host, self.server_port))
        while self.urls:
            url = self.urls.pop(0)
            client_socket.send(url.encode())
            data = client_socket.recv(4096).decode()
            print(data)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('threads', type=int)
    parser.add_argument('urls_file')
    return parser


if __name__ == '__main__':
    input_parser = create_parser()
    # print(parse_arg)
    args = input_parser.parse_args()
    urls_file = args.urls_file
    threads = args.threads
    client = Client(urls_file, threads)
    client.run()
