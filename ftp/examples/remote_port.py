import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from cp_ftp import FTP

ftp = FTP("192.168.56.101", debug=True)
ftp.send_login_commands("student", "golyeeHug6")

target_address = ("192.168.56.103", 21)
ftp.send_port_command(target_address)
response = ftp.recv_response()
if response.code != 200:
  print(response)
  sys.exit(1)

ftp.send_command("LIST")
response = ftp.recv_response()
if response.code != 150:
  print(response)
  sys.exit(1)

# No Data is received because it was sent somewhere besides this program!
response = ftp.recv_response()
if response.code != 226:
  print(response)
  sys.exit(1)

ftp.close()
