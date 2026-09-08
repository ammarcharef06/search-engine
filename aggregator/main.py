import asyncio
import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

# استيراد المحولات
from adapters.shodan import ShodanAdapter
# from adapters.censys import CensysAdapter  # علق مؤقتاً
from adapters.zoomeye import ZoomEyeAdapter
from adapters.fofa import FofaAdapter
from adapters.binaryedge import BinaryEdgeAdapter
from adapters.leakix import LeakIXAdapter
from adapters.dehashed import DehashedAdapter
from adapters.hudsonrock import HudsonRockAdapter
from adapters.grayhat import GrayhatAdapter
from adapters.netcraft import NetcraftAdapter
from adapters.intelx import IntelXAdapter

from cache import get_cache, set_cache
from formatter import format_results

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

# قائمة المحولات النشطة
adapters = [
    ShodanAdapter(),
    # CensysAdapter(),  # علق مؤقتاً
    ZoomEyeAdapter(),
    FofaAdapter(),
    BinaryEdgeAdapter(),
    LeakIXAdapter(),
    DehashedAdapter(),
    HudsonRockAdapter(),
    GrayhatAdapter(),
    NetcraftAdapter(),
    IntelXAdapter(),
]

@app.post("/search")
async def search(req: SearchRequest):
    # التحقق من الكاش
    cached = await get_cache(req.query)
    if cached:
        return json.loads(cached)
    
    # تنفيذ البحث على المحولات النشطة
    tasks = [adapter.search(req.query) for adapter in adapters]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # دمج النتائج
    merged = []
    for i, res in enumerate(results):
        if isinstance(res, Exception):
            merged.append({
                "source": adapters[i].__class__.__name__,
                "error": str(res)
            })
        else:
            merged.extend(res)
    
    formatted = format_results(merged)
    await set_cache(req.query, json.dumps(formatted))
    return formatted

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8082))
    uvicorn.run(app, host="0.0.0.0", port=port)
