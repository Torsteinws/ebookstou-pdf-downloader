# About
Project for downloading ebook images from [readonline.ebookstou.org](http://readonline.ebookstou.org) and convert them to a single pdf file.

# Prerequisites

1. Download and install [python](https://www.python.org/downloads/windows/)

# Download source code

Download the source code by either:
- [Option A] Navigating the GitHub website.
- [Option B] Download and install [git](https://git-scm.com/download/win). Then clone the project via the command line.

    ```shell
    git clone https://github.com/Torsteinws/ebookstou-pdf-downloader.git
    ```

# Setup

Install dependencies:
```shell
pip install -r requirements.txt
```

# Run project

```shell
python main.py
```

or...

```shell
python main.py <base_url>
```

base_url should be the url to the directory where the source images are located.
For example:

```shell
python main.py http://readonline.ebookstou.org/flipbook/40908/files/mobile
```

# Edit project
Start editing the project by downloading and installing an IDE (Integrated Development Environment).
I Recommend using either:
- [Visual Studio Code](https://code.visualstudio.com/Download) — Fast and fantastic, but has a steeper learning curve.
- [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows) — Easier to learn, but runs slowly.