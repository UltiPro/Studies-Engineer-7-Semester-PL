from enum import IntEnum

from PIL.Image import Image

kernel_user = [0, 1, 0, 1, 1, 1, 0, 1, 0]


class PixelType(IntEnum):
    BG = 0
    FG = 1
    DC = 2


def get_pixels_in_mask(image: Image, pos: tuple, mask_dims=3) -> tuple:
    pixels: list = []
    mask_indices: list = []
    w, h = image.size

    positions: list = []
    offset = mask_dims // 2
    for y in range(-offset, offset + 1):
        for x in range(-offset, offset + 1):
            positions.append((x, y))

    for i, (dx, dy) in enumerate(positions):
        x = pos[0] + dx
        y = pos[1] + dy

        if x < 0 or x > w - 1:
            continue
        if y < 0 or y > h - 1:
            continue

        mask_indices.append(i)
        pixels.append(image.getpixel((x, y))[0])

    return pixels, mask_indices


def create_pixel_mapping(fg, bg):
    return {PixelType.FG: fg, PixelType.BG: bg}


def exact_match(kernel: list, image_pixels: list, indices, fg, bg) -> bool:
    mapping = create_pixel_mapping(fg, bg)
    for i in range(len(image_pixels)):
        kernel_pixel = kernel[indices[i]]
        if kernel_pixel == PixelType.DC:
            continue
        if image_pixels[i] != mapping[kernel_pixel]:
            return False

    return True


def partial_match(kernel: list, image_pixels: list, indices, fg, bg) -> bool:
    mapping = create_pixel_mapping(fg, bg)
    for i in range(len(image_pixels)):
        kernel_pixel = kernel[indices[i]]
        if kernel_pixel == PixelType.DC:
            continue
        if image_pixels[i] == mapping[kernel_pixel]:
            return True

    return False


def erosion(image: Image, fg=0, bg=255) -> Image:
    w, h = image.size
    kernel = [PixelType.FG for _ in range(9)]

    new_image = image.copy()
    for x in range(w):
        for y in range(h):
            image_pixels, indices = get_pixels_in_mask(image, (x, y))
            match = exact_match(kernel, image_pixels, indices, fg, bg)
            new_color = fg if match else bg
            new_image.putpixel((x, y), 3 * (new_color,))

    return new_image


def dilation(image: Image, fg=0, bg=255) -> Image:
    w, h = image.size
    kernel = [PixelType.FG for _ in range(9)]

    new_image = image.copy()
    for x in range(w):
        for y in range(h):
            image_pixels, indices = get_pixels_in_mask(image, (x, y))
            match = partial_match(kernel, image_pixels, indices, fg, bg)
            new_color = fg if match else bg
            new_image.putpixel((x, y), 3 * (new_color,))

    return new_image


def opening(image: Image) -> Image:
    image = erosion(image)
    return dilation(image)


def closing(image: Image) -> Image:
    image = dilation(image)
    return erosion(image)


def hitandmiss(image: Image, kernel=kernel_user, fg=0, bg=255) -> Image:
    w, h = image.size

    new_image = image.copy()
    for x in range(w):
        for y in range(h):
            image_pixels, indices = get_pixels_in_mask(image, (x, y))
            match = exact_match(kernel, image_pixels, indices, fg, bg)
            new_color = fg if match else bg
            new_image.putpixel((x, y), 3 * (new_color,))

    return new_image


def hitandmiss_thinthick(
    image: Image, kernel: list, thicken=False, fg=0, bg=255
) -> Image:
    w, h = image.size
    hit_color = fg if thicken else bg

    new_image = image.copy()
    for x in range(w):
        for y in range(h):
            image_pixels, indices = get_pixels_in_mask(image, (x, y))
            if len(image_pixels) != len(kernel):
                new_image.putpixel((x, y), image.getpixel((x, y)))
                continue
            match = exact_match(kernel, image_pixels, indices, fg, bg)
            new_color = hit_color if match else image.getpixel((x, y))[0]
            new_image.putpixel((x, y), 3 * (new_color,))

    return new_image


def rotate_kernel(kernel: list[int], count: int):
    new_kernel = kernel[:]
    for _ in range(count):
        new_kernel = rotate(new_kernel)
    return new_kernel


def rotate(kernel: list[int]):
    t_kernel = [-1 for _ in range(len(kernel))]
    for i in range(3):
        for j in range(3):
            t_kernel[3 * i + j] = kernel[3 * j + i]

    new_kernel = []
    for i in range(3):
        row = t_kernel[i * 3 : i * 3 + 3]
        new_kernel.extend(row[::-1])

    return new_kernel


def image_equals(image: Image, image2: Image) -> bool:
    if image.size != image2.size:
        return False

    w, h = image.size
    for x in range(w):
        for y in range(h):
            if image.getpixel((x, y)) != image2.getpixel((x, y)):
                return False
    return True
