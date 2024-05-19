import time
import asyncio

import torch
import torchvision

from kaiju.item import BaseItem
from kaiju.handler import BaseHandler
from kaiju.runner import Runner


class ImageItem(BaseItem):
    image: torch.Tensor = torch.tensor([])
    predict: torch.Tensor = torch.tensor([])


class ModelHandler(BaseHandler):
    def __init__(self) -> None:
        super().__init__()
        torch.set_num_threads(1)
        torch.set_num_interop_threads(1)
        self._model = torchvision.models.resnet18(weights='DEFAULT').eval()

    def forward(self, data: ImageItem) -> ImageItem:
        data.predict = self._model(data.image)
        return data


async def main(r: Runner, n: int) -> None:
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            r.pool,
            r,
            ImageItem(
                image=torch.rand(16, 3, 224, 224)
            )
        )
        for _ in range(n)
    ]

    await asyncio.gather(*futures)


if __name__ == '__main__':
    runner = Runner(ModelHandler()).n_workers(16)

    n = 16
    s = time.time()
    asyncio.run(main(runner, n))
    rt = time.time() - s
    print(f'Exec time: {round(rt, 5)}')
