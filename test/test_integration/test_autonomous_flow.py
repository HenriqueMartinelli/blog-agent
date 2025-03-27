import pytest

@pytest.mark.asyncio
async def test_create_autonomous_post_flow(test_client):
    async with test_client as client:
        response = await client.post("/posts/autonomous")
        assert response.status_code == 201
        data = response.json()
        assert "titulo" in data
        assert "conteudo" in data

