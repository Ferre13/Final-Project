import random

class Rectangle:
    def __init__(self, base, height=None):
        if height is None:
            self.height = base
        else:
            self.height = height
        self.base = base

    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Base must be a number.")
        if value <= 0:
            raise ValueError("Base must be positive.")
        self.__base = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Height must be a number.")
        if value <= 0:
            raise ValueError("Height must be positive.")
        self.__height = value

    @property
    def square(self):
        return self.base == self.height

    def __str__(self):
        if self.square:
            shape = "square"
        else:
            shape = "rectangle"
        return f"a {shape} with base {self.base} and height {self.height}"

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (self.base == other.base and self.height == other.height) or (self.base == other.height and self.height == other.base)

    def perimeter(self):
        return 2 * (self.base + self.height)

    def area(self):
        return self.base * self.height

    def longest_side(self):
        if self.base >= self.height:
            return self.base
        else:
            return self.height

    def rect_to_square(self):
        longest = self.longest_side()
        if self.base < longest:
            self.base = longest
            return True
        elif self.height < longest:
            self.height = longest
            return False

    def __lt__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.longest_side() < other.longest_side()

    def __le__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.longest_side() <= other.longest_side()

    def __gt__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.longest_side() > other.longest_side()

    def __ge__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.longest_side() >= other.longest_side()

if __name__ == "__main__":
    elements = random.randint(10, 1000)
    rectangles = []
    for rect in range(elements):
        base = random.randint(1, 10)
        height = random.randint(1, 10)
        rectangles.append(Rectangle(base, height))

    print("\nSquare rectangles")
    for sq in rectangles:
        if sq.square:
            print(sq)

    max_area = 0
    for rect in rectangles:
        if rect.area() > max_area:
            max_area = rect.area()
    print(f"\nRectangles with largest area ({max_area}):")
    for rect in rectangles:
        if rect.area() == max_area:
            print(rect)

    max_perimeter = 0
    for rect in rectangles:
        if rect.perimeter() > max_perimeter:
            max_perimeter = rect.perimeter()
    print(f"\nRectangles with largest perimeter ({max_perimeter}):")
    for rect in rectangles:
        if rect.perimeter() == max_perimeter:
            print(rect)

    max_side = 0
    largest_side_rects = []
    for rect in rectangles:
        if rect.longest_side() > max_side:
            max_side = rect.longest_side()
    print(f"\nRectangles with largest side ({max_side}):")
    for rect in rectangles:
        if rect.longest_side() == max_side:
            print(rect)
            largest_side_rects.append(rect)

    print("\nConverting largest side rectangles to squares")
    for rect in largest_side_rects:
        print(f"\nOld {rect}")
        changed = rect.rect_to_square()
        if changed is True:
            print("Base was changed.")
        elif changed is False:
            print("Height was changed.")
        else:
            print("It was already a square.")
        print(f"New: {rect}")
