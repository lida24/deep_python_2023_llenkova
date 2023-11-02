import unittest
import server
import client
from unittest import mock


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    # @mock.patch('requests.get')
    # def test_server_processing_with_mocks(self, mock_get) -> None:
    #     server_obj = server.Server(workers_count=10, k_words=7)
    #     mock_response = mock.Mock()
    #     mock_response.text = 'This is response text'
    #     mock_get.return_value = mock_response
    #     server_obj.sock = mock.Mock()
    #     mock_socket = server_obj.sock.return_value
    #     mock_socket.recv.return_value = 'http://test.com'
    #     server_obj.start()
    #     mock_get.assert_called_with('http://test.com')
    #     mock_socket.send.assert_called_with('http://test.com')
    #     mock_socket.recv.assert_called_with(4096)

    @mock.patch('socket.socket')
    def test_server_processing(self, mock_socket) -> None:
        server_obj = server.Server(workers_count=10, k_words=7)
        server_obj.sock = mock.Mock()
        server_obj.sock.accept = mock.Mock(return_value=(mock_socket, ''))
        mock_socket.recv.return_value = b'http://test.com'

        server_obj.start()
        mock_socket.send.assert_called_with(b'http://test.com')
        mock_socket.recv.assert_called_with(4096)