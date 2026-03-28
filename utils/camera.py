import math
from pydantic.dataclasses import dataclass

@dataclass
class Camera: 
    fov: float
    zfar: float
    znear: float
    width: float
    height: float

    def aspect_ratio(self) -> float:
        return self.width/self.height

