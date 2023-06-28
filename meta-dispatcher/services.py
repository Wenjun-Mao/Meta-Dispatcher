# services.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import httpx


TIMEOUT_LIMIT = 300

class Service(ABC):
    @abstractmethod
    async def send_request(self, data: Any) -> httpx.Response:
        pass

class FaceService(Service):
    def __init__(self):
        self.url = "http://localhost:8001"

    async def send_request(self, data: Dict[str, Any]) -> httpx.Response:
        async with httpx.AsyncClient(timeout=TIMEOUT_LIMIT) as client:
            response = await client.post(self.url, data=data)
        return response

class ManhuaService(Service):
    def __init__(self):
        self.url = "http://localhost:5000/sdapi/v1/img2img"

    async def send_request(self, data: Dict[str, Any]) -> httpx.Response:
        async with httpx.AsyncClient(timeout=TIMEOUT_LIMIT) as client:
            response = await client.post(self.url, json=data)
        return response
