import timeit
from itertools import zip_longest
from PIL import Image as im

FILE = "./ppm-obrazy-testowe/ppm-test-06-p6.ppm"


def grouper(n, iterable, fillvalue=None):
    return zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)


def read_p6(file):
    params = []
    pointer = None
    binary = None
    with open(FILE, "r", encoding="ISO-8859-1") as f:
        while True:
            line = f.readline()
            idx = line.find("#")
            if idx != -1:
                line = line[:idx]
            params.extend(line.split())

            if len(params) == 4:
                print("params", params)
                pointer = f.tell()
                print("pointer: ", pointer)
                break

    if pointer:
        with open(FILE, "rb") as f:
            f.seek(pointer)
            binary = f.read()

    if binary:
        img = im.frombuffer("RGB", (int(params[1]), int(params[2])), binary)
        img.show()


start_time = timeit.default_timer()
count = 0
l = ""
with open(FILE, "r", encoding="ISO-8859-1") as f:
    first_line = f.readline()
    if first_line.split()[0] == "P3":
        print("This is p3")
    elif first_line.split()[0] == "P6":
        read_p6(FILE)

print(timeit.default_timer() - start_time)
