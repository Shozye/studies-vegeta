from dataclasses import dataclass
import logging
from queue import SimpleQueue
import random
import threading
import time
from .channel import Channel
from .message import *



class Process(threading.Thread):
    def __init__(self, pid: int, amount_resources: int) -> None:
        super().__init__(name=str(pid), daemon=True)
        self.pid: int = pid
        self._outgoing_channels: dict[int, Channel] = dict()
        self._incoming_channels: dict[int, Channel] = dict()
        self._incoming_snapshot_messager: SimpleQueue[str]

        self._recorded_state = dict()
        self._during_recording: dict[str, int] = dict()
        self._state: dict[str, dict] = dict()
        self._state_gatherer: SimpleQueue 

        self._amount_resources = amount_resources
        self._send_resources: bool = True
    
    def set_should_not_send_resources(self):
        self._send_resources=False

    @staticmethod
    def connect(sender: "Process", receiver: "Process") -> None:
        channel = Channel(sender.pid, receiver.pid)
        sender._outgoing_channels[channel.to_pid] = channel
        receiver._incoming_channels[channel.from_pid] = channel
    
    def connect_snapshot_manager(self, gatherer: SimpleQueue, incoming_snapshot_messager: SimpleQueue):
        self._state_gatherer = gatherer
        self._incoming_snapshot_messager = incoming_snapshot_messager

    def run(self):
        while True:
            if not self._incoming_snapshot_messager.empty():
                self.initiate_snapshot(self._incoming_snapshot_messager.get_nowait())

            if random.random() >= 1/(len(self._outgoing_channels)+1): # to have not changing resource
                if self._amount_resources > 0 and self._send_resources:
                    random_pick = random.choice(list(self._outgoing_channels.keys()))
                    self._outgoing_channels[random_pick].send(SendResourceMessage(amount_resource=1))
                    self._amount_resources -= 1
                    # logging.debug(f"P{self.pid}|Decreased amount resources {self._amount_resources}")
            else:
                for other_pid, channel in self._incoming_channels.items():
                    msg = channel.receive()
                    if msg is not None:
                        self.handle_received_message(other_pid,msg)
            time.sleep(0.01)

    def handle_received_message(self, from_pid: int, msg: Message):
        if msg.type == MESSAGE_TYPE.SEND_RESOURCE:
            self.handle_send_resource_message(msg) # type: ignore
        elif msg.type == MESSAGE_TYPE.MARKER:
            self.handle_marker_message(from_pid, msg) # type: ignore
        else:
            raise Exception("wrong message my friend")

    def handle_send_resource_message(self, msg: SendResourceMessage):
        self._amount_resources += msg.amount_resource
        # logging.debug(f"P{self.pid}|Increased amount resources {self._amount_resources}")

    def handle_marker_message(self, from_pid: int, msg: MarkerMessage):
        inc_channel = self._incoming_channels[from_pid]
        logging.info(f"{self.pid} Received marker message from {from_pid}")
        # https://github.com/ChrisWhealy/DistributedSystemNotes/blob/master/Lecture%2008.md
        # When a process receives a marker message, it can react in one of two different ways. 
        # Scenario 1: Nope, I Haven't Seen a Marker Message Before...
        if self._during_recording.get(msg.marker_id) is None:
            self._during_recording[msg.marker_id] = 0
            # Records its own state (?)
            self._state[msg.marker_id] = dict()
            self._state[msg.marker_id]["processes"] = {str(self.pid): {"resources":self._amount_resources}}
            # Flags the channel on which the marker message was received as empty
            self._state[msg.marker_id]['channels'] = {str(inc_channel): {}}
            self._increase_recorded_messages_for_marker(msg.marker_id)
            # Sends out a marker message on each of its outgoing channels
            for channel in self._outgoing_channels.values(): # something like this?
                channel.send(msg)
            # Starts recording incoming messages on all channels except the one on which it received the original marker message (now flagged as empty)
            for other_pid, channel in self._incoming_channels.items():
                if other_pid != from_pid:
                    channel.start_recording()


        # Scenario 2: Yup, I've Already Seen a Marker Message...
        else:
            logging.info(f"{self.pid} I received marker message that I already received.")
            # So when a process that has already sent out its own marker message receives someone else's marker message
            # 1. Stops recording incoming messages on that channel
            recorded_messages = inc_channel.stop_recording()
            # 2. Sets that channel's final state to be the sequence of all messages received whilst recording was active
            # print(len(recorded_messages))
            self._state[msg.marker_id]['channels'][str(inc_channel)] = recorded_messages
            self._increase_recorded_messages_for_marker(msg.marker_id)
    
    def _increase_recorded_messages_for_marker(self, marker_id: str):
        self._during_recording[marker_id] += 1
        if self._during_recording[marker_id] == len(self._incoming_channels):
            # I want an exception if it is empty which is what i get here.
            snapshot_message = {"marker_id": marker_id, "state": self._state[marker_id]}
            logging.info(f"{self.pid} Sending snapshot {snapshot_message}")
            self._state_gatherer.put(snapshot_message) # type: ignore
            # del self._during_recording[marker_id]
            # del self._state[marker_id]


    def initiate_snapshot(self, marker_id: str):
        logging.info(f"{self.pid}|Received Initiate Snapshot message {marker_id=}, Currently resources={self._amount_resources}")
        if self._during_recording.get(marker_id) is not None:
            return None # i cannot initiate a snapshot with a marker id the same as the one that is ongoing.
        self._during_recording[marker_id] = 0
        # https://github.com/ChrisWhealy/DistributedSystemNotes/blob/master/Lecture%2008.md
        # 1. Records its own state (?)
        self._state[marker_id] = dict()
        self._state[marker_id]["processes"] = {str(self.pid): {"resources":self._amount_resources}}
        self._state[marker_id]['channels'] = dict()
        # 2. Sends a Marker Message out on all its ougoing channels
        for channel in self._outgoing_channels.values(): # something like this?
            channel.send(MarkerMessage(marker_id=marker_id))
        # 3. Starts recording messages arriving on all incoming channels
        for channel in self._incoming_channels.values():
            channel.start_recording()
        