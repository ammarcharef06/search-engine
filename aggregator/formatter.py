from datetime import datetime
from typing import List, Dict, Any

def format_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """تنسيق النتائج لإظهارها بشكل منظم"""
    formatted = []
    for item in results:
        formatted.append({
            "source": item.get("source", "Unknown"),
            "ip": item.get("ip", "N/A"),
            "port": item.get("port", "N/A"),
            "banner": item.get("banner", "")[:300],
            "cve": item.get("cve", []),
            "timestamp": datetime.now().isoformat(),
            "link": item.get("link", "#")
        })
    return sorted(formatted, key=lambda x: x["source"])