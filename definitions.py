from __future__ import annotations
from typing import Callable
import math

import PIL
from PIL import Image

def intify(t: tuple[float, ...]) -> tuple[int, ...]:
    return tuple(map(int, t))

def clamp(x, low, high):
    if (x < low): return low
    if (x > high): return high
    return x

def normalize_01(x, low, high):
    "[0, 1]"
    return (x-low)/(high-low)

def normalize_11(x, low, high):
    "[-1, 1]"
    n = normalize_01(x, low, high)
    return n*2 - 1

def unnormalize_01(n, low, high):
    "[low, high]"
    return low + n*(high-low)

def unnormalize_11(n1, low, high):
    "[low, high]"
    n = (n1 + 1)/2
    return unnormalize_01(n, low, high)


class Color:
    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b
        
    def copy(self) -> Color:
        return Color(self.r, self.g, self.b)
    
    @staticmethod
    def normal_to_255(x: float) -> int:
        return clamp(int(x*255), 0, 255)
    
    @staticmethod
    def from_rgb_255(r: int, g: int, b: int) -> Color:
        return Color(r/255, g/255, b/255)
    
    @staticmethod
    def from_tuple_255(color: tuple[int, int, int]) -> Color:
        return Color(*color)
    
    def to_rgb_255(self) -> tuple[int, ...]:
        return tuple( map(self.normal_to_255, [self.r, self.g, self.b] ) )
        
def get_color_at(img: Image.Image, point: tuple[int, int]) -> Color:
    color = img.getpixel(point)
    return Color.from_rgb_255(*color)

def put_color_at(img: Image.Image, point: tuple[int, int], color: Color):
    img.putpixel(intify(point), color.to_rgb_255())


def distance(p1, p2 = (0,0)):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx*dx + dy*dy)

    
def normalize_point(
    point: tuple[float, float], 
    sizes: tuple[int, int], 
    normalizer: Callable[ [float,float,float], float ]
) -> tuple[float, float]:
    return tuple( [
        normalizer(point[0], 0, sizes[0]),
        normalizer(point[1], 0, sizes[1]),    
    ] )

