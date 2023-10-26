import asyncio
import datetime

from typing import List, Dict
from fastapi import WebSocket
from config import check_openai_api_key
from agent.research_agent import ResearchAgent


class FilesCacheManager:

    def __init__(self) -> None:
        self.files_uploaded: Dict[str, list[str]] = {}

    async def add_files(self, fid: str, file_list: list[str]):
        self.files_uploaded[fid] = file_list
    
    async def get_files(self, fid: str):
        if fid in self.files_uploaded:
            return self.files_uploaded[fid]
        return []

    async def del_files(self, fid: str):
        if fid in self.files_uploaded:
            del self.files_uploaded[fid]


class WebSocketManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.sender_tasks: Dict[WebSocket, asyncio.Task] = {}
        self.message_queues: Dict[WebSocket, asyncio.Queue] = {}

    async def start_sender(self, websocket: WebSocket):
        queue = self.message_queues[websocket]
        while True:
            message = await queue.get()
            if websocket in self.active_connections:
                await websocket.send_text(message)
            else:
                break

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.message_queues[websocket] = asyncio.Queue()
        self.sender_tasks[websocket] = asyncio.create_task(self.start_sender(websocket))

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.sender_tasks[websocket].cancel()
        del self.sender_tasks[websocket]
        del self.message_queues[websocket]

    async def start_streaming(self, task, report_type, agent, agent_role_prompt, file_list, websocket):
        report, path = await run_agent(task, report_type, agent, agent_role_prompt, file_list, websocket)
        return report, path


async def run_agent(task, report_type, agent, agent_role_prompt, file_list, websocket):
    check_openai_api_key()

    start_time = datetime.datetime.now()

    # await websocket.send_json({"type": "logs", "output": f"Start time: {str(start_time)}\n\n"})

    assistant = ResearchAgent(task, agent, agent_role_prompt, websocket, file_list=file_list)
    await assistant.conduct_research()

    report, path = await assistant.write_report(report_type, websocket)

    await websocket.send_json({"type": "path", "output": path})

    end_time = datetime.datetime.now()
    await websocket.send_json({"type": "logs", "output": f"\nEnd time: {end_time}\n"})
    await websocket.send_json({"type": "logs", "output": f"\nTotal run time: {end_time - start_time}\n"})

    return report, path
