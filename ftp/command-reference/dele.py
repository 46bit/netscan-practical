import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from cp_ftp import FTP

ftp = FTP("192.168.56.101", debug=True)
ftp.send_login_commands("student", "golyeeHug6")

data_address = ftp.new_data_address()
ftp.send_port_command(data_address)
response = ftp.recv_response()
if response.code != 200:
  print(response)
  sys.exit(1)

file_to_delete = "file.txt"

ftp.send_command("DELE %s" % file_to_delete)
response = ftp.recv_response()
if response.code != 250:
  print(response)
  sys.exit(1)

ftp.close()
