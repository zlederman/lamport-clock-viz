from functools import lru_cache
from fastapi import Depends

from src.system.manager import NodeManager


@lru_cache
def get_manager() -> NodeManager:
    """Singleton manager instance"""
    return NodeManager()