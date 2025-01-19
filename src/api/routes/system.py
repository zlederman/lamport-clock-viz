from typing import Annotated, AsyncIterator, Generic, Iterator, TypeAlias, TypeVar
from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.api.depend import get_manager
from src.api.models import CreateSystemResponse

from src.common.models import InternalEvent, RecvEvent, SendEvent, SystemParams, SystemEvent
from multiprocessing import Queue
from loguru import logger

from src.system.manager import NodeManager


system_router = APIRouter()

StreamedSystemEvents: TypeAlias = Annotated[StreamingResponse, SystemEvent]



@system_router.post('/create')
async def create_system(system_params: SystemParams, manager: NodeManager = Depends(get_manager)):
    manager.cleanup()
    node_ids = manager.setup_nodes(system_params.num_nodes, system_params.max_messages)
    return CreateSystemResponse(node_ids=node_ids)

@system_router.get("/start", responses={
        200: {
            "description": "Stream of log messages",
            "content": {
                "text/event-stream": {
                    "schema": {
                        "type": "array",
                        "items": {
                    "anyOf": [
                        SendEvent.model_json_schema(),
                        RecvEvent.model_json_schema(),
                        InternalEvent.model_json_schema()
                    ],
                    "discriminator": {
                        "propertyName": "event_type",
                        "mapping": {
                            "SEND": "#/items/anyOf/0",
                            "RECV": "#/items/anyOf/1",
                            "INTERNAL": "#/items/anyOf/2"
                        }
                    }
                }
                    }
                }
            }
        }
    })
async def stream_logs(manager: NodeManager = Depends(get_manager)):
    manager.start_nodes()
    return StreamingResponse(
        manager.get_logs(),
        media_type="text/event-stream"
    )
        
@system_router.get("/cleanup")
async def cleanup_system(manager: NodeManager = Depends(get_manager)):
    manager.cleanup()