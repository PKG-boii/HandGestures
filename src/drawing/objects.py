from dataclasses import dataclass
from typing import List, Tuple


Point = Tuple[float, float]


@dataclass
class Stroke:
    points: List[Point]
    color: Tuple[int, int, int]
    width: int
    opacity: int = 255
    tool: str = "pen"
