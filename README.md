# A tool for scraping images from Yandex

I've written a really useful script for scraping only original images from Yandex

## Getting Started

You need a python >=3.6

Just clone my repo and run main.py with flags, where:

* Number of images: -c
* Folder to save: -f
* Search request: -s

If Yandex asks a captcha, a window with a captcha is popping up. Just write a text in the console and hit enter.

If a new scraped image is a copy of the old one, Harris algorithm handles that, and write a log to console.

## How to use:
```
python3 main.py -c 100 -f cats -s 'cat'
```
