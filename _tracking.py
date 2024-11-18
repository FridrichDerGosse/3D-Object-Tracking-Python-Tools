"""
_tracking.py
14. November 2024

<description>

Author:
Nilusink
"""
import typing as tp
from ._data_types import Box, Vec2


class Track:
    movement_threshold: float = 50
    track_timeout: int = 20

    last_box: Box
    position_history: list[Vec2]

    _track_type: int  # -1: degraded, 0: new / unclassified, 1: tracking / valid
    _current_timeout: int

    def __init__(self, box: Box) -> None:
        self._current_timeout = self.track_timeout
        self.position_history = [box.center]
        self.last_box = box

        self._track_type = 0

    @property
    def track_type(self) -> int:
        return self._track_type

    def in_range(self, box: Box) -> bool:
        """
        check if a new box is in range
        """
        return abs(
            (box.center - box.center).length
        ) < max(
            self.last_box.size.x, self.last_box.size.y
        ) / 4

    def update_track(self, box: Box | None = None) -> None:
        if self._track_type == -1:
            return

        if box is None:
            self._current_timeout -= 1

            if self._current_timeout < 0:
                print(self, "degraded")
                self._track_type = -1

            return

        if self._track_type == 0:
            self._current_timeout = self.track_timeout
            self.position_history.append(box.center)

            if abs(
                    (self.position_history[0] - self.position_history[-1]).length
            ) > self.movement_threshold:
                self._track_type = 1

        elif self._track_type == 1:
            self._current_timeout = self.track_timeout
            self.position_history.append(box.center)

        else:
            ...

        self.last_box = box

    def __repr__(self):
        return f"Track<center: {self.last_box.center}, type: {self.track_type}>"