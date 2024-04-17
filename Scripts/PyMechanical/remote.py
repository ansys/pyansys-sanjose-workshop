### Imports

from ansys.mechanical.core import launch_mechanical
from pathlib import Path
import os

### Input Parameters : Folders . Ansys Version

inputs_dir = os.path.join(os.getcwd(),"inputs")
outputs_dir = os.path.join(os.getcwd(),"outputs")
work_dir = os.path.join(os.getcwd(),"wdir")

# script file with commands
mech_script_file = "valve_commands_for_remote.py"

ansys_version = 241


### Construct Absolute File paths

# Absolute path of script file with commands
remote_commands_file = os.path.join(inputs_dir,mech_script_file )

# Get executable Path for the above Ansys Version
dir_needed = f'ANSYS{ansys_version}_DIR'
ansdir = os.environ[dir_needed]
full_path=os.path.join(Path(ansdir).parent.absolute(),"aisol","bin","winx64","AnsysWBU.exe")


### Using  Executable(AnsysWBU)  path , Launch Remote session of Mechanical and connect to it.


mechanical = launch_mechanical(exec_file=full_path, verbose_mechanical=True, batch=False)
print(mechanical)

### Run commands from a scipt file in this Mechanical session remotely.
run_remote_commands = mechanical.run_python_script_from_file(remote_commands_file)

### Disconnect by  Closing the Remote Session.
mechanical.exit()


