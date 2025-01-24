from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field, model_serializer

from src.system.clock import LamportClock

EventType = Literal["SEND", "RECV", "INTERNAL"]

class SystemParams(BaseModel):
    num_nodes: int
    max_messages: int

class BaseEvent(BaseModel):
    node_id: str
    clock: LamportClock

    @model_serializer
    def serialize_model(self):
        return {
            "node_id": self.node_id,
            "timestamp": self.clock.timestamp
        }

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
    @model_serializer
    def serialize_model(self):
        return {
            **super().serialize_model(),
            "msg_to": self.msg_to,
            "event_type": self.event_type
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
    @model_serializer
    def serialize_model(self):
        return {
            **super().serialize_model(),
            "msg_from": self.msg_from,
            "event_type": self.event_type
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
    @model_serializer
    def serialize_model(self):
        return {
            **super().serialize_model(),
            "event_type": self.event_type
        }
SystemEvent = Annotated[
    Union[SendEvent, RecvEvent, InternalEvent],
    Field(discriminator='event_type')
]