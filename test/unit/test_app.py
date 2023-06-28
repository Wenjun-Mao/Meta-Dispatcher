# test/unit/test_app.py

from unittest.mock import patch
import httpx
from fastapi.testclient import TestClient
from meta_dispatcher.app import app

client = TestClient(app)

