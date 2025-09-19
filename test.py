import re
# Below part of code clears all content in AgentFunction.py to insert updated python code by deleting existing python code.
code_file="./AgentFunction.py"
            # Read original code
with open(code_file, 'r') as file:
    code = file.read()

# Build a regex pattern to remove each function in agent_names
func_name="ID_Fetching_Agent"
func_name=func_name.replace(" ","_")
print("Func_Name = ",func_name)
pattern = rf"^def\s+{func_name}\s*\(.*?\):\n(?:[ \t]+.*\n)*"
code = re.sub(pattern, '', code, flags=re.MULTILINE)
print("Code = ")
print(code)
# Write the updated code back to the file
with open(code_file, 'w') as file:
    file.write(code)