import requests
import os
from typing import List, Dict, Any

class HudsonRockAdapter:
    def __init__(self):
        self.api_key = os.getenv("HUDSONROCK_KEY")
        self.base_url = "https://cavalier.hudsonrock.com/api/v1/search"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            params = {"query": query, "limit": limit}
            response = requests.get(self.base_url, headers=headers, params=params)
            data = response.json()
            results = data.get("results", [])
            return [{
                "source": "Hudson Rock",
                "ip": r.get("ip", "N/A"),
                "port": None,
                "banner": f"Username: {r.get('username', '')} - Domain: {r.get('domain', '')}",
                "cve": [],
                "link": "#"
            } for r in results]
        except Exception as e:
            return [{"source": "Hudson Rock", "error": str(e)}]