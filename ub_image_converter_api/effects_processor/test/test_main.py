"""
Unittests for effects_processor
"""
from hashlib import md5
from pathlib import Path
from unittest.mock import patch

import cv2 as cv  # type: ignore
import numpy as np

import pytest

from ..main import ImgProcessor
from .utils.hashes import get_hashes, get_effect_hash


with open(f"{Path(__file__).parent.absolute()}/utils/city.jpg", "rb") as f:
    image = f.read()
    test = ImgProcessor(image)


img_hashes = get_hashes(test)


def test_all_effects_hashes():
    """Test the hashes dict against the processed images"""
    img_hashes.pop("noise")  # Noise effect needs a special test case
    for effect in img_hashes:
        assert img_hashes[effect] == get_effect_hash(test, effect)


@pytest.mark.timeout(2)
def test_noise():
    """Test noise effect and hash"""

    def mocked_noise() -> np.ndarray:
        noise = np.zeros(test.src_image().shape, dtype=np.float64)
        cv.randn(noise, 0, 128)
        return cv.add(test.src_image(), np.array(1.5 * noise), dtype=cv.CV_64F)

    noisy = mocked_noise()
    with patch.object(test, "noise", return_value=noisy):
        inner_img_hashes = get_hashes(test)
        test.noise.assert_called()  # pylint: disable=no-member
        assert inner_img_hashes["noise"] == md5(test.noise()).hexdigest()

        assert inner_img_hashes["noise"] == md5(test.noise(-1)).hexdigest()
        assert inner_img_hashes["noise"] == md5(test.noise("I_@m_a_$tr1ng")).hexdigest()
        assert md5(test.noise(1000)).hexdigest() == md5(test.noise(1000)).hexdigest()


@pytest.mark.timeout(1)
def test_blur():
    """Test blur effect"""
    assert img_hashes["blur"] == md5(test.blur(-1)).hexdigest()
    assert img_hashes["blur"] == md5(test.blur(0)).hexdigest()
    assert img_hashes["blur"] == md5(test.blur("I_@m_a_$tr1ng")).hexdigest()
    assert md5(test.blur(3)).hexdigest() == md5(test.blur(2)).hexdigest()
    assert md5(test.blur(99)).hexdigest() == md5(test.blur(98)).hexdigest()
    assert md5(test.blur()).hexdigest() == md5(test.blur(10000)).hexdigest()


def test_flip():
    """Test flip effect"""
    assert img_hashes["flip"] == md5(test.flip(1)).hexdigest()
    assert img_hashes["flip"] == md5(test.flip("I_@m_a_$tr1ng")).hexdigest()
    assert img_hashes["flip"] == md5(test.flip("B")).hexdigest()


def test_laplacian():
    """Test laplacian effect"""
    assert img_hashes["laplacian"] == md5(test.laplacian(-1)).hexdigest()
    assert img_hashes["laplacian"] == md5(test.laplacian(0)).hexdigest()
    assert img_hashes["laplacian"] == md5(test.laplacian("I_@m_a_$tr1ng")).hexdigest()
    assert md5(test.laplacian(3)).hexdigest() == md5(test.laplacian(2)).hexdigest()
    assert md5(test.laplacian(31)).hexdigest() == md5(test.laplacian(30)).hexdigest()
    assert md5(test.laplacian()).hexdigest() == md5(test.laplacian(10000)).hexdigest()


@pytest.mark.timeout(4)
def test_scale():
    """Test scale effect"""
    assert img_hashes["scale"] == md5(test.scale(-1)).hexdigest()
    assert img_hashes["scale"] == md5(test.scale("I_@m_a_$tr1ng")).hexdigest()
    assert md5(test.scale()).hexdigest() == md5(test.scale(6)).hexdigest()
    assert md5(test.scale(5)).hexdigest() == md5(test.scale(5)).hexdigest()


def test_sobel():
    """Test sobel effect"""
    assert img_hashes["sobel"] == md5(test.sobel(-1)).hexdigest()
    assert img_hashes["sobel"] == md5(test.sobel("I_@m_a_$tr1ng")).hexdigest()
    assert md5(test.sobel(31)).hexdigest() == md5(test.sobel(30)).hexdigest()
    assert md5(test.sobel()).hexdigest() == md5(test.sobel(1000)).hexdigest()
