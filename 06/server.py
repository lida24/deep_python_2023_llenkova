import json
import socket
import sys
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
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                words = soup.get_text().split()
                words = Counter(words).most_common(self.k_words)
                most_common_words = {key: value for key, value in words}
                return most_common_words, self.url
            else:
                raise Exception(f"Received status code {response.status_code}")
        except Exception as e:
            print(f"Error occurred on server side while processing url {self.url}: {e}")


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
            if not url:
                continue
            url_process = URLProcess(url, self.k_words)
            try:
                result = url_process.process()
                if result:
                    most_common_words, processed_url = result
                    self.client_socket.send(
                        json.dumps(
                            f"{processed_url}: {most_common_words}", ensure_ascii=False
                        ).encode()
                    )
                    self.server.print_statistics(self.lock)
            except Exception as e:
                print(f"Error occurred on server side while running {url}: {e}")


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
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(self.workers_count)
            while True:
                client_socket, _ = self.sock.accept()
                thread = Worker(
                    self, len(threads) + 1, client_socket, self.k_words, self.lock
                )
                thread.start()
                threads.append(thread)
        except Exception as e:
            print(f"Error occurred while starting the server: {e}")

    def print_statistics(self, lock):
        if not lock.locked():
            lock.acquire()
        self.processed_urls_counter += 1
        lock.release()
        print(f"Processed {self.processed_urls_counter} urls")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", type=int)
    parser.add_argument("-k", type=int)
    return parser


if __name__ == "__main__":
    input_parser = create_parser()
    args = input_parser.parse_args()
    if not (args.w and args.k):
        print("Please provide values for both -w and -k arguments")
    workers = args.w
    top_k = args.k
    try:
        server = Server(workers, top_k)
        server.start()
    except Exception as e:
        print(f"Error occurred while creating the server: {e}")
