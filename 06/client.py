import socket
import argparse


class Client:
    def __init__(self):
        pass

    def get_urls(self):
        pass


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('urls_file')
    return parser


if __name__ == '__main__':
    input_parser = create_parser()
    # print(parse_arg)
    args = input_parser.parse_args()
    urls_file = args.urls_file
    sock = socket.socket()
    sock.connect((socket.gethostname(), 8000))
    with open(urls_file, 'r') as file:
        for url in file:
            print(url)
            sock.send(url.encode())
            data = sock.recv(1024)
            print(data)
    sock.close()

