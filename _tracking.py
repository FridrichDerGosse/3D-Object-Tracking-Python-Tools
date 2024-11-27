"""
_tracking.py
14. November 2024

<description>

Author:
Nilusink
"""
from dataclasses import dataclass
from ._data_types import Vec3

# raise NotImplementedError("not rewritten to 3d")

class Track:
    # movement_threshold: float = 50
    # track_timeout: int = 20
    #
    # last_box: Box
    position_history: list[Vec3]

    _track_type: int  # -1: degraded, 0: new / unclassified, 1: tracking / valid
    _id: int
    # _current_timeout: int

    def __init__(self, track_id: int, pos: Vec3, track_type: int) -> None:
        self._id = track_id
        self.position_history = [pos.copy()]
        # self.last_box = box

        self._track_type = track_type

    @property
    def track_type(self) -> int:
        return self._track_type

    @property
    def id(self) -> int:
        return self._id

    @property
    def position(self) -> Vec3:
        return self.position_history[-1]

    def update_track(self, pos: Vec3, track_type: int | None = None) -> None:
        """
        append position to track and optionally update track type
        """
        if track_type is not None:
            self._track_type = track_type

        self.position_history.append(pos)

    def __repr__(self):
        return f"Track<center: {self.position}, type: {self.track_type}>"


@dataclass
class TrackUpdate:
    track_id: int
    pos: Vec3
    track_type: int
