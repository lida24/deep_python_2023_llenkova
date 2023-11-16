import unittest
from unittest import mock
import asyncio
import aiohttp
from aiohttp.test_utils import make_mocked_coro
from fetcher import fetch_url, worker


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.mock_queue = asyncio.Queue()
        self.mock_queue.get = make_mocked_coro(return_value="http://test.com")
        self.mock_session = mock.MagicMock()
        self.mock_tasks = []

    def tearDown(self) -> None:
        self.mock_queue = None
        self.mock_session = None
        self.mock_tasks = None

    @mock.patch("aiohttp.ClientSession.get")
    async def test_fetch_url(self, mock_get) -> None:
        mock_response = mock.MagicMock()
        mock_response.text = make_mocked_coro(return_value="<p>Test sentence</p>")
        mock_get.return_value.__aenter__.return_value = mock_response

        async with aiohttp.ClientSession() as session:
            result = await fetch_url(session, "http://test.com")
            self.assertEqual(result, "Test sentence")

    @mock.patch("fetcher.fetch_url")
    async def test_worker_no_url(self, mock_fetch) -> None:
        self.mock_queue.get = make_mocked_coro(return_value=None)
        await worker(self.mock_session, self.mock_queue, self.mock_tasks)
        mock_fetch.assert_not_called()
