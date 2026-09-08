import requests
import os
from typing import List, Dict, Any

class IntelXAdapter:
    def __init__(self):
        self.api_key = os.getenv("INTELX_KEY")
        self.base_url = "https://2.intelx.io"

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            headers = {"x-api-key": self.api_key}
            payload = {"term": query, "maxresults": limit}
            response = requests.post(f"{self.base_url}/search", headers=headers, json=payload)
            data = response.json()
            results = data.get("records", [])
            return [{
                "source": "IntelX",
                "ip": r.get("ip", "N/A"),
                "port": None,
                "banner": f"Domain: {r.get('domain', '')} - Date: {r.get('date', '')}",
                "cve": [],
                "link": f"https://intelx.io/record/{r.get('id', '')}"
            } for r in results]
        except Exception as e:
            return [{"source": "IntelX", "error": str(e)}]