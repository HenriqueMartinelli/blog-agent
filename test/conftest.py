import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest_asyncio
from httpx import AsyncClient
from app import app 
from httpx import AsyncClient

@pytest_asyncio.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
