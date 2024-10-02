import httpx
import asyncio
import sys
import json

async def submit_urls(urls):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8888/api/v1/tasks/", json=urls)
        return response.json()

async def get_task_status(task_id):
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get(f"http://localhost:8888/api/v1/tasks/{task_id}")
            task = response.json()
            if task['status'] == 'ready':
                return task
            await asyncio.sleep(1)

async def main(urls):
    task = await submit_urls(urls)
    task_id = task['id']
    print(f"Task ID: {task_id}")
    
    completed_task = await get_task_status(task_id)
    for result in completed_task['result']:
        print(f"{result['status_code']}\t{result['url']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crawl.py <url1> <url2> ...")
        sys.exit(1)

    urls = sys.argv[1:]
    asyncio.run(main(urls))
