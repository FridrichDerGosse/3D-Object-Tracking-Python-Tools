"""
_common_functions.py
26. November 2024

Functions used by both the client and the server

Author:
Nilusink
"""
from pydantic import TypeAdapter, ValidationError
from contextlib import suppress
from traceback import print_exc
from uuid import getnode
from time import time
import socket
import json

from ._message_future import MessageFuture
from ._message_types import *
from core.tools import debugger


DEVICE_MAC: int = getnode()


def try_find_id(message: str) -> int:
    """
    tries to find an id in an invalid message
    :return: id if found, -1 if not
    """
    # try to read as normal json
    try:
        data = json.loads(message)
        mid = data["id"]

        debugger.trace(f"found id in message (json): \"{mid}\"")
        return mid

    except (json.JSONDecodeError, TypeError):
        sid = '"id":'

        # if json fails, try to manually find it
        if sid in message:
            # try to find id key in message
            string_pos = message.find(sid) + len(sid)
            id_message = message[string_pos:].lstrip()

            # scan message until next non-digit
            pos = 0
            while id_message[pos].isdigit():
                pos += 1

            # cut message and try to convert to int
            with suppress(ValueError):
                mid = int(id_message[:pos])

                debugger.trace(f"found id in message (manual): \"{mid}\"")
                return mid

    # if message is completely unreadable, return -1
    return -1


def prepare_message(
        data: MessageData,
        message_queue_callback: tp.Callable[[Message], None]
) -> tuple[Message, MessageFuture | None]:
    """
    converts message data to a message, adding type, id and time
    """
    match data:
        case ReqData(req=_):
            type_name = "req"
            message_type = ReqMessage

        case AckData(to=_, ack=_):
            type_name = "ack"
            message_type = AckMessage

        case ReplData(to=_, data=_):
            type_name = "repl"
            message_type = ReplMessage

        case DataDataMessage():
            type_name = "data"
            message_type = DataMessage

        case _:
            debugger.error("invalid message data for send")
            raise ValueError("invalid message data")

    # encapsulate message
    t = time()
    message = message_type(
        type=type_name,
        id=int(t + DEVICE_MAC),
        time=t,
        data=data
    )

    # if message wants a reply, add it to pending
    future = None
    if message.type != "ack":
        future = MessageFuture(message)

        debugger.trace("DataServer: appending message to pending")

        message_queue_callback(future)

    return message, future


def receive_message(
        s: socket.socket,
        send_callback: tp.Callable[[MessageData], None],
        encoding: str = "utf-8"
) -> Message:
    """
    receives a message and converts it to Pydantic
    """
    # receive message
    try:
        data = s.recv(2048).decode(encoding)

    except socket.timeout:
        return ...

    except (ConnectionResetError, OSError, ConnectionAbortedError) as e:
        debugger.error("fatal network error: ", e)
        raise RuntimeError

    except Exception:
        debugger.error("unknown error on receive")
        raise RuntimeError

    if data == "":
        debugger.error("server disconnected")
        raise RuntimeError

    # try validating to json
    try:
        json_data = json.loads(data)

    except json.JSONDecodeError:
        debugger.error(f"received broken message: {data}")

        # send NACK to server
        send_callback(
            AckData(to=try_find_id(data), ack=False)
        )
        return ...

    # validate message
    message_adapter = TypeAdapter(Message)
    try:
        validated_data = message_adapter.validate_python(json_data)

    except ValidationError:
        debugger.error(f"received invalid message: {data}")

        print_exc()

        # send NACK to server
        send_callback(
            AckData(to=try_find_id(data), ack=False)
        )
        return ...

    return validated_data