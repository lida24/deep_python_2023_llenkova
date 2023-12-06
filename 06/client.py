import socket
import argparse
from queue import Queue
import threading


class Client:
    def __init__(self, file, number_of_threads):
        self.host = socket.gethostname()
        self.port = 8080
        self.file = file
        self.number_of_threads = number_of_threads

    def get_urls(self):
        try:
            with open(self.file, "r") as file:
                for line in file:
                    yield line.strip()
        except FileNotFoundError:
            print(f"File {self.file} not found")

    def get_client_socket(self):
        sock = socket.socket()
        try:
            sock.connect((self.host, self.port))
            return sock
        except Exception as e:
            print(f"Error occurred on client side while connecting to the server: {e}")

    def send_requests(self, url_queue, result_queue):
        while True:
            url = url_queue.get()
            if url is None:
                url_queue.put(url)
                break
            with self.get_client_socket() as sock:
                try:
                    sock.send(url.encode())
                    data = sock.recv(4096).decode()
                    if data:
                        result_queue.put((url, data))
                        print(f"{url}: {data}")
                except Exception as e:
                    print(f"Error occurred on client side while processing url {url}: {e}")

    def run(self):
        urls = list(self.get_urls())
        url_queue = Queue()
        result_queue = Queue()
        client_threads = [
            threading.Thread(target=self.send_requests, args=(url_queue, result_queue))
            for _ in range(self.number_of_threads)
        ]
        for thread in client_threads:
            thread.start()

        for url in urls:
            url_queue.put(url)
        url_queue.put(None)

        for thread in client_threads:
            thread.join()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("threads", type=int)
    parser.add_argument("urls_file")
    return parser


if __name__ == "__main__":
    input_parser = create_parser()
    args = input_parser.parse_args()
    urls_file = args.urls_file
    threads = args.threads
    client = Client(urls_file, threads)
    client.run()
