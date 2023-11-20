from src.shapes import Shape


def write(filename: str, shapes: list[Shape]):
    buff = ""
    for shape in shapes:
        for num in shape.coords:
            buff += f"{num} "
        buff += "\n"

    with open(filename, "w") as f:
        f.write(buff)


def read(filename: str) -> list[Shape]:
    shapes: list[Shape] = []
    with open(filename, "r") as f:
        for line in f:
            coords = [int(val) for val in line.split()]
            shapes.append(Shape(coords))

    return shapes
