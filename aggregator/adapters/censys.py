import os
from typing import List, Dict, Any

class CensysAdapter:
    def __init__(self):
        self.api_id = os.getenv("CENSYS_ID", "")
        self.api_secret = os.getenv("CENSYS_SECRET", "")
        self.enabled = bool(self.api_id and self.api_secret)
        
        if self.enabled:
            from censys.search import SearchClient
            self.client = SearchClient(self.api_id, self.api_secret)

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        if not self.enabled:
            return [{"source": "Censys", "error": "Censys API keys not configured"}]
        
        try:
            results = self.client.v2.hosts.search(query, limit=limit)
            return [{
                "source": "Censys",
                "ip": r["ip"],
                "port": r.get("services", [{}])[0].get("port"),
                "banner": str(r.get("services", [{}])[0].get("banner", ""))[:300],
                "cve": [],
                "link": f"https://censys.io/ip/{r['ip']}"
            } for r in results]
        except Exception as e:
            return [{"source": "Censys", "error": str(e)}]