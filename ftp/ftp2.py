import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cp_ftp import FTP

ftp = FTP("192.168.56.101", debug=True)
ftp.send_login_commands("student", "golyeeHug6")
for port in range(1, 65536):
  target_address = ("192.168.56.102", port)
  ftp.send_port_command(target_address)
  ftp.recv_response()

  ftp.send_command("LIST")
  ftp.recv_response()
  final_list_response = ftp.recv_response()

  if final_list_response.text != "450 LIST: Connection refused":
    print("> %d is open." % port)
ftp.close()
