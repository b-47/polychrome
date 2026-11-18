import platform
import time
import timeit
import tracemalloc

import PIL
from PIL import Image


def via_getpixel(img, sample_every):
    width, height = img.size
    total = width*height
    pixels = []
    for i in range(0, total, sample_every):
        x = i % width
        y = i // width
        pixels.append(img.getpixel((x, y)))
    return pixels

def via_flattened(img, sample_every):
    pixels = img.get_flattened_data()
    pixels = pixels[::sample_every]
    return list(pixels)

def via_tobytes(img, sample_every):
    pixel_bytes = img.tobytes()
    pixels = []
    for i in range(0, len(pixel_bytes), 4*sample_every):
        pixels.append(tuple(pixel_bytes[i:i+4]))
    return pixels

def via_tobytes_noloop(img, sample_every):
    pixel_bytes = img.tobytes()

    return list(zip(
        pixel_bytes[0::4*sample_every],
        pixel_bytes[1::4*sample_every],
        pixel_bytes[2::4*sample_every],
        pixel_bytes[3::4*sample_every]
        ))

APPROACHES = {
    "getpixel": via_getpixel,
    "get_flattened_data": via_flattened,
    "tobytes": via_tobytes,
    "tobytes_noloop": via_tobytes_noloop,
}

def make_check_image():
    img = Image.new("RGBA", (7, 5))
    img.putdata([(i, 2 * i % 256, 3 * i % 256, 255) for i in range(7 * 5)])
    return img

def check():
    img = make_check_image()
    for n in (1, 2, 5, 100):
        expected = via_getpixel(img, n)
        for name, func in APPROACHES.items():
            got = func(img, n)
            assert got == expected, f"{name} differs at sample_every={n}: {got[:3]}..."
    print("all approaches agree")

def measure_time(func, img, n):
    wall = min(timeit.repeat(lambda: func(img, n), number=1, repeat=3))
    cpu = min(timeit.repeat(lambda: func(img, n), number=1, repeat=3, timer=time.process_time))
    return wall, cpu

def measure_memory(func, img, n):
    tracemalloc.start()
    result = func(img, n)
    kept, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del result
    return peak, kept

def bench():
    print(f"Python {platform.python_version()}, Pillow {PIL.__version__}, {platform.machine()}")
    img = Image.new("RGBA", (4000, 3000), (220, 30, 30, 255))
    for name, func in APPROACHES.items():
        for n in (1, 10):
            wall, cpu = measure_time(func, img, n)
            peak, kept = measure_memory(func, img, n)
            print(
                f"{name:<20} sample_every={n:<3} "
                f"wall {wall:6.3f} s  cpu {cpu:6.3f} s  "
                f"peak {peak / 1e6:5.0f} MB  kept {kept / 1e6:5.0f} MB"
            )

if __name__ == "__main__":
    check()
    bench()
