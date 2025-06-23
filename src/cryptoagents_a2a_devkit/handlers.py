from typing import TypedDict, Optional
import httpx
import os

class AgentDetail(TypedDict):
    agent_id: str
    description: str
    agent_name: str
    base_url: str # something like http://api.openai.com/v1/chat/completions

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
AUTHORIZATION_TOKEN = os.getenv("AUTHORIZATION_TOKEN", "super-secret") 

async def get_agent_detail(agent_id: str) -> Optional[AgentDetail]:
    """
    Get the details of an agent
    """
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BACKEND_BASE_URL}/vibe-agent/{agent_id}",
                headers={"Authorization": f"Bearer {AUTHORIZATION_TOKEN}"}
            )
        except httpx.HTTPStatusError:
            return None

        if response.status_code == 200:
            data = response.json()

            container = data["container_name"] or data["container_id"]
            port = data["port"] or 80

            return AgentDetail(
                agent_id=agent_id,
                description=data["description"],
                agent_name=data["name"],
                base_url=f"http://{container}:{port}/prompt"
            )

        return None
