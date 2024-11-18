"""
_data_types.py
14. November 2024

<description>

Author:
Nilusink
"""
from dataclasses import dataclass
from ._vectors import Vec2


@dataclass()
class Box:
    position: Vec2
    size: Vec2

    @property
    def center(self) -> Vec2:
        return Vec2.from_cartesian(
            self.position.x + self.size.x / 2,
            self.position.y + self.size.y / 2
        )

    def __repr__(self) -> str:
        return f"Box<position: {self.position}, size: {self.size}>"


if __name__ == "__main__":
    b = Box(Vec2.from_cartesian(1, 2), Vec2.from_cartesian(2, 3))
    print(b, b.center)