import argparse
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def fetch_url(session, url):
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, "html.parser")
        paragraph = soup.find("p")
        first_sentence = paragraph.text.strip().split("\n")[0]
        return first_sentence


async def worker(session, queue):
    while True:
        url = await queue.get()
        try:
            task = await fetch_url(session, url)
            tasks.append(task)
        except Exception as e:
            print(f"Failed to fetch {url}, {str(e)}")
        finally:
            queue.task_done()


async def batch_fetch(queue, requests):
    async with aiohttp.ClientSession() as session:
        worker_tasks = [
            asyncio.create_task(worker(session, queue)) for _ in range(requests)
        ]
        await queue.join()
        for worker_task in worker_tasks:
            worker_task.cancel()


def get_urls(urls_file):
    with open(urls_file, "r") as file:
        for line in file:
            yield line


async def main(requests, urls_file):
    queue = asyncio.Queue()
    for url in get_urls(urls_file):
        await queue.put(url)
    await batch_fetch(queue, requests)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("number_of_requests", type=int)
    parser.add_argument("urls_file")
    return parser


if __name__ == "__main__":
    tasks = []
    input_parser = create_parser()
    args = input_parser.parse_args()
    number_of_requests = args.number_of_requests
    urls_file = args.urls_file
    asyncio.run(main(number_of_requests, urls_file))
