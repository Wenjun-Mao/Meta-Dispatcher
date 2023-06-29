# src/meta-dispatcher/main.py
import asyncio
from typing import Dict, Any, Optional

from fastapi import FastAPI, Depends, HTTPException, Request, UploadFile
from pydantic import BaseModel, ValidationError
import httpx

from .services import FaceService, ManhuaService

app = FastAPI()
lock = asyncio.Lock()

class FaceData(BaseModel):
    content_type: str
    content_name: str
    face_restore: Optional[int]
    file: Optional[UploadFile]
    url: Optional[str]

class ManhuaData(BaseModel):
    data: Dict[str, Any]

def determine_service(data: Dict[str, Any]):
    try:
        face_data = FaceData(**data)
        return FaceService()
    except ValidationError:
        pass

    try:
        manhua_data = ManhuaData(**data)
        return ManhuaService()
    except ValidationError:
        pass

    raise HTTPException(status_code=400, detail="Invalid request format.")

@app.post("/")
async def api_endpoint(request: Request):
    async with lock:
        try:
            form_data = await request.form()
            service = determine_service(form_data)
            data = form_data
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse form-data.")

        if not service:
            try:
                json_data = await request.json()
                service = determine_service(json_data)
                data = json_data
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=400, detail="Failed to parse JSON data.")

        try:
            response = await service.send_request(data)
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Internal service returned an error.")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Unexpected error occurred.")
