"""
Unittests for effects_processor
"""
from hashlib import md5
from pathlib import Path
from unittest.mock import patch

import cv2 as cv  # type: ignore
import numpy as np

from ..main import ImgProcessor
from .utils.hashes import get_hashes, get_effect_hash


with open(f"{Path(__file__).parent.absolute()}/utils/city.jpg", "rb") as f:
    image = f.read()
    test = ImgProcessor(image)

IMG_HASHES = get_hashes(test)


def test_hashes():
    """Test the hashes dict against the processed images"""
    IMG_HASHES.pop("noise")  # Noise effect needs a special test case
    for effect in IMG_HASHES:
        assert IMG_HASHES[effect] == get_effect_hash(test, effect)


def test_noise():
    """Test noise effect"""

    def mocked_noise() -> np.ndarray:
        noise = np.zeros(test.src_image().shape, dtype=np.float64)
        cv.randn(noise, 0, 128)
        return cv.add(test.src_image(), np.array(1.5 * noise), dtype=cv.CV_64F)

    noisy = mocked_noise()
    with patch.object(test, "noise", return_value=noisy):
        temp_img_hashes = get_hashes(test)
        test.noise.assert_called()  # pylint: disable=no-member
        assert temp_img_hashes["noise"] == md5(test.noise()).hexdigest()
