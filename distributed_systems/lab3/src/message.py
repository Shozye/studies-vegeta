from dataclasses import dataclass
from enum import StrEnum, auto


class MESSAGE_TYPE(StrEnum):
    MARKER = auto()
    SEND_RESOURCE = auto()

@dataclass
class Message:
    type: MESSAGE_TYPE

@dataclass(kw_only=True)
class MarkerMessage(Message):
    type: MESSAGE_TYPE=MESSAGE_TYPE.MARKER
    marker_id: str

@dataclass(kw_only=True)
class SendResourceMessage(Message):
    type: MESSAGE_TYPE=MESSAGE_TYPE.SEND_RESOURCE
    amount_resource: int

