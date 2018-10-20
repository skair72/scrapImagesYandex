# A tool for scrapping images from yandex

I wrote a really useful script for scraping only original images from yandex

## Getting Started

You need a python >=3.6

Just clone my repo and run main.py with flags, where:

* Number of images: -c
* Folder to save: -f
* Search request: -s

If yandex need captcha, a window with captcha image is poping up. Write a text to console and hit enter.

If new scrapped image is a copy of old one, harris algorithm provide that, and write a log to console.

## How to use:
```
python3 main.py -c 100 -f cats -s 'cat'
```
