import aiohttp
import asyncio

import time


async def request(url: str, session: aiohttp.ClientSession) -> str:
    async with session.post(url) as response:
        await response.text()


async def main(url: str, r: int) -> None:
    async with aiohttp.ClientSession() as session:
        f = [
            asyncio.create_task(request(url, session))
            for i in range(r)
        ]

        await asyncio.gather(*f)


if __name__ == '__main__':
    repeats = 16

    s = time.time()
    asyncio.run(main('http://127.0.0.1:8000/pipeline', repeats))
    rt = time.time() - s
    print(rt)
