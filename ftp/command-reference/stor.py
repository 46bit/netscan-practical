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

file_to_store = "file.txt"
file_contents = "ABCDEF"

ftp.send_command("STOR %s" % file_to_store)
response = ftp.recv_response()
if response.code != 150:
  print(response)
  sys.exit(1)

ftp.send_data(file_contents)
response = ftp.recv_response()
if response.code != 226:
  print(response)
  sys.exit(1)

ftp.close()
