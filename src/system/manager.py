import asyncio
import random
from typing import AsyncGenerator, Dict, List
import multiprocessing as mp

from loguru import logger
from src.system.node import Node
from src.common.models import SystemEvent


class NodeManager:
    def __init__(self) -> None:
        self.nodes: List[Node] = []
        self.log_queue: "mp.Queue[str]" = mp.Queue()
        self.queue_map: Dict[str, mp.Queue] = {}
        
    def generate_id(self, length:int = 4) -> str:
        chars = 'abcdefghijkmnpqrstuvwxyz23456789'
        return ''.join(random.choice(chars) for _ in range(length))
    
    def setup_nodes(self, num_nodes: int, max_messages: int) -> List[str]:
        # Create queues for each node
        node_ids = []
        for i in range(num_nodes):
            node_id = self.generate_id()
            node_ids.append(node_id)
            self.queue_map[node_id] = mp.Queue()
        
        # Create and start nodes
        for i in range(num_nodes):
            node_id = node_ids[i]
            node = Node(
                node_id=node_id,
                max_messages=max_messages,
                queue_map=self.queue_map,
                log_queue=self.log_queue
            )
            self.nodes.append(node)
        return [node.node_id for node in self.nodes]
    
    
    def start_nodes(self):
        for node in self.nodes:
            node.start()

    def cleanup(self):
        for node in self.nodes:
            if node.is_alive():
                node.join(timeout=1)
                if node.is_alive():
                    node.terminate()
        self.nodes = []

        for queue in self.queue_map.values():
            while not queue.empty():
                try:
                    queue.get_nowait()
                except:
                    pass
        self.queue_map = {}
        # drain queue
        while not self.log_queue.empty():
            try:
                self.log_queue.get_nowait()
            except:
                pass

    
    async def get_logs(self) -> AsyncGenerator[str]:
        while any(node.is_alive() for node in self.nodes):
            try:
                if not self.log_queue.empty():
                    log = self.log_queue.get_nowait()

                    yield f"data: {log}\n\n"
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in get_logs: {e}")
                await asyncio.sleep(0.1)
                continue