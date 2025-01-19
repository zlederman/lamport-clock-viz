from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

EventType = Literal["SEND", "RECV", "INTERNAL"]

class SystemParams(BaseModel):
    num_nodes: int
    max_messages: int

class BaseEvent(BaseModel):
    node_id: str
    timestamp: int

class SendEvent(BaseEvent):
    event_type: EventType = "SEND"
    msg_to: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "node_id": "node1",
                "timestamp": 1234567890,
                "event_type": "SEND",
                "msg_to": "node2"
            }
        }

class RecvEvent(BaseEvent):
    event_type: EventType = "RECV"
    msg_from: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "node_id": "node2",
                "timestamp": 1234567891,
                "event_type": "RECV",
                "msg_from": "node1"
            }
        }

class InternalEvent(BaseEvent):
    event_type: EventType = "INTERNAL"
    
    class Config:
        json_schema_extra = {
            "example": {
                "node_id": "node1",
                "timestamp": 1234567892,
                "event_type": "INTERNAL"
            }
        }
SystemEvent = Annotated[
    Union[SendEvent, RecvEvent, InternalEvent],
    Field(discriminator='event_type')
]