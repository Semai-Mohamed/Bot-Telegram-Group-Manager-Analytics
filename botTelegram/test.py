## for test 
import re

example = 'mute 5h @mohamed'
match = re.match(r'mute (\d+)([mh])(?:\s*@([A-Za-z0-9_]+))?', example)
if match:
    value = match.group(1)  
    unit = match.group(2) 
    name = match.group(3) 
    print(unit)
    print(value)
    print(name)
else:
    print("No match found.")