from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import httpx
import asyncio
import uuid

app = FastAPI()

class Task(BaseModel):
    id: str
    status: str
    result: List[Dict[str, str]] = []

tasks = {}

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
            try:
                response = await client.get(url)
                results.append({"url": url, "status_code": str(response.status_code)})
            except httpx.RequestError:
                results.append({"url": url, "status_code": "RequestError"})
        tasks[task_id].status = "ready"
        tasks[task_id].result = results

@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
