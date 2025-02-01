import logging
from queue import SimpleQueue
import random
import threading
import time
from .process import Process

class SnapshotManager(threading.Thread):

    def __init__(self, outgoing_queue: SimpleQueue):
        super().__init__(name="snapshot_manager", daemon=True)
        self.outgoing_queues: dict[int, SimpleQueue] = dict()
        self.gathering_queue = SimpleQueue()
        self.outgoing_queue = outgoing_queue

        self.amount_snapshots_initiated = 1
        self.snapshots: dict[str, dict] = {}
        self.snapshot_in_progress = False
    
    def connect_to_process(self, process: Process):
        self.outgoing_queues[process.pid] = SimpleQueue()
        process.connect_snapshot_manager(self.gathering_queue, self.outgoing_queues[process.pid])

    def initiate_snapshot(self, pid: int):
        logging.error(f"Snapshot nr_{self.amount_snapshots_initiated}_start{pid} started")
        self.outgoing_queues[pid].put(f"nr_{self.amount_snapshots_initiated}_start={pid}")
        self.snapshot_in_progress = True
        self.amount_snapshots_initiated += 1

    def add_to_snapshot(self, snapshot_message: dict):
        marker_id: str = snapshot_message['marker_id']
        state = snapshot_message['state']
        if self.snapshots.get(marker_id) is None:
            self.snapshots[marker_id] = {"processes": {}, "channels": {}}
        self.snapshots[marker_id]['processes'].update(state['processes'])
        self.snapshots[marker_id]['channels'].update(state['channels'])

        if len(self.snapshots[marker_id]['processes']) == len(self.outgoing_queues):
            logging.error(f"Snapshot {marker_id} completed.")
            self.snapshot_in_progress = False
            self.snapshots[marker_id]['marker_id'] = marker_id
            self.outgoing_queue.put(self.snapshots[marker_id])

    def run(self):
        time_since_last_snapshot_started = time.time()
        while True:
            if not self.gathering_queue.empty():
                snapshot_message = self.gathering_queue.get_nowait()
                logging.info(f"Snapshot Manager received {snapshot_message}")
                self.add_to_snapshot(snapshot_message)

            if time.time() - time_since_last_snapshot_started > 0.5 and not self.snapshot_in_progress:
                self.initiate_snapshot(random.choice(list(self.outgoing_queues.keys())))
                time_since_last_snapshot_started = time.time()

            time.sleep(0.01)