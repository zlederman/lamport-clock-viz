from pydantic import BaseModel

from typing import Any


class LamportClock(BaseModel):
    timestamp: int = 0

    def __add__(self, other: int):
        self.timestamp += other
        return self

    def update_from_msg(self, clock: 'LamportClock'):
        self.timestamp = max(self.timestamp, clock.timestamp + 1) 

