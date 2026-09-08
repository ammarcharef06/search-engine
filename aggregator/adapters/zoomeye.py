import requests
import os
from typing import List, Dict, Any

class ZoomEyeAdapter:
    def __init__(self):
        self.api_key = os.getenv("ZOOMEYE_KEY")
        self.base_url = "https://api.zoomeye.org"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            headers = {"API-KEY": self.api_key}
            params = {"query": query, "page": 1, "size": limit}
            response = requests.get(f"{self.base_url}/host/search", headers=headers, params=params)
            data = response.json()
            matches = data.get("matches", [])
            return [{
                "source": "ZoomEye",
                "ip": m.get("ip", {}).get("ip", "N/A"),
                "port": m.get("portinfo", {}).get("port"),
                "banner": m.get("portinfo", {}).get("banner", "")[:300],
                "cve": [],
                "link": f"https://zoomeye.org/result/{m.get('ip', {}).get('ip', '')}"
            } for m in matches]
        except Exception as e:
            return [{"source": "ZoomEye", "error": str(e)}]