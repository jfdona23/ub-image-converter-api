from typing import Any, Dict, List, Optional

from numpy import isin
from ..response import RequestHandler

def makeRequest(effects: Optional[List[str]], fileb64: Optional[str], malformed: bool=False) -> Dict:
    # An empty dictionary is also malformed but i wanted to also test one with diferents keys:values
    if malformed:
        m = {
            "xxx": "",
            "bla": [],
            "extra": 0
        }
        return m
    
    r: Dict[str, Any] = dict()
    if isinstance(fileb64, str):
        with open(fileb64, "r") as f:
            txt = f.read()
        r["img"] = txt
    if isinstance(effects, list):
        r["effects"] = effects
    
    return r 


def error_json(error: str) -> Dict[int, str]:
    errors_map = {
    "notJson": [0, "Expected request in Json format"],
    "noImage": [1, "No image to process"],
    "noEffects": [2, "No effects given"],
    "weightExceeded": [3, "Sum of effect's weight exceeds limit"],
    "malformedJson": [4, "Invalid Json format"]
    }
    json = {
        "cod": errors_map[error][0],
        "msg": errors_map[error][1]
    }
    return json


def test_RequestHandler_build_response_errors():
    r = RequestHandler(None)
    assert RequestHandler.build_response() == error_json("notJson")
    r = RequestHandler(makeRequest(effects=None, fileb64=None))
    assert r.build_response == error_json("malformedJson")
    r = RequestHandler(makeRequest(effects=None, fileb64=None, malformed=True))
    assert r.build_response == error_json("malformedJson")
    r = RequestHandler(makeRequest(makeRequest(effects=["negative"], fileb64=None)))
    assert r.build_response == error_json("noImage")
    r = RequestHandler(makeRequest(effects=None, fileb64="text.b64"))
    assert r.build_response == error_json("noEffects")
    r = RequestHandler(makeRequest(effects=["negative","scale","sepia","sharp","sobel"], fileb64="text.b64"))
    assert r.build_response == error_json("weightExceeded") # weight: 51
    
