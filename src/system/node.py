import multiprocessing as mp
import random
import time
from typing import Dict, List
from src.common.models import SystemEvent, SendEvent, RecvEvent, InternalEvent, EventType
from loguru import logger

from src.system.clock import LamportClock

class Node(mp.Process):

    def __init__(self, node_id: str, max_messages: int, queue_map: Dict[str, "mp.Queue[SendEvent]"], log_queue: mp.Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_id = node_id
        self.max_messages = max_messages
        self.sent_messages = 0
        self.queue_map = queue_map
        self.log_queue = log_queue
        self.clock = LamportClock()

    def event_generator(self) -> EventType:
        if not self.queue_map[self.node_id].empty():
            return "RECV"
        else:
            return random.choice(["INTERNAL", "SEND"])
    
    def handle_internal_event(self) -> InternalEvent:
        return InternalEvent(clock=self.clock.model_copy(), node_id=self.node_id)


    def _choose_node_id(self):
        idx_choice = random.randrange(0, len(self.queue_map))
        node_ids = list(self.queue_map.keys())
        if node_ids[idx_choice] == self.node_id:
            return node_ids[(idx_choice + 1) % len(self.queue_map)]
        return node_ids[idx_choice]
    
    def handle_send_event(self) -> SendEvent:
        send_event = SendEvent(clock=self.clock.model_copy(), node_id=self.node_id, msg_to=self._choose_node_id())
        self.queue_map[send_event.msg_to].put(send_event)
        self.sent_messages += 1
        return send_event

    def handle_recv_event(self) -> RecvEvent | None:
        if self.queue_map[self.node_id].empty():
            return None
        
        message = self.queue_map[self.node_id].get()
        self.clock.update_from_msg(message.clock)
        recv_event = RecvEvent(clock=self.clock.model_copy(), msg_from=message.node_id, node_id=self.node_id)
        return recv_event

    def run(self):
        delay = lambda: (random.randrange(5,10) / 10)
        while self.sent_messages < self.max_messages:
            next_event_type = self.event_generator()
            event: SystemEvent | None = None
            match next_event_type:
                case "INTERNAL":
                    event = self.handle_internal_event()
                case "SEND":
                    event = self.handle_send_event()
                case "RECV":
                    event = self.handle_recv_event()
            self.log_queue.put(event.model_dump_json())
            if event is not None:
                self.clock += 1
                time.sleep(delay())
                
        event = self.handle_recv_event()
        if event is not None:
            self.log_queue.put(event.model_dump_json())
            self.clock += 1
            time.sleep(delay())