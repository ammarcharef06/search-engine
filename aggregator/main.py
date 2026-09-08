import asyncio
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from adapters import *
from cache import get_cache, set_cache

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    token: str  # مفتاح الجلسة المؤقت

adapters = [
    ShodanAdapter(),
    CensysAdapter(),
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
    cached = await get_cache(req.query)
    if cached:
        return json.loads(cached)

    tasks = [adapter.search(req.query) for adapter in adapters]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    merged = []
    for i, res in enumerate(results):
        if isinstance(res, Exception):
            merged.append({"source": adapters[i].__class__.__name__, "error": str(res)})
        else:
            merged.extend(res)

    await set_cache(req.query, json.dumps(merged))
    return merged