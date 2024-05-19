"""
Setup script for ORT tools.
"""

from setuptools import find_packages, setup
import kaiju


setup(
    name='kaiju',
    version=kaiju.__version__,
    description='Async AI model executor for async server',
    author='Oleg Kachalov',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pydantic>=2.7'
    ]
)
