import asyncio
import json

import aiohttp


async def stream_reader():
    async with aiohttp.request('get', 'http://127.0.0.1:8001/api/v1/github/exposed_keys', json={'words': []}) as r:
    # async with aiohttp.request('get', 'http://127.0.0.1:8001/api/v1/github/exposed_keys', json={'words': ['password', 'token']}) as r:
    # async with aiohttp.request('get', 'http://127.0.0.1:8001/api/v1/github/raw') as r:
        async for line in r.content:
            yield json.loads(line)


async def main():
    async for item in stream_reader():
        print(item)


asyncio.get_event_loop().run_until_complete(main())
