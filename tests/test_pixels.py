import pytest
from PIL import Image

from polychrome.pixels import load_pixels


def solid(color, size=(2, 2)):
    return Image.new("RGB", size, color)


@pytest.mark.parametrize("sample_every", [0, -1])
def test_sample_every_below_1_raises(sample_every):
    with pytest.raises(ValueError, match="sample_every"):
        load_pixels(solid("red"), sample_every=sample_every)

@pytest.mark.parametrize("image", [None, b"bytes", 42])
def test_image_wrong_type_raises(image):
    with pytest.raises(TypeError, match="image"):
        load_pixels(image)