#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rectangle import Rectangle
import random

rectangles = []
n = random.randint(10, 1000)

for _ in range(n):
    h = random.randint(1, 10)
    b = random.randint(1, 10)
    rectangles.append(Rectangle(b, h))

# Print squares
for r in rectangles:
    if r.square:
        print(r)

# Find maxima
max_area = 0.0
max_perimeter = 0.0
max_side = 0.0

for r in rectangles:
    if r.area() > max_area:
        max_area = r.area()
    if r.perimeter() > max_perimeter:
        max_perimeter = r.perimeter()
    if r.longest_side() > max_side:
        max_side = r.longest_side()

print("Those with the largest area are:")
for r in rectangles:
    if r.area() == max_area:
        print(r)

print("Those with the largest perimeter are:")
for r in rectangles:
    if r.perimeter() == max_perimeter:
        print(r)

print("Those with the largest side are:")
for r in rectangles:
    if r.longest_side() == max_side:
        print(r)

print("Converting those with the largest side into squares")
for r in rectangles:
    if r.longest_side() == max_side and not r.square:
        print("Was:", r)
        changed_base = r.make_square()
        print("Now:", r, end=" ")
        if changed_base:
            print("(Base was changed)")
        else:
            print("(Height was changed)")
