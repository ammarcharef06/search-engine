import requests
import os
from typing import List, Dict, Any

class FofaAdapter:
    def __init__(self):
        self.api_key = os.getenv("FOFA_KEY")
        self.email = os.getenv("FOFA_EMAIL")
        self.base_url = "https://fofa.info/api/v1/search/all"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            params = {
                "key": self.api_key,
                "email": self.email,
                "qbase64": query,
                "size": limit
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            results = data.get("results", [])
            return [{
                "source": "FOFA",
                "ip": r[0],
                "port": r[1],
                "banner": r[2][:300],
                "cve": [],
                "link": f"https://fofa.info/ip/{r[0]}"
            } for r in results]
        except Exception as e:
            return [{"source": "FOFA", "error": str(e)}]