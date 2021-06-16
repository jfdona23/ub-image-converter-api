"""
Handle requests based on a json format
"""
from base64 import b64decode, b64encode
from json import dumps
from typing import Dict, List
from ..effects_processor.main import ImgProcessor


class RequestHandler:
    """Process request and build appropriate response"""

    errors_map = {
        "notJson": [0, "Expected request in Json format"],
        "noImage": [1, "No image to process"],
        "noEffects": [2, "No effects given"],
        "weightExceeded": [3, "Sum of effect's weight exceeds limit"],
        "malformedJson": [4, "Invalid Json format"]
    }

    def __init__(self, request: dict):
        """
        Args:
            - request (dict): requets to be processed
        """
        self.request = request
        self.effect_weight_map = ImgProcessor.effect_weight
        
    def _effects_weight_apply_map(self, effects_to_apply: List[str]) -> Dict[str, int]:
        '''Makes dict of effects to apply with ther respective weights

        Args:
            - effects_to_apply (List[str]): effects to apply to image

        Returns:
            - Dict[str, int]: Effect - weight dictionary
        '''
        ew_map: Dict[str, int] = self.effect_weight_map
        new_map = dict()
        for e in effects_to_apply:
            new_map[e] = ew_map.get(e, 0)
        return new_map
        


    def _build_error_template(self, error_type: str, effects_weight: list=[], effects_to_apply: List[str]=[]) -> dict:
        ''''Error response Template

        Args:
            - error_type (str): Name of defined error
            - effects_weight (List[int]): Weight of each effect. Only positive integers. Default: empty list
            - effects_to_apply (List[str]): effects to apply to image. Default: empty list

        Returns:
            - dict: Error template
        '''
        error_template = {
            "cod": self.errors_map[error_type][0],
            "msg": self.errors_map[error_type][1]
        }

        if effects_weight:
            error_template["effect_weight"] = self._effects_weight_apply_map(effects_to_apply)
            error_template["total_effect_weight"] = sum(effects_weight)

        return error_template


    def _verify_effects_weight(self,effects_to_apply: List[str], max_weight: int=50) -> bool:
        '''Verify arbitrary limit for weight effects
        
        Args:
            - effects_to_apply (List[str]): effects to apply to image
            - max_weight (int): Maximun weight of sum of all effects. Only positive integers greater than 0. Default: 50

        Returns:
            - bool: True if total sum of effects weight less than maximun weight and greater than zero.
        '''
        return self._getTotalWeight(effects_to_apply) <= (1 if max_weight < 1 else max_weight)


    def _getEffectsWeight(self, effects_to_apply: List[str]) -> List[int]:
        '''Get list of weights for each effect to apply to image

        Args:
            - effects_to_apply (List[str]): effects to apply to image

        Returns:
            - List[int]: Previously set weight of each effect to apply.
        '''
        return [self.effect_weight_map[e] for e in effects_to_apply]


    def _getTotalWeight(self, effects_to_apply: List[str]) -> int:
        '''Get sum of weight of effects to apply to image

        Args:
            - effects_to_apply (List[str]): effects to apply to image

        Returns:
            - int: Total weight of list of effects
        '''
        return sum(self._getEffectsWeight(effects_to_apply))

    
    def _build_success_template(self, img: bytes) -> Dict:
        ''''Success response Template

        Args:
            - img (bytes): image to process

        Returns:
            - dict: Success template template
        '''
        img_b64 = b64encode(img).decode()
        success_template =  {
            "img": img_b64,
            "msg": "Image processed correctly"
        }
        return dumps(success_template)


    def build_response(self):
        if isinstance(self.request, dict):
            data = self.request
            if not all(["img" in data.keys(), "effects" in data.keys()]):
                response_template = self._build_error_template("malformedJson")
                return response_template
        else:
            response_template = self._build_error_template("notJson")
            return response_template

        img = b64decode(data.get("img", None))
        if not img:
            response_template = self._build_error_template("noImage")
            return response_template           

        effects: List[str] = data.get("effects", [])
        if not effects:
            response_template = self._build_error_template("noEffects")
            return response_template  
        if not self._verify_effects_weight(effects):
            response_template = self._build_error_template("weightExceeded")
            return response_template  
         
        i_p = ImgProcessor(img)
        for e in effects:
            getattr(i_p, e)()
            i_p = ImgProcessor(i_p.dst_image())

        return self._build_success_template(i_p.dst_image())

if __name__ == "__main__":

    with open("text.b64", "r") as f:
        txt = f.read()
        r = {
            "img": txt,
            "effects": [
                "negative",
            ]
        }
        req = RequestHandler(r)
        print(req.build_response())