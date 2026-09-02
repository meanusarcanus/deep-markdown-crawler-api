from setuptools import setup, find_packages

setup(
    name="deep-markdown-crawler",
    version="1.0.0",
    description="Universal Website to Clean Markdown Crawler SDK (Firecrawl Alternative).",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    author="Meanus Arcanus",
    author_email="meanusarcanus@gmail.com",
    url="https://github.com/meanusarcanus/deep-markdown-crawler-api",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.12.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
