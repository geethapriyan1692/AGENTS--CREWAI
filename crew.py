from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
import re
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# from crewai.project import CrewBase, agent, crew, task
import importlib
from pydantic import BaseModel
from crewai.tasks.task_output import TaskOutput
import cx_Oracle
from app_config import config_loader
dev_ml_username=config_loader.get('ml_username')
dev_ml_password=config_loader.get('ml_password')
dev_ml_service_name=config_loader.get('ml_service_name')
dev_ml_host=config_loader.get('ml_catalog_host')
dev_ml_port=config_loader.get('ml_port')

class CodeOutput(BaseModel):
    code: str

def customLogic(result: TaskOutput):
    lines = str(result) # result: TaskOutput, has the output of generator task.
    # Use regex to extract function name after 'def'
    match = re.search(r'def\s+(\w+)\s*\(', lines) # Finding function_name using regex pattern.
    if match:
        agentName = match.group(1)
    else:
        agentName = None  # or handle accordingly
    methodName=agentName # For proper name for agent_name and methodName
    agentName=agentName.replace("_"," ") # For proper name for agent_name and methodName
    match = re.search(r'```(?:python)?\n(.*?)```', lines, re.DOTALL | re.IGNORECASE)
    extracted_code=lines
    if match:
        extracted_code = match.group(1).strip()  # Extracting the code using regex pattern.
    ext = extracted_code.encode()
    connection = cx_Oracle.connect(user=dev_ml_username, password=dev_ml_password, dsn=cx_Oracle.makedsn(dev_ml_host,dev_ml_port,service_name=dev_ml_service_name))
    cursor = connection.cursor()
    check_for_code_query=config_loader.get('check_for_code_query')
    sel= check_for_code_query.format(agentName,"custom_logic")
    cursor.execute(sel)
    rows = cursor.fetchall()
    if(len(rows)>0):
        pass
    else:
        sql = config_loader.get('insert_query') # Inserting generated code data in oracle db.
        cursor.execute(sql, (agentName, "custom_logic", ext, methodName))
        connection.commit()
        cursor.close()
        connection.close()
        #Above code is for inserting generated code in crewai_config table with respective agent)name, config_type, config_data, method_name.
        filename = r"/code/agents/AgentFunction.py"
        with open(filename, 'a+', encoding='utf-8') as file:
            file.seek(0) # To point from starting index of file
            content = file.read() # Reads the AgentFunction file content
            existing_methods = set(re.findall(r'def\s+(\w+)\s*\(', "".join(content))) # Extracts all function names presents in AgentFunction.py file.
            agent_check=agentName.replace(" ","_")
            #If function name from generated code is not present in AgentFunction then only write it in AgentFunction.py
            if agent_check not in existing_methods:
                file.write(extracted_code)
                file.write("\n")

@CrewBase
class CodeGeneration():
    """ crew"""
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "/code/agents/agents.yaml"
    tasks_config = "/code/agents/tasks.yaml"
    def __init__(self, selected_agents=None, selected_tasks=None):
        self.selected_agents=selected_agents
        self.selected_tasks=selected_tasks
        with open(self.agents_config, 'r') as f:
            self.agents_config=yaml.safe_load(f)
        with open(self.tasks_config, 'r') as f:
            self.task_config=yaml.safe_load(f)















    







    



















    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task


    @crew
    def crew(self) -> Crew:
        agents = []
        tasks = []
        if self.selected_agents:
            for agent_name in self.selected_agents:
                if hasattr(self, agent_name):
                    agent_instance = getattr(self, agent_name)()
                    agents.append(agent_instance)
                else:
                    raise ValueError(f"Agent '{agent_name}' not found.")
        else:
            agents = list(self.agents.values())

        if self.selected_tasks:
            for task_name in self.selected_tasks:
                if hasattr(self, task_name):
                    task_instance = getattr(self, task_name)()
                    tasks.append(task_instance)
                else:
                    raise ValueError(f"Task '{task_name}' not found.")
        else:
            tasks = list(self.tasks.values())
        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )