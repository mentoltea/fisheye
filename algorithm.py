import PIL
from PIL import Image
from definitions import *

def disturbance(point: tuple[float, float]) -> float:
    def f(t):
        # return math.sqrt(abs(math.log(abs(t))))
        return math.exp(-(t*t))
    
    return ( 1 - 1/( f( distance(point) ) + 1 ) )

def translate(coord11: tuple[float, float], radius: float) -> tuple[float, float]:
    "[-1, 1]^2"
    d = distance(coord11)
    
    if (d==0): 
        return (0,0)
    direction = tuple(map(lambda t: t/d, coord11))
    dist = disturbance(coord11)
    # print(f"{dist}")
    
    return tuple(map(lambda i: coord11[i] - direction[i]*dist*radius, [0, 1]) )

def fisheye(original: Image.Image, fishcenter: tuple[float, float], fishradius: float) -> Image.Image:
    edited = Image.new(original.mode, original.size)
    edited = edited.convert("RGB")
    sizes = (xsize, ysize) = original.size
    
    for y in range(ysize):
        for x in range(xsize):
            p11 = normalize_point((x,y), sizes, normalize_11)
            
            fishcoords = tuple(map(lambda i: (p11[i] - fishcenter[i]), [0, 1]))
            
            fishtrans = translate(fishcoords, fishradius)
            
            trans = tuple(map(lambda i: fishtrans[i] + fishcenter[i], [0, 1]))
            
            other = list(normalize_point(trans, sizes, unnormalize_11))
            other[0] = clamp(other[0], 0, xsize-1)
            other[1] = clamp(other[1], 0, ysize-1)
            
            col = get_color_at(original, other)
            
            put_color_at(
                edited,
                (x,y),
                col
            )    
    return edited


def alg(original: Image.Image) -> Image.Image:
    edited = original.copy()
    
    # edited = fisheye(edited, (-0.75, -0.75), 0.45)
    # edited = fisheye(edited, (0.75, -0.75), 0.35)
    # edited = fisheye(edited, (-0.75, 0.75), 0.25)
    # edited = fisheye(edited, (0.75, 0.75), 0.55)
    
    # for i in range(5):
    #     edited = fisheye(edited, (-0.1 + i*0.05, -0.1 + i*0.05), 0.3 + i*0.07)    
    
    edited = fisheye(edited, (0,-0.1), 2)    
    
    return edited