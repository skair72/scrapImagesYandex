# A tool for scrapping images from yandex

I wrote a really useful script for scrapping only original images from yandex

## Getting Started

You need a python >=3.6

Just clon my repo and run main.py with flags, where:

* Number of images: -c
* Folder to save: -f
* Search request: -s

If yandex need captcha, a window with captcha image is poping up. Write a text to console and hit enter

## Example:
```
python3 main.py -c 100 -f cats -s 'cat'
```
