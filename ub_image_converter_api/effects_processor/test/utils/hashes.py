"""
Hashes for the testing image.
If the image for testing changes, so these hashes
"""
from hashlib import md5
from pathlib import Path

from ...main import ImgProcessor


def get_effect_hash(obj: ImgProcessor, method: str) -> str:
    """Get the hash of the desired effect"""
    effect = getattr(obj, method, None)
    return md5(effect()).hexdigest()


def get_hashes(obj: ImgProcessor) -> dict:
    """Get the dict of hashes for each effect"""
    hashes = dict()
    methods = [m for m in dir(ImgProcessor) if m.startswith("_") is False]
    methods.remove("effect_weight")  # This is not an effect but an attribute
    for method in methods:
        hashes[method] = get_effect_hash(obj, method)
    return hashes


if __name__ == "__main__":
    with open(f"{Path(__file__).parent.absolute()}/city.jpg", "rb") as f:
        image = f.read()
        test = ImgProcessor(image)
    print(get_hashes(test))
