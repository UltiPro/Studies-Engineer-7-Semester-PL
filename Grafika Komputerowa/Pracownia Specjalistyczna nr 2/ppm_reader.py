from dataclasses import dataclass
from collections import deque
from itertools import zip_longest


@dataclass
class RGB():
    r: int
    g: int
    b: int

    def to_hex(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)


class Image():
    def __init__(self, width: int, height: int, max_val: int, pixel_data, type='tuples', mode='RGB'):
        self.width = width
        self.height = height
        self.max_val = max_val
        self.pixel_data = pixel_data
        self.type = type
        self.mode = mode


def rgb_to_hex(rgb_tuple: tuple[int, int, int]):
    return '#%02x%02x%02x' % rgb_tuple


def grouper(n, iterable, fillvallue=None):
    return zip_longest(*[iter(iterable)]*n, fillvalue=fillvallue)


def read_p3(filepath: str):
    pixel_data: list
    tmp_data = deque()
    file_contents: str
    with open(filepath, 'r', encoding='ISO-8859-1') as f:
        file_contents = f.read()

    sections = file_contents.split('#')
    for i, x in enumerate(sections):
        if i == 0:
            if len(x.strip()) < 3:
                tmp_data.append(x)
            else:
                tmp_data.extend(x.split())
            continue

        if idx := x.find('\n'):
            x = x[idx:]

        tmp_data.extend(x.split())

    type = tmp_data.popleft().strip()
    width = int(tmp_data.popleft())
    height = int(tmp_data.popleft())
    max_val = int(tmp_data.popleft())

    if len(tmp_data) % 3 != 0:
        print('Not all rgb values have 3 ints')
        return None

    if len(tmp_data)/3 != width * height:
        print('Amount of rgb values not equivalent to img dimensions')
        return None

    pixel_data: list
    if max_val == 255:
        pixel_data = list(grouper(3, [int(v) for v in tmp_data], fillvallue=0))
    else:
        pixel_data = list(
            grouper(3, [round(int(v)/max_val*255) for v in tmp_data], fillvallue=0))

    print("len of pixel_data: ", len(pixel_data))
    return Image(width, height, max_val, pixel_data)


def read_p6(filepath: str):
    params = []
    pointer = None
    binary = None
    with open(filepath, 'r', encoding='ISO-8859-1') as f:
        while True:
            line = f.readline()
            idx = line.find('#')
            if idx != -1:
                line = line[:idx]
            params.extend(line.split())

            if len(params) == 4:
                pointer = f.tell()
                break

    if pointer:
        with open(filepath, 'rb') as f:
            f.seek(pointer)
            binary = f.read()

    if binary:
        return Image(int(params[1]), int(params[2]), int(params[3]), binary, type='bin')

    print('no binary data in p6 file retrieved')
    return None


def read_file(filepath: str):
    if filepath[-4:] != '.ppm':
        print("Trying to use ppm reader on a non .ppm filetype")
        return None

    with open(filepath, 'r', encoding='ISO-8859-1') as f:
        first = f.readline().split()[0]
        if first == 'P3':
            return read_p3(filepath)
        elif first == 'P6':
            return read_p6(filepath)
        else:
            print('error in file')
            return None
