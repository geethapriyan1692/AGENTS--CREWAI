from typing import Type, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import importlib
from main import FinalOutput
class AgentOutput(BaseModel):
    	agentOutput: Any
shared_response = AgentOutput(agentOutput="")


