import json

from fastapi.encoders import jsonable_encoder
import aioreactive as rx


async def json_stream_from_aiter(aiter):
    async for item in aiter:
        yield json.dumps(jsonable_encoder(item), separators=(',', ':')).encode() + b'\n'


async def json_stream_from_observable(observable):
    async for item in rx.to_async_iterable(observable):
        print('json_stream_from_observable yield')
        yield json.dumps(jsonable_encoder(item), separators=(',', ':')).encode() + b'\n'



