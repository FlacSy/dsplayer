from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.readlines()

setup(
    name="dsplayer",
    version="0.1.0",
    description="Music player for Discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FlacSy",
    author_email="flacsy.x@gmail.com",
    url="https://github.com/FlacSy/dsplayer",
    install_requires = install_requires,
    python_requires=">=3.6",
)