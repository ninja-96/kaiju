import torch
import torchvision
from pydantic import Field

from kaiju.item import BaseItem
from kaiju.handler import BaseHandler
from kaiju.runner import Runner
from kaiju.pipeline import Pipeline


class ImageItem(BaseItem):
    """DTO item for `Pipeline`.

    Fields:
        image (torch.Tensor): NCHW image (float32).
        predict (torch.Tensor): model prediction.
    """
    image: torch.Tensor = Field(default_factory=torch.Tensor)
    predict: torch.Tensor = Field(default_factory=torch.Tensor)


class Reader(BaseHandler):
    """Dummy reader.

    Write your code to read data from source. `torch.rand` is for example.
    """
    def forward(self, data: ImageItem) -> ImageItem:
        """Getting new `ImageItem` instance and fill it with new data.

        Args:
            data (ImageItem): new `ImageItem` instance.

        Returns:
            ImageItem: filled `ImageItem` instance.
        """
        data.image = torch.rand(16, 3, 224, 224)
        return data


class R18Model(BaseHandler):
    """Model inference.

    Write your code to process data.
    """
    def __init__(self, device) -> None:
        super().__init__()
        with torch.inference_mode():
            self._model = torchvision.models.resnet18(weights='DEFAULT').eval().to(device)

        self._device = device

    def forward(self, data: ImageItem) -> ImageItem:
        """Resnet 18 inference.

        Getting data from `data.image` and pass it through model.

        Args:
            data (ImageItem): `ImageItem` instance.

        Returns:
            ImageItem: `ImageItem` instance with predicts.
        """
        with torch.inference_mode():
            data.predict = self._model(data.image.to(self._device)).cpu()
            return data


if __name__ == '__main__':
    pipeline = Pipeline(
        Runner(Reader()).n_workers(2),
        Runner(R18Model('cuda')).n_workers(4).critical_section()
    )

    pipeline.start(ImageItem(), batch_size=32)
