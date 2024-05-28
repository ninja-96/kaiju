import pickle
import tempfile

import uvicorn

import aiofile
import torch
import torchvision

from fastapi import FastAPI

from kaiju.item import BaseItem
from kaiju.handler import BaseHandler, AsyncBaseHandler
from kaiju.pipeline import Pipeline
from kaiju.runner import Runner, AsyncRunner


class ImageItem(BaseItem):
    image: torch.Tensor = torch.tensor([])
    predict: torch.Tensor = torch.tensor([])


class ModelHandler(BaseHandler):
    def __init__(self, device) -> None:
        super().__init__()
        self._model = torchvision.models.resnet18(weights='DEFAULT').eval().to(device)
        self._device = device

    def forward(self, data: ImageItem) -> ImageItem:
        data.predict = self._model(data.image.to(self._device)).cpu()
        return data


class AsyncTensorSaverHandler(AsyncBaseHandler):
    def __init__(self) -> None:
        super().__init__()
        self._tmp_dir = tempfile.TemporaryDirectory()

    async def forward(self, data: ImageItem) -> ImageItem:
        async with aiofile.async_open(f'{self._tmp_dir.name}/kek.pt', 'wb') as file:
            await file.write(pickle.dumps(data.predict.cpu()))

        return data


if __name__ == '__main__':
    app = FastAPI()
    pipeline = Pipeline(
        [
            Runner(ModelHandler('cpu')).n_workers(4),
            Runner(ModelHandler('cuda')).n_workers(2).critical_section(),
            AsyncRunner(AsyncTensorSaverHandler())
        ]
    )

    @app.post('/pipeline')
    async def post_thread_pipeline():
        item = ImageItem(
            image=torch.rand(16, 3, 224, 224)
        )
        await pipeline(item)

    uvicorn.run(app)
