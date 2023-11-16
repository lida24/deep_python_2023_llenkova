import unittest
from server import Server, URLProcess, create_parser
from client import Client
from unittest import mock
from queue import Queue


class TestServer(unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.MagicMock(w=5, k=10))
    def test_create_parser(self, mock_parse_args):
        parser = create_parser()
        args = parser.parse_args()
        self.assertEqual(args.w, 5)
        self.assertEqual(args.k, 10)

    def test_process_url(self):
        url_process = URLProcess("https://example.com", 5)
        most_common_words, processed_url = url_process.process()
        self.assertEqual(processed_url, "https://example.com")
        self.assertIsInstance(most_common_words, dict)

    def test_create_server(self):
        server = Server(5, 10)
        self.assertEqual(server.workers_count, 5)
        self.assertEqual(server.k_words, 10)


class TestClient(unittest.TestCase):
    def test_get_urls(self):
        client = Client("urls.txt", 5)
        urls = client.get_urls("urls.txt")

        self.assertIsInstance(urls, Queue)
        self.assertEqual(urls.qsize(), 100)

    @mock.patch('socket.socket')
    def test_send_requests(self, mock_socket):
        client = Client("urls.txt", 5)
        client.urls = mock.MagicMock()
        client.urls.get.side_effect = ["https://example.com", "https://google.com"]

        client.send_requests()
        mock_socket.return_value.connect.assert_called_with((client.host, client.port))
        mock_socket.return_value.send.assert_called_with("https://example.com".encode())
        mock_socket.return_value.recv.assert_called_with(4096)

