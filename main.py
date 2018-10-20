import requests
from bs4 import BeautifulSoup
import os
import click
import harris
import urllib.request
import cv2
import numpy as np
import json
from skimage import io

@click.command()
@click.option('--count', '-c', default=12, help='number of images')
@click.option('--folder', '-f', default='downloaded', help='folder to save images')
@click.option('--search', '-s', default='test', help='search request')
def main(count, folder, search):
    S = SearchQuery(search, count, folder)
    S.search_pictures()


class SearchQuery:
    def __init__(self, search_text, num_of_pic, path):
        self.search_params = {
            'source': 'collections',
            'text': search_text
        }
        self.search_text = search_text
        self.num_of_pic = num_of_pic
        self.current_page = 0

        self.S = requests.session()
        self.S.headers = {
            'User-Agent': 'Opera/9.80 (Series 60; Opera Mini/7.1.32444/34.861; U; en) Presto/2.8.119 Version/11.10'
        }

        if os.path.exists(os.path.join(self.search_text, 'hashes.json')):
            self.pictures_hashes = json.load(open(os.path.join(self.search_text, 'hashes.json'), 'r+'))
            self.good_pic_found = int(list(self.pictures_hashes.keys())[-1][:-4])
        else:
            self.good_pic_found = 0
            self.pictures_hashes = dict()
        self.path = path

        make_path(search_text)
        make_path(os.path.join(search_text, path))
        make_path(os.path.join(search_text, 'pages'))

        self.last_request = None
        self.openedWindow = False

    def search_pictures(self):
        while self.num_of_pic > self.good_pic_found:
            if self.current_page != 0:
                self.search_params.update({'p': str(self.current_page)})

            r = self.S.get('https://m.yandex.ru/images/smart/search', params=self.search_params)

            self.last_request = r
            print(f'page {self.current_page + 1}')
            with open(os.path.join(self.search_text, 'pages', f'{self.current_page}.html'), 'w+') as f:
                f.write(r.text)
                f.close()
            self.download_thumbnails(r)
            self.current_page += 1

    def download_thumbnails(self, page):
        soup = BeautifulSoup(page.text, 'html.parser')
        hrefs = soup.findAll('img', {'class': 'serp-item__image'})

        while len(hrefs) == 0:
            r = self.captcha()
            soup = BeautifulSoup(r.text, 'html.parser')
            hrefs = soup.findAll('img', {'class': 'serp-item__image'})

        if self.openedWindow:
            self.openedWindow = False

        for img in hrefs:
            pic_url = 'https:' + str(img.get('src')[:-2] + '32')
            # print(pic_url)
            image = url_to_image(pic_url)

            image_hash, number, name_of_original = self.is_copy(image)
            if number != 0:
                print(f'{pic_url} is copy of {name_of_original}, {number}')
                continue

            self.good_pic_found += 1
            cv2.imwrite(os.path.join(self.search_text, self.path, f'{self.good_pic_found}.jpg'), image)
            self.pictures_hashes.update({f'{self.good_pic_found}.jpg': image_hash})
            json.dump(self.pictures_hashes, open(os.path.join(self.search_text, 'hashes.json'), 'w+'))
            print(f'{self.good_pic_found}/{self.num_of_pic}')

    def is_copy(self, image):
        target_hash = harris.get_hash(image)
        if len(self.pictures_hashes) == 0:
            return target_hash, 0, ''

        for name, h in self.pictures_hashes.items():
            n = harris.compare_hashes(h, target_hash)
            if n > 5:
                return target_hash, n, name
        return target_hash, 0, ''

    def captcha(self):
        soup = BeautifulSoup(self.last_request.text, 'html.parser')

        src = soup.find('img', {'class': 'image form__image'}).get('src')
        key = soup.find('input', {'class': 'form__key'}).get('value')
        repath = soup.find('input', {'class': 'form__retpath'}).get('value')

        image = io.imread(src)
        self.openedWindow = True
        cv2.imshow('Captcha', image)
        params = {
            'key': key,
            'retpath': repath,
            'rep': input('enter captcha: ')
        }
        cv2.destroyWindow('Captcha')
        cv2.waitKey(1)

        r = self.S.get('https://m.yandex.ru/checkcaptcha', params=params)
        self.last_request = r

        with open(os.path.join(self.search_text, 'pages', 'captcha.html'), 'w+') as f:
            f.write(r.text)
            f.close()

        return r


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'

    # return the image
    return img


def make_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


main()