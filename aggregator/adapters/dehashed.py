import requests
import os
from typing import List, Dict, Any

class DehashedAdapter:
    def __init__(self):
        self.email = os.getenv("DEHASHED_EMAIL")
        self.api_key = os.getenv("DEHASHED_KEY")
        self.base_url = "https://api.dehashed.com/search"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            auth = (self.email, self.api_key)
            params = {"query": query, "size": limit}
            response = requests.get(self.base_url, auth=auth, params=params)
            data = response.json()
            entries = data.get("entries", [])
            return [{
                "source": "DeHashed",
                "ip": e.get("ip_address", "N/A"),
                "port": None,
                "banner": f"Email: {e.get('email', '')} - Password: {e.get('password', '')}",
                "cve": [],
                "link": "#"
            } for e in entries]
        except Exception as e:
            return [{"source": "DeHashed", "error": str(e)}]