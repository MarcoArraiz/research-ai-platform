import os
import sys
import uuid
import time
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Add project root to path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.executor import ResearchExecutor
from src.crew.research_crew import ResearchCrew
from src.utils import agent_logic
from src.database.repository import ResearchRepository

# Simple in-memory storage for tasks
# In a real app, this should be in a database or Redis
class TaskManager:
    def __init__(self):
        self.executors: Dict[str, ResearchExecutor] = {}
        self.results: Dict[str, Any] = {}
        self.topics: Dict[str, str] = {}

    def create_task(self, topic: str) -> str:
        task_id = str(uuid.uuid4())
        executor = ResearchExecutor()
        self.executors[task_id] = executor
        self.topics[task_id] = topic
        return task_id

    def get_executor(self, task_id: str) -> ResearchExecutor:
        return self.executors.get(task_id)

    def get_result(self, task_id: str):
        return self.results.get(task_id)

task_manager = TaskManager()


tags_metadata = [
    {
        "name": "Research",
        "description": "Operations relating to the AI research process.",
    },
    {
        "name": "General",
        "description": "General API information.",
    },
]

app = FastAPI(
    title="Elaia Research Platform API",
    description="API for the Elaia Research Platform, powered by Autonomous AI Agents.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Elaia Research Platform API is running", "docs_url": "/docs"}

@app.get("/api/research", tags=["Research"])
def research_info():
    return {"message": "Send a POST request to this endpoint with {'topic': 'your topic'} to start research."}

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    task_id: str
    message: str

class StatusResponse(BaseModel):
    status: str
    logs: list[str]
    is_running: bool

class ResultResponse(BaseModel):
    result: str | None

def run_research_background(task_id: str, topic: str):
    executor = task_manager.get_executor(task_id)
    if not executor:
        return
    
    def background_job(topic):
        def step_callback(step):
            current_role = None
            if hasattr(step, 'agent'):
                current_role = getattr(step.agent, 'role', str(step.agent))
            role_key = agent_logic.detect_agent_role(step, current_role)
            
            if hasattr(step, 'thought') and step.thought:
                display_name = agent_logic.get_agent_display_name(role_key)
                executor.logs.put(f"💭 **{display_name}**: {step.thought[:150]}...")

        crew = ResearchCrew(topic=topic)
        return crew.run(step_callback=step_callback)

    executor.submit(background_job, topic)

@app.post("/api/research", response_model=ResearchResponse, tags=["Research"], summary="Start Research Task")
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """
    **Start a new research processing task.**
    
    - **topic**: The topic to research (e.g., "AI in Healthcare").
    
    Returns a unique `task_id` to track progress.
    """
    task_id = task_manager.create_task(request.topic)
    
    # Start the actual processing in the background
    background_tasks.add_task(run_research_background, task_id, request.topic)
    
    return ResearchResponse(task_id=task_id, message="Research started successfully")

@app.get("/api/research/{task_id}/status", response_model=StatusResponse, tags=["Research"], summary="Get Task Status")
async def get_status(task_id: str):
    """
    **Get the current status and logs of a research task.**
    """
    executor = task_manager.get_executor(task_id)
    if not executor:
        raise HTTPException(status_code=404, detail="Task not found")
    
    logs = executor.get_logs()
    
    # Check simple status
    status = "running" if executor.is_running else "completed"
    
    # Check for result or error
    result = executor.check_status()
    if result:
         if isinstance(result, str) and result.startswith("Error"):
             status = "failed"
         elif not executor.is_running:
             status = "completed"
             task_manager.results[task_id] = str(result)
    
    return StatusResponse(
        status=status,
        logs=logs,
        is_running=executor.is_running
    )

@app.get("/api/research/{task_id}/result", response_model=ResultResponse, tags=["Research"], summary="Get Final Result")
async def get_result(task_id: str):
    """
    **Retrieve the final markdown report.**
    """
    if task_id not in task_manager.results:
        # Check if it's done but result not cached yet
        executor = task_manager.get_executor(task_id)
        if executor:
            result = executor.check_status()
            if result and not executor.is_running and not (isinstance(result, str) and result.startswith("Error")):
                task_manager.results[task_id] = str(result)
            else:
                return ResultResponse(result=None)
        else:
             raise HTTPException(status_code=404, detail="Task not found")
             
    return ResultResponse(result=task_manager.results.get(task_id))
