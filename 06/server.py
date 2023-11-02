import socket
import argparse
import threading
import requests
from bs4 import BeautifulSoup
from collections import Counter


class Worker(threading.Thread):
    def __init__(self, server, worker_id, top_k_words):
        super().__init__()
        self.server = server
        self.worker_id = worker_id
        self.top_k_words = top_k_words

    def run(self):
        while True:
            url = self.server.get_url_to_process()
            if url:
                process = URLProcess(url, self.top_k_words)
                top_words = process.process_url()
                response = {url: top_words}
                self.server.send_response(response)


class Server:
    def __init__(self, workers, top_k_words):
        self.host = socket.gethostname()
        self.port = 8000
        self.workers = workers
        self.top_k_words = top_k_words
        self.worker_threads = []
        self.urls_queue = []
        self.lock = threading.Lock()
        self.responses = {}

    def start(self):
        sock = socket.socket()
        sock.bind((socket.gethostname(), 8000))
        sock.listen(5)
        for i in range(self.workers):
            worker = Worker(self, i, self.top_k_words)
            worker_thread = threading.Thread(target=worker.run)
            self.worker_threads.append(worker_thread)
            worker_thread.start()
        while True:
            client_conn, client_addr = sock.accept()
            data = client_conn.recv(4096)
            self.urls_queue.append(data)

    def get_url_to_process(self):
        if self.urls_queue:
            with self.lock:
                url = self.urls_queue.pop(0)
            return url
        return None

    def send_response(self, response):
        self.responses.update(response)


class URLProcess:
    def __init__(self, url, top_k_words):
        self.url = url
        self.top_k_words = top_k_words

    def process_url(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                words = text.split()
                word_counter = Counter(words)
                top_words = dict(word_counter.most_common(self.top_k_words))
                return top_words
        except Exception as e:
            print(f'Error while processing {self.url}: {str(e)}')
        return {}


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('number_of_workers', type=int)
    parser.add_argument('qt_of_words', type=int)
    return parser


if __name__ == '__main__':
    input_parser = create_parser()
    # print(parse_arg)
    args = input_parser.parse_args()
    number_of_workers = args.number_of_workers
    qt_of_words = args.qt_of_words
    server = Server(number_of_workers, qt_of_words)
    server.start()
