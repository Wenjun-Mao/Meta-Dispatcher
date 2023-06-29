# test/unit/test_app.py

from unittest.mock import patch
import pytest
import httpx
from fastapi.testclient import TestClient
from meta_dispatcher.app import app

@pytest.fixture
def client():
    return TestClient(app)

@patch('services.FaceService.send_request')
def test_form_data_request(mock_send_request):
    # Given: Setup the conditions for the test.
    # Mock the response from the FaceService.
    mock_response = httpx.Response(200, json={"message": "Success"})
    mock_send_request.return_value = mock_response

    form_data = {
        "content_type": "type1",
        "content_name": "name1",
        "face_restore": 1,
        "file": "file1",
        "url": "http://test.com"
    }

    # When: Perform the action that we're testing.
    response = client.post("/", data=form_data)

    # Then: Make assertions about the result.
    assert response.status_code == 200
    assert response.json() == {"message": "Success"}
