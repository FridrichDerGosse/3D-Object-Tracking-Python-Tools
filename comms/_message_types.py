"""
_message_types.py
20. November 2024

implements all message types according to the protocol

Author:
Nilusink
"""
from pydantic import BaseModel, Field
import typing as tp


# data message types
class CamAngle(BaseModel):
    cam_id: int
    direction: tuple[float, float]


class CamAngle3(BaseModel):
    cam_id: int
    position: tuple[float, float, float]
    direction: tuple[float, float, float]


class TResData(BaseModel):
    track_id: int
    cam_angles: list[CamAngle]


class TRes3Data(BaseModel):
    track_id: int
    position: tuple[float, float, float]
    cam_angles: list[CamAngle3]


class SInfData(BaseModel):
    id: int
    position: tuple[float, float, float]
    direction: tuple[float, float, float]
    fov: tuple[float, float]
    resolution: tuple[float, float]


# message data types
class TResDataMessage(BaseModel):
    type: tp.Literal["tres"] = "tres"
    data: TResData


class TRes3DataMessage(BaseModel):
    type: tp.Literal["tres3"] = "tres3"
    data: TRes3Data


class SInfDataMessage(BaseModel):
    type: tp.Literal["sinf"] = "sinf"
    data: SInfData


DataDataMessage = tp.Annotated[tp.Union[TResDataMessage, TRes3DataMessage, SInfDataMessage], Field(discriminator='type')]


class ReqData(BaseModel):
    req: str


class AckData(BaseModel):
    to: int
    ack: bool


class ReplData(BaseModel):
    to: int
    data: dict


# message
class _Message(BaseModel):
    type: str
    id: int
    time: float

class ReqMessage(_Message):
    type: tp.Literal["req"] = "req"
    data: ReqData

class AckMessage(_Message):
    type: tp.Literal["ack"] = "ack"
    data: AckData

class ReplMessage(_Message):
    type: tp.Literal["repl"] = "repl"
    data: ReplData

class DataMessage(_Message):
    type: tp.Literal["data"] = "data"
    data: DataDataMessage


Message = tp.Annotated[tp.Union[ReqMessage, AckMessage, ReplMessage, DataMessage], Field(discriminator='type')]
MessageData = tp.Union[ReqData, AckData, ReplData, DataDataMessage]
