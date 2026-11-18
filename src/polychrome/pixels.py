from pathlib import Path

from PIL import Image

type ImageSource = str | Path | Image.Image

def load_pixels(image: ImageSource, sample_every: int = 10) -> list[tuple[int, int, int]]:
    if sample_every < 1:
        raise ValueError(f"sample_every must be at least 1, got {sample_every}")
    if not isinstance(image, (str, Path, Image.Image)):
        raise TypeError(f"image must be a str, Path, or PIL Image, got {type(image).__name__}")
    
    if isinstance(image, (str, Path)):
        img = Image.open(image)
    else:
        img = image
    img = img.convert("RGBA")
    pixel_bytes = img.tobytes()

    pixels = zip(
        pixel_bytes[0::4*sample_every],
        pixel_bytes[1::4*sample_every],
        pixel_bytes[2::4*sample_every],
        pixel_bytes[3::4*sample_every]
        )
    pixels = [(r, g, b) for r, g, b, a in pixels if a >= 125 and min(r,g,b) <= 250]
    return pixels
    
    
    

    
