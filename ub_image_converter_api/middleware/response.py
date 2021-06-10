"""
Handle requests based on a json format
"""

from typing import Dict, List
from ..effects_processor.main import ImgProcessor


class RequestHandler:
    """Process request and build appropriate response"""

    errors_map = {
        "notJson": [0, "Expected request in Json format"],
        "noImage": [1, "No image to process"],
        "noEffects": [2, "No effects given"],
        "weightExceeded": [3, "Sum of effect's weight exceeds limit"],
        "invalidImgFormat": [4, "Invalid image format"]
    }

    def __init__(self, request: dict):
        """
        Args:
            - request (dict): requets to be processed
        """
        self.request = request
        self.effect_weight_map = ImgProcessor.effect_weight
        

    def _build_error_template(self, error_type: str, effects_weight: list=[]) -> dict:
        ''''Error response Template

        Args:
            - error_type (str): Name of defined error
            - effects_weight (list): Weight of each effect. Only positive integers. Default: empty list

        Returns:
            - dict: Error template
        '''
        error_template = {
            "cod": self.errors_map[error_type][0],
            "msg": self.errors_map[error_type][1]
        }

        if effects_weight:
            error_template["effect_weight"] = effects_weight
            error_template["total_effect_weight"] = sum(effects_weight)

        return error_template


    def _verify_effects_weight(self,effects_to_apply: List[str], max_weight: int=50) -> bool:
        return self._getTotalWeight(effects_to_apply) <= (1 if max_weight < 1 else max_weight)


    def _getEffectsWeight(self, effects_to_apply: List[str]) -> List[int]:
        return [self.effect_weight_map[e] for e in effects_to_apply]


    def _getTotalWeight(self, effects_to_apply: List[str]) -> int:
        return sum(self._getEffectsWeight(effects_to_apply))

    
    def _build_success_template(self, img: bytes) -> Dict:
        success_template =  {
            "img": img,
            "msg": "Image processed correctly"
        }
        return success_template


    def build_response(self):
        try:
            data = self.request.loads()
        except:
            response_template = self._build_error_template("notJson")
            return response_template

        img = data.get("img", None)
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

