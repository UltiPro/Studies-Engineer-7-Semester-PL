from PIL.Image import Image
import statistics


def get_pixels_in_mask(
    image: Image, pos: tuple[int, int], mask_dims=3
) -> tuple[list[tuple], list]:
    pixels = []
    mask_indices = []
    w, h = image.size
    positions = []
    offset = mask_dims // 2
    for y in range(-offset, offset + 1):
        for x in range(-offset, offset + 1):
            positions.append((x, y))
    i = 0
    for dx, dy in positions:
        x = pos[0] + dx
        y = pos[1] + dy
        if x < 0 or x > w - 1:
            continue
        if y < 0 or y > h - 1:
            continue
        mask_indices.append(i)
        pixels.append(image.getpixel((x, y)))
        i += 1
    return pixels, mask_indices


class AverageFilter:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        new_image = image.copy()
        for x in range(0, w):
            for y in range(0, h):
                pixels_in_mask, indices = get_pixels_in_mask(image, (x, y))
                r = round(
                    sum([pixel[0] for pixel in pixels_in_mask]) / len(pixels_in_mask)
                )
                g = round(
                    sum([pixel[1] for pixel in pixels_in_mask]) / len(pixels_in_mask)
                )
                b = round(
                    sum([pixel[2] for pixel in pixels_in_mask]) / len(pixels_in_mask)
                )
                new_image.putpixel((x, y), (r, g, b))
        return new_image


class MedianFilter:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        new_image = image.copy()

        for x in range(0, w):
            for y in range(0, h):
                pixels_in_mask, indices = get_pixels_in_mask(image, (x, y))
                r = round(statistics.median([pixel[0] for pixel in pixels_in_mask]))
                g = round(statistics.median([pixel[1] for pixel in pixels_in_mask]))
                b = round(statistics.median([pixel[2] for pixel in pixels_in_mask]))
                new_image.putpixel((x, y), (r, g, b))

        return new_image


class SobelFilter:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        new_image = image.copy()
        x_kernel = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
        y_kernel = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
        for x in range(0, w):
            for y in range(0, h):
                pixels_in_mask, indices = get_pixels_in_mask(image, (x, y))
                grayscale_pixels = [sum(pixel) / 3 for pixel in pixels_in_mask]
                x_mag = sum([grayscale_pixels[i] * x_kernel[i] for i in indices])
                y_mag = sum(
                    [pixel * y_kernel[i] for i, pixel in enumerate(grayscale_pixels)]
                )
                mag = round((x_mag**2 + y_mag**2) ** 0.5)
                new_image.putpixel((x, y), (mag, mag, mag))
        return new_image


class HighPassFilter:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        new_image = image.copy()
        x_kernel = [-1, -1, -1, -1, 9, -1, -1, -1, -1]
        for x in range(0, w):
            for y in range(0, h):
                pixels_in_mask, indices = get_pixels_in_mask(image, (x, y))
                grayscale_pixels = [sum(pixel) / 3 for pixel in pixels_in_mask]
                mag = round(sum([grayscale_pixels[i] * x_kernel[i] for i in indices]))
                new_image.putpixel((x, y), (mag, mag, mag))
        return new_image


class GaussianFilter:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        new_image = image.copy()
        x_kernel = [1, 2, 1, 2, 4, 2, 1, 2, 1]
        for x in range(0, w):
            for y in range(0, h):
                pixels_in_mask, indices = get_pixels_in_mask(image, (x, y))
                grayscale_pixels = [sum(pixel) / 3 for pixel in pixels_in_mask]

                sum_of_vals = sum([grayscale_pixels[i] * x_kernel[i] for i in indices])
                mag = round(sum_of_vals / 16)

                new_image.putpixel((x, y), (mag, mag, mag))
        return new_image


class GrayscaleFilter:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        for x in range(w):
            for y in range(h):
                gray = round(sum(image.getpixel((x, y))) / 3)
                image.putpixel((x, y), (gray, gray, gray))
        return image


class GrayscaleFilterTwo:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        for x in range(w):
            for y in range(h):
                r, g, b = image.getpixel((x, y))
                gray = (max(r, g, b) + min(r, g, b)) / 2
                gray = round(gray)
                image.putpixel((x, y), (gray, gray, gray))
        return image


class GrayscaleFilterThree:
    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        for x in range(w):
            for y in range(h):
                r, g, b = image.getpixel((x, y))
                gray = r * 0.3 + g * 0.6 + b * 0.11
                gray = round(gray)
                image.putpixel((x, y), (gray, gray, gray))
        return image


class CustomFilter:
    def __init__(self, dims: int, weights: list[int]):
        self.dims = dims
        self.weights = weights

    def apply_filter(self, image: Image) -> Image:
        w, h = image.size
        new_image = image.copy()
        for x in range(0, w):
            for y in range(0, h):
                pixels_in_mask, indices = get_pixels_in_mask(
                    image, (x, y), mask_dims=self.dims
                )
                grayscale_pixels = [sum(pixel) / 3 for pixel in pixels_in_mask]
                sum_of_vals = sum(
                    [grayscale_pixels[i] * self.weights[i] for i, pixel in indices]
                )
                mag = round(
                    sum_of_vals
                    / calculate_normalize_factor([self.weights[i] for i in indices])
                )
                new_image.putpixel((x, y), (mag, mag, mag))
        return new_image


def calculate_normalize_factor(weights: list[int]):
    weights_sum = sum(weights)
    if weights_sum == 0:
        return 1
    return weights_sum
