import cv2
import numpy as np
import json
import os


def get_length(side):
    x = side[0][0] - side[1][0]
    y = side[0][1] - side[1][1]
    return x*x + y*y


def get_hash(image):
    dots = get_dots(image)
    checking_array = list()
    array = list()

    for i, dot_first in enumerate(dots):
        for j, dot_second in enumerate(dots):
            for k, dot_third in enumerate(dots):
                dot = (dot_first, dot_second, dot_third)
                sorted_dot = sorted(dot)
                if dot_first != dot_second and dot_first != dot_third and dot_second != dot_third and sorted_dot not in checking_array:
                    checking_array.append(sorted_dot)
                    array.append(dot)
    del checking_array

    triangle_arr = list()
    for i in array:
        sides = [get_length((i[0], i[1])), get_length((i[1], i[2])), get_length((i[0], i[2]))]
        triangle_arr.append(sorted(sides, reverse=True))

    return triangle_arr


def get_dots(img):
    if type(img) == str:
        img = cv2.imread(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    trash = np.sort(dst.ravel())[::-1][10]

    # Threshold for an optimal value, it may vary depending on the image.
    operation = dst > trash

    must_append = 10 - len(dst[operation])

    img[operation] = [0, 0, 255]

    for i, row in enumerate(dst):
        for j, line in enumerate(row):
            if must_append == 0:
                break
            elif line == trash:
                img[i, j] = [0, 0, 255]
                must_append -= 1

    dots = list()
    c = 0
    for y, i in enumerate(img):
        for x, j in enumerate(i):
            if j.tolist() == [0, 0, 255]:
                dots.append((x, y))
                c += 1

    return dots


def write_hashes(path):
    a = list(os.walk(path))[0][2]

    Hashes = dict()
    for c, i in enumerate(a):
        print(f'{c + 1}/{len(a)}')
        if i.endswith('.jpg'):
            H = get_hash(os.path.join(path, i))
            Hashes.update({i: H})
    json.dump(Hashes, open(os.path.join(path, 'config.json'), 'w+'))


def compare_hashes(hash1, hash2):
    c = 0
    c1 = 0
    while True:
        if c1 > len(hash1) - 1:
            break
        co1 = hash1[c1]
        c2 = 0
        while True:
            if c2 > len(hash2) - 1:
                c1 += 1
                break
            co2 = hash2[c2]
            if co1[0] / co2[0] == co1[1] / co2[1] == co1[2] / co2[2]:
                c += 1
                del hash1[c1]
                del hash2[c2]
                break
            else:
                c2 += 1
    return c


def compare_images(dir_name):
    json_config1 = json.load(open(os.path.join(dir_name, 'config.json')))
    json_config2 = json_config1.copy()
    start_length = len(json_config2)

    images = dict()
    for name1, hash1 in json_config1.items():
        images.update({name1: list()})
        for name2, hash2 in json_config2.items():
            if name1 != name2:
                comparing = compare_hashes(hash1[:], hash2[:])
                images[name1].append({name2: comparing})
                if comparing > 30:
                    print(name1, name2, comparing)
        del json_config2[name1]
        print(f'{len(json_config2) + 1}/{start_length}')
        json.dump(images, open(os.path.join(dir_name, 'results.json'), 'w+'))


def show_results(dir_name):
    results = json.load(open(os.path.join(dir_name, 'results.json'), 'r+'))

    for name, r in results.items():
        new_results = sorted(r, key=lambda x: next(iter(x.values())), reverse=True)
        if len(new_results) > 0:
            if next(iter(new_results[0].values())) > 10:
                print(name)
            else:
                continue
        else:
            continue
        for i in new_results:
            key, value = i.popitem()
            if value > 10:
                print(key, value, end=', ')
        print('\n')


def do_with_results(dir_name):
    results = json.load(open(os.path.join(dir_name, 'results.json'), 'r+'))
    for name, r in results.items():
        for i in r:
            key, value = i.popitem()
            if value > 43:
                print(value, name, key, 'is a copy')
            elif value > 34:
                print(value, name, key, 'maybe a copy')
            elif value > 24:
                print(value, name, key, 'maybe not a copy')


if __name__ == '__main__':
    compare_images('01')
    do_with_results('01')
