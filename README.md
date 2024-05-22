# Kaiju

Async AI model executor for async server

## Installation

Install using `pip`\
From source:

```bash
pip3 install git+https://github.com/ninja-96/kaiju
```

## Getting Started

1) Write your own class for pass data throught `Pipeline`

```python
from kaiju.item import BaseItem

class ImageItem(BaseItem):
    image: torch.Tensor = torch.tensor([])
    predict: torch.Tensor = torch.tensor([])
```

2) Write your own class for handler

```python
from kaiju.handler import BaseHandler

class ModelHandler(BaseHandler):
    def __init__(self, device: str) -> None:
        super().__init__()
        self._model = torchvision.models.resnet18(weights='DEFAULT').eval().to(device)
        self._device = device

    def forward(self, data: ImageItem) -> ImageItem:
        data.predict = self._model(data.image.to(self._device)).cpu()
        return data
```

3) Create `Pipeline` instance

```python
from kaiju.runner import Runner

pipeline = Pipeline(
    [
        Runner(ModelHandler('cpu'))
    ]
)
```

### Note

- You can set number of worker for every `Runner`

```python
Runner(ModelHandler('cpu')).n_workers(4)
```

- If your model uses Nvidia GPU, you can device your `Runner` as critical section of `Pipeline`. It will be useful for preventing GPU memory overload. [See](https://pytorch.org/docs/stable/notes/multiprocessing.html#cuda-in-multiprocessing)

```python
Runner(ModelHandler('cuda')).n_workers(2).critical_section()
```

## Built with

- [pydantic](https://github.com/pydantic/pydantic) - Data validation using Python type hints

## Versioning

All versions available, see the [tags on this repository](https://github.com/ninja-96/kaiju/tags).

## Authors

- **Oleg Kachalov** - _Initial work_ - [ninja-96](https://github.com/ninja-96)

See also the list of [contributors](https://github.com/ninja-96/kaiju/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 license - see the [LICENSE.md](./LICENSE) file for details.
