import requests
import os
from typing import List, Dict, Any

class GrayhatAdapter:
    def __init__(self):
        self.base_url = "https://grayhatwarfare.com/api/v1"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            params = {"q": query, "limit": limit}
            response = requests.get(f"{self.base_url}/buckets/search", params=params)
            data = response.json()
            buckets = data.get("buckets", [])
            return [{
                "source": "Grayhat Warfare",
                "ip": "N/A",
                "port": None,
                "banner": f"Bucket: {b.get('name', '')} - File: {b.get('file', '')} - Size: {b.get('size', '')}",
                "cve": [],
                "link": f"https://grayhatwarfare.com/bucket/{b.get('name', '')}"
            } for b in buckets]
        except Exception as e:
            return [{"source": "Grayhat Warfare", "error": str(e)}]