from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import httpx
import asyncio
import uuid
import redis.asyncio as aioredis
from urllib.parse import urlparse

app = FastAPI()

class Task(BaseModel):
    id: str
    status: str
    result: List[Dict[str, str]] = []

tasks = {}
redis = None

@app.on_event("startup")
async def startup_event():
    global redis
    redis = await aioredis.from_url("redis://localhost")
    asyncio.create_task(cleanup_cache(300))

@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()

@app.post("/api/v1/tasks/", response_model=Task, status_code=201)
async def create_task(urls: List[str]):
    task_id = str(uuid.uuid4())
    tasks[task_id] = Task(id=task_id, status="running")
    asyncio.create_task(process_urls(task_id, urls))
    return tasks[task_id]

async def process_urls(task_id: str, urls: List[str]):
    async with httpx.AsyncClient() as client:
        results = []
        for url in urls:
            domain = urlparse(url).netloc
            cached_code = await redis.get(url)

            if cached_code:
                results.append({"url": url, "status_code": cached_code.decode('utf-8')})
                await redis.incr(f"domain_count:{domain}")
            else:
                try:
                    response = await client.get(url)
                    status_code = str(response.status_code)
                    results.append({"url": url, "status_code": status_code})
                    await redis.set(url, status_code, ex=60)
                    await redis.incr(f"domain_count:{domain}")
                except httpx.RequestError:
                    results.append({"url": url, "status_code": "RequestError"})
        
        tasks[task_id].status = "ready"
        tasks[task_id].result = results

@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

async def cleanup_cache(timeout: int):
    while True:
        await asyncio.sleep(timeout)

@app.get("/api/v1/domain_count/{domain}", response_model=Dict[str, int])
async def get_domain_count(domain: str):
    count = await redis.get(f"domain_count:{domain}")
    return {domain: int(count) if count else 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
