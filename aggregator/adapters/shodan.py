import shodan
import os
from typing import List, Dict, Any

class ShodanAdapter:
    def __init__(self):
        self.api_key = os.getenv("SHODAN_KEY")
        self.client = shodan.Shodan(self.api_key)

    async def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        try:
            results = self.client.search(query, limit=limit)
            return [{
                "source": "Shodan",
                "ip": r["ip_str"],
                "port": r["port"],
                "banner": r["data"][:300],
                "cve": list(r.get("vulns", {}).keys()),
                "link": f"https://www.shodan.io/host/{r['ip_str']}"
            } for r in results["matches"]]
        except Exception as e:
            return [{"source": "Shodan", "error": str(e)}]