import queue
from typing import Optional
from .message import Message, MESSAGE_TYPE
import logging


class Channel:
    def __init__(self, from_pid: int, to_pid: int) -> None:
        self.from_pid: int = from_pid
        self.to_pid: int = to_pid
        self._queue = queue.SimpleQueue()
        self._recording = False
        self._recorded_messages: list[Message] = []

    def send(self, message: Message) -> None:
        logging.debug(f"Message sent on {repr(self)}: {message.type}")
        self._queue.put(message)

    def receive(self)-> Optional[Message]:
        if self._queue.empty():
            return None
        message = self._queue.get()
        if self._recording and message.type != MESSAGE_TYPE.MARKER:
            self._recorded_messages.append(message)
        logging.debug(f"Message received on {repr(self)}: {message.type}")
        return message

    def start_recording(self) -> None:
        logging.info(f"Started recording on {repr(self)}")
        self._recording = True
        self._recorded_messages = []

    def stop_recording(self) -> list[Message]:
        self._recording = False
        recorded_messages = self._recorded_messages[:]
        logging.info(f"Stopped recording on {repr(self)} with messages {recorded_messages}")
        return recorded_messages
    
    def __repr__(self) -> str:
        return f"{self.from_pid}->{self.to_pid}"

