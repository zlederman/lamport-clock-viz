from typing import List
from pydantic import BaseModel


class CreateSystemResponse(BaseModel):
    node_ids: List[str]