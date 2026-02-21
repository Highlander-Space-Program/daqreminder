import httpx
from dataclasses import dataclass


@dataclass
class Webhook:
    webhook_url: str
    name: str
    pfp_url: str

    async def send_message(self, message: str):
        payload = {
            "username": self.name,
            "avatar_url": self.pfp_url,
            "content": message,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.webhook_url, json=payload)
            if response.status_code != 204:
                print(
                    f"Failed to send message: {response.status_code} - {response.text}"
                )
