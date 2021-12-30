import asyncio
import base64
from itertools import cycle

import aioreactive as rx
import httpx

from core.settings import settings

DEFAULT_BASE_URL = "https://api.github.com"
URL_PATH = "/search/code"
REQUEST_DELAY = 10


class GithubClient:
    observable: rx.AsyncObservable

    def __init__(self):
        self.token_iter = cycle(settings.GITHUB_TOKENS)
        self.recent_sha = set()
        self.recent_sha_deq = []

    def get_token(self):
        return next(self.token_iter)

    def get_headers(self):
        return {"Authorization": f'token {self.get_token()}',
                "Accept": "application/vnd.github.v3.text-match+json",
                'User-Agent': 'PyGithub/Python'}

    async def get_items_meta(self, per_page: int = 100):
        search_q = '+'.join(settings.SEARCH_KEYWORDS)
        params_str = f"?sort=indexed&order=desc&q={search_q}&per_page={per_page}&page={1}"

        print('sleep delay start')
        await asyncio.sleep(REQUEST_DELAY)
        print('sleep delay end')

        headers = self.get_headers()
        print(headers['Authorization'])
        async_client = httpx.AsyncClient()
        async with async_client:
            r = await async_client.get(DEFAULT_BASE_URL + URL_PATH + params_str, headers=headers)
        if r.status_code == 403:
            raise ConnectionError('Rate limit reached')
        try:
            print(f"get_items_meta {len(r.json()['items'])=}")
            for item in r.json()['items']:
                yield item
        except Exception as e:
            print(e)
            print(r.json())
            raise

    async def get_recent_items_meta(self):
        async for item in self.get_items_meta():
            if item['sha'] not in self.recent_sha:
                self.recent_sha_deq.append(item['sha'])
                self.recent_sha.add(item['sha'])
                yield item
            while len(self.recent_sha_deq) > 500:
                item_sha = self.recent_sha_deq.pop()
                self.recent_sha.remove(item_sha)

    async def load_item(self, item):
        client = httpx.AsyncClient()
        async with client:
            req = await client.get(item['url'], headers=self.get_headers())
            return req.json()

    async def iter_items(self):
        while True:
            async for item in self.get_recent_items_meta():
                loaded_item = await self.load_item(item)
                content = base64.b64decode(loaded_item['content']).decode('utf-8')
                loaded_item['content'] = content
                yield loaded_item


client = GithubClient()
observable = rx.from_async_iterable(client.iter_items())
subject = rx.AsyncSubject()
