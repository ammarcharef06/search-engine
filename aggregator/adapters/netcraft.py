import requests
import os
from typing import List, Dict, Any

class NetcraftAdapter:
    def __init__(self):
        self.api_key = os.getenv("NETCRAFT_KEY")
        self.base_url = "https://api.netcraft.com/v1"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            params = {"search": query, "limit": limit}
            response = requests.get(f"{self.base_url}/hosts", headers=headers, params=params)
            data = response.json()
            hosts = data.get("hosts", [])
            return [{
                "source": "Netcraft",
                "ip": h.get("ip", "N/A"),
                "port": None,
                "banner": f"Domain: {h.get('domain', '')} - Server: {h.get('server', '')}",
                "cve": [],
                "link": f"https://sitereport.netcraft.com/?url={h.get('domain', '')}"
            } for h in hosts]
        except Exception as e:
            return [{"source": "Netcraft", "error": str(e)}]