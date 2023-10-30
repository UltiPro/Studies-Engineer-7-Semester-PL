class AddOperation:
    def transform(self, val: int, transformation_val) -> int:
        new_val = val + transformation_val
        return round(new_val)


class SubOperation:
    def transform(self, val: int, transformation_val) -> int:
        new_val = val - transformation_val
        return round(new_val)


class MulOperation:
    def transform(self, val: int, transformation_val) -> int:
        new_val = val * transformation_val
        return round(new_val)


class DivOperation:
    def transform(self, val: int, transformation_val) -> int:
        if transformation_val == 0:
            transformation_val = 1
        new_val = val / transformation_val
        return round(new_val)
