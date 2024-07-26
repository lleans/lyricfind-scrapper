import setuptools

requirements = [requirement.strip() for requirement in open(
    'requirements.txt', 'r', encoding='utf-8').readlines()]

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="LyricsFindScrapper",
    version='1.0.0',
    author="lleans",
    author_email="",
    description="LyricsFind scrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lleans/lyricfind-scrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], install_requires=requirements,
    python_requires='>=3.10',
)
