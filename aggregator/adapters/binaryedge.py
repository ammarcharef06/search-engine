import requests
import os
from typing import List, Dict, Any

class BinaryEdgeAdapter:
    def __init__(self):
        self.api_key = os.getenv("BINARYEDGE_KEY")
        self.base_url = "https://api.binaryedge.io/v2"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            headers = {"X-Key": self.api_key}
            params = {"query": query, "limit": limit}
            response = requests.get(f"{self.base_url}/query/search", headers=headers, params=params)
            data = response.json()
            events = data.get("events", [])
            return [{
                "source": "BinaryEdge",
                "ip": e.get("ip", "N/A"),
                "port": e.get("port", {}).get("port"),
                "banner": e.get("port", {}).get("banner", "")[:300],
                "cve": [],
                "link": f"https://app.binaryedge.io/result/{e.get('id', '')}"
            } for e in events]
        except Exception as e:
            return [{"source": "BinaryEdge", "error": str(e)}]