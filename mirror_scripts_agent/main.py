from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile
from pydantic import BaseModel
import json
import os
import asyncio
import traceback

from agent.llm_utils import choose_agent
from agent.run import WebSocketManager


class ResearchRequest(BaseModel):
    task: str
    report_type: str
    agent: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Change to domains if you deploy this to production
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload multiple local resources to the server
@app.post("/upload")
async def create_upload_files(files: list[UploadFile]):
    if not os.path.isdir("resources"):
        os.makedirs("resources")
    for file in files:
        with open(f"resources/{file.filename}", "wb+") as f:
            f.write(file.file.read())
    return {"status": "ok", "message": f"Uploaded {len(files)} files to the server."}

# app.mount("/site", StaticFiles(directory="client"), name="site")
# app.mount("/static", StaticFiles(directory="client/static"), name="static")
# Dynamic directory for outputs once first research is run
@app.on_event("startup")
def startup_event():
    if not os.path.isdir("outputs"):
        os.makedirs("outputs")
    app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

    if not os.path.isdir("resources"):
        os.makedirs("resources")
    app.mount("/resources", StaticFiles(directory="resources"), name="resources")

# templates = Jinja2Templates(directory="client")

manager = WebSocketManager()


# @app.get("/")
# async def read_root(request: Request):
#     return templates.TemplateResponse('index.html', {"request": request, "report": None})

@app.get("/status")
async def status():
    return {"status": "ok", "message": "MirrorScripts is running smoothly!"}


async def handle_start_command(data: str, websocket: WebSocket):
    json_data = json.loads(data[6:])
    task = json_data.get("task")
    report_type = json_data.get("report_type")
    agent = json_data.get("agent")
    # temporary so "normal agents" can still be used and not just auto generated, will be removed when we move to auto generated
    if agent == "Auto Agent":
        agent_dict = choose_agent(task)
        agent = agent_dict.get("agent")
        agent_role_prompt = agent_dict.get("agent_role_prompt")
    else:
        agent_role_prompt = None

    await websocket.send_json({"type": "logs", "output": f"Initiated an Agent: {agent}"})

    if task and report_type and agent:
        asyncio.create_task(manager.start_streaming(task, report_type, agent, agent_role_prompt, websocket))
    else:
        print("Error: not enough parameters provided.")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("start"):
                main_task = asyncio.create_task(handle_start_command(data, websocket))
                await asyncio.gather(main_task)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)