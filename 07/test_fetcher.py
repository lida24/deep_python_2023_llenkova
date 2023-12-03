import os
import unittest
from unittest import mock
import asyncio
from aiohttp.test_utils import make_mocked_coro
from fetcher import fetch_url, batch_fetch, get_urls


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.urls_file = "test_urls.txt"
        self.test_urls = [
            "http://example.com/1",
            "http://example.com/2",
            "http://example.com/3",
            "http://example.com/4",
            "http://example.com/5",
        ]
        with open(self.urls_file, "w") as file:
            for url in self.test_urls:
                file.write(f"{url}\n")

    def tearDown(self) -> None:
        os.remove(self.urls_file)

    @mock.patch("aiohttp.ClientSession.get")
    async def test_fetch_url(self, mock_session) -> None:
        mock_response = mock.MagicMock()
        mock_response.text = make_mocked_coro("<p>Test sentence</p>")
        mock_session.get.return_value.__aenter__.return_value = mock_response

        with mock.patch("aiohttp.ClientSession", return_value=mock_session):
            result = await fetch_url(mock_session, "http://example.com")
            self.assertEqual(result, "Test sentence")
            mock_session.get.called_once_with("http://example.com")

    @mock.patch("aiohttp.ClientSession.get")
    def test_batch_fetch(self, mock_session):
        mock_response = mock.MagicMock()
        mock_response.text = make_mocked_coro("<p>Test sentence</p>")

        async def mocked_session():
            return mock_response

        mock_session.side_effect = mocked_session
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        queue = asyncio.Queue()
        for url in self.test_urls:
            loop.run_until_complete(queue.put(url))
        loop.run_until_complete(batch_fetch(queue, 5))
        mock_session.assert_has_calls(
            [mock.call(url) for url in self.test_urls], any_order=True
        )

    def test_get_urls(self):
        urls = list(get_urls(self.urls_file))
        expected_urls = [url + "\n" for url in self.test_urls]
        self.assertEqual(urls, expected_urls)
