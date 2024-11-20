"""
_combined_result.py
19. November 2024

A combination of 2d camera angles and 3d track

Author:
Nilusink
"""
from dataclasses import dataclass
import typing as tp

from ._data_types import AngularTrack
from ._tracking import TrackUpdate


@dataclass
class CombinedResult:
    camera_angles: tp.Iterable[AngularTrack]
    track_update: TrackUpdate
