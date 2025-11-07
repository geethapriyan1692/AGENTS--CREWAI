from Load.load import load_yaml
from Custom.custom import create_tool_class
import re
from agent_logger.logger_config import setup_logger
import traceback
import logging
setup_logger()
LOGGER = logging.getLogger(__name__)
crew_file = "/code/agents/crew.py"
agents_config = "/code/agents/agents.yaml"
tasks_config = "/code/agents/tasks.yaml"


def update_crew(agent: str):
    
    """
    Author : Gnana Bharathi S
    Created On : 23/04/2025
    This method is for updating code in crew.py.
    """
    
    
    agents_data = load_yaml(agents_config) #Extracting agents.yaml file data
    tasks_data = load_yaml(tasks_config) #Extracting tasks.yaml file data

    try:
        with open(crew_file, "r") as file:
            crew_content = file.readlines()
    except FileNotFoundError:
        LOGGER.error(traceback.format_exc())
        return

    class_start = None
    class_end = None
    for i, line in enumerate(crew_content):
        if "class CodeGeneration" in line:
            class_start = i
        if class_start is not None and line.strip() == "":  # Detect blank line after class
            class_end = i
            break

    class_end = 88 # Line number in crew.py where data starts updating.

    if class_start is None:
        LOGGER.error(traceback.format_exc())
        return

    existing_agents = set(re.findall(r"@agent\n\s*def (\w+)\(", "".join(crew_content))) #Extracting existing agents.
    existing_tasks = set(re.findall(r"@task\n\s*def (\w+)\(", "".join(crew_content))) #Extracting existing tasks.


    new_methods = []
    new_methods.append("\n\n")

    # Add new agents
    for agent_name in list(agents_data.keys()):
        #tool_name = ''.join(word.capitalize() for word in agent_name.split('_'))
        if agent_name not in existing_agents and "executor" in agent_name: #For agent_executor
            create_tool_class(agent)
            agent_method = "    @agent\n"
            agent_method += "    def {0}(self) -> Agent:\n".format(agent_name)
            agent_method += "        from tools import custom_tool\n"
            agent_method += "        importlib.reload(custom_tool)\n" 
            agent_method += "        from tools.custom_tool import {0}\n".format(agent)
            agent_method += "        return Agent(\n"
            agent_method += "            config=self.agents_config['{0}'],\n".format(agent_name)
            agent_method += "            verbose=True,\n"
            agent_method += "            tools=[{0}()]\n".format(agent)
            agent_method += "        )\n"
            new_methods.append(agent_method)
        elif agent_name not in existing_agents: #For agent_generator
            agent_method = "    @agent\n"
            agent_method += "    def {0}(self) -> Agent:\n".format(agent_name)
            agent_method += "        return Agent(\n"
            agent_method += "            config=self.agents_config['{0}'],\n".format(agent_name)
            agent_method += "            verbose=True\n"
            agent_method += "        )\n"
            new_methods.append(agent_method)


    # Add new tasks
    for task_name in list(tasks_data.keys()):
        file_name = task_name[:-15]
        if task_name not in existing_tasks and "executor" not in task_name: #For task_generator
            task_method = "    @task\n"
            task_method += "    def {0}(self) -> Task:\n".format(task_name)
            task_method += "        return Task(\n"
            task_method += "            config=self.tasks_config['{0}'],\n".format(task_name)
            task_method += "            callback=customLogic"
            task_method += "        )\n"
            new_methods.append(task_method)
        elif task_name not in existing_tasks: #For task_executor
            task_method = "    @task\n"
            task_method += "    def {0}(self) -> Task:\n".format(task_name)
            task_method += "        return Task(\n"
            task_method += "            config=self.tasks_config['{0}']\n".format(task_name)
            task_method += "        )\n"
            new_methods.append(task_method)


    if not new_methods:
        # LOGGER("No new agents or tasks to add.")
        pass

    updated_content = crew_content[:class_end] + ["\n".join(new_methods) + "\n"] + crew_content[class_end:]

    with open(crew_file, "w") as file:
        file.writelines(updated_content)

    return "Success"