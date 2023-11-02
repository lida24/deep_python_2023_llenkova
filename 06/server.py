import json
import socket
import threading
import argparse
import requests
from bs4 import BeautifulSoup
from collections import Counter


class URLProcess:
    def __init__(self, url, k_words):
        self.url = url
        self.k_words = k_words

    def process(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        words = soup.get_text().split()
        words = Counter(words).most_common(self.k_words)
        most_common_words = {}
        for key, value in words:
            most_common_words[key] = value
        return most_common_words, self.url


class Worker(threading.Thread):
    def __init__(self, server, thread_id, client_socket, k_words, lock):
        super().__init__()
        self.server = server
        self.thread_id = thread_id
        self.client_socket = client_socket
        self.k_words = k_words
        self.lock = lock

    def run(self):
        while True:
            if not self.lock.locked():
                self.lock.acquire()
            data = self.client_socket.recv(4096)
            url = data.decode().strip()
            if self.lock.locked():
                self.lock.release()
            url_process = URLProcess(url, self.k_words)
            most_common_words, processed_url = url_process.process()
            self.client_socket.send(json.dumps(f'{processed_url}: {most_common_words}', ensure_ascii=False).encode())
            self.server.print_statistics(self.lock)


class Server:
    def __init__(self, workers_count, k_words):
        self.host = socket.gethostname()
        self.port = 8080
        self.workers_count = workers_count
        self.k_words = k_words
        self.lock = threading.Lock()
        self.sock = socket.socket()
        self.processed_urls_counter = 0

    def start(self):
        threads = []
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.workers_count)
        for i in range(self.workers_count):
            client_socket, _ = self.sock.accept()
            thread = Worker(self, i + 1, client_socket, self.k_words, self.lock)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def print_statistics(self, lock):
        if not lock.locked():
            lock.acquire()
        self.processed_urls_counter += 1
        lock.release()
        print(f'Обработано {self.processed_urls_counter} урлов')


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', type=int)
    parser.add_argument('-k', type=int)
    return parser


if __name__ == '__main__':
    input_parser = create_parser()
    args = input_parser.parse_args()
    workers = args.w
    top_k = args.k
    server = Server(workers, top_k)
    server.start()
