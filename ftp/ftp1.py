import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ftp import FTP

ftp = FTP("192.168.56.101")
ftp.login("student", "golyeeHug6")

for port in range(1, 65536):
  ftp.sendport("192.168.56.102", port)
  ftp.putcmd("LIST")
  ftp.getline()
  if ftp.getline() != "450 LIST: Connection refused":
    print("> %d is open." % port)

ftp.quit()

############################################################
############################################################
############################################################
############################################################
############################################################

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ftp import FTP

ftp = FTP("192.168.56.101")
ftp.set_debuglevel(1)
ftp.login("student", "golyeeHug6")

ftp.sendport("192.168.56.102", 21)
ftp.putcmd("LIST")
ftp.read_line()
if ftp.read_line() != "450 LIST: Connection refused":
  print("> %d is open." % 21)

ftp.quit()

############################################################
############################################################
############################################################
############################################################
############################################################

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ftp import FTP

ftp = FTP("192.168.56.101")
ftp.set_debuglevel(1)
ftp.login("student", "golyeeHug6")

ftp.makeport()
#ftp.sendport("192.168.56.102", 21)
ftp.set_pasv(1)
ftp.list()
#if ftp.read_line() != "450 LIST: Connection refused":
#  print("> %d is open." % 21)

ftp.quit()

############################################################
############################################################
############################################################
############################################################
############################################################

# ftp.send_command(cmd)
# ftp.recv_response
# ftp.send_port
# ftp.setup_port
# ftp.
