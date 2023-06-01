import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="cheetahpy",
    version="0.4.0",
    author="Ryan Duecker",
    author_email='ryan.duecker@yahoo.com',
    description="Python wrapper for working with the Golden Cheetah API & opendata",
    extras_require={
        "test": [
            "pytest"]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["PyYAML", "pandas","requests",],
    url="https://github.com/RyanAugust/CheetahPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
)