import requests
import os
from typing import List, Dict, Any

class LeakIXAdapter:
    def __init__(self):
        self.base_url = "https://leakix.net/api/v1"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            params = {"q": query, "limit": limit}
            response = requests.get(f"{self.base_url}/search", params=params)
            data = response.json()
            results = data.get("results", [])
            return [{
                "source": "LeakIX",
                "ip": r.get("ip", "N/A"),
                "port": r.get("port"),
                "banner": r.get("banner", "")[:300],
                "cve": r.get("cves", []),
                "link": f"https://leakix.net/host/{r.get('ip', '')}"
            } for r in results]
        except Exception as e:
            return [{"source": "LeakIX", "error": str(e)}]