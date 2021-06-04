"""
Unittests for effects_processor
"""
from hashlib import md5
from pathlib import Path

from ..main import ImgProcessor
from .utils.hashes import get_hashes


with open(f"{Path(__file__).parent.absolute()}/city.jpg", "rb") as f:
    image = f.read()
    test = ImgProcessor(image)

HASHES = get_hashes(test)

def test_init():
    """Test the constructor"""

def test_blur():
    """Test blur effect"""
    assert HASHES["blur"] == md5(test.blur()).hexdigest()

def test_emboss():
    """Test emboss effect"""
    assert HASHES["emboss"] == md5(test.emboss()).hexdigest()

def test_flip():
    """Test flip effect"""
    assert HASHES["flip"] == md5(test.flip()).hexdigest()

def test_grayscale():
    """Test grayscale effect"""
    assert HASHES["grayscale"] == md5(test.grayscale()).hexdigest()

def test_laplacian():
    """Test laplacian effect"""
    assert HASHES["laplacian"] == md5(test.laplacian()).hexdigest()

def test_negative():
    """Test negative effect"""
    assert HASHES["negative"] == md5(test.negative()).hexdigest()

def test_noise():
    """Test noise effect"""
    # assert HASHES["noise"] == md5(test.noise()).hexdigest()
    pass

def test_rotate():
    """Test rotate effect"""
    assert HASHES["rotate"] == md5(test.rotate()).hexdigest()

def test_scale():
    """Test scale effect"""
    assert HASHES["scale"] == md5(test.scale()).hexdigest()

def test_sepia():
    """Test sepia effect"""
    assert HASHES["sepia"] == md5(test.sepia()).hexdigest()

def test_sharp():
    """Test sharp effect"""
    assert HASHES["sharp"] == md5(test.sharp()).hexdigest()

def test_sobel():
    """Test sobel effect"""
    assert HASHES["sobel"] == md5(test.sobel()).hexdigest()

def test_src_image():
    """Test src_image effect"""
    assert HASHES["src_image"] == md5(test.src_image()).hexdigest()
