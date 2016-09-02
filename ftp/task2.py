import sys, os
from cp_ftp import FTP

# List of discovered host IP addresses.
hosts = []

for last_octet in range(101, 132):
  # Make a new FTP connection each time for simplicity.
  ftp = FTP("192.168.56.101", debug=True)
  ftp.send_login_commands("student", "golyeeHug6")

  host = "192.168.56.%d" % last_octet
  target_address = (host, 22)

  ################################################################################
  # STUDENT TODO 1: Send a PORT command for target_address. Then send data to it.
  # Hint: the provided examples/remote_port.py will be useful.
  # Important: if a port is open then run:
  #   hosts.append(host)
  ################################################################################

  ftp.close()

print(hosts)
