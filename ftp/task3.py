import sys, os
from cp_ftp import FTP

################################################################################
# STUDENT TODO 1: List of discovered host IP addresses.
# Change this array to the hosts output by `task2.py`.
################################################################################
hosts = []

hosts_ports = {}

for host in hosts:
  hosts_ports[host] = []

  for port in range(1, 1024):
    # Make a new FTP connection each time for simplicity.
    ftp = FTP("192.168.56.101", debug=True)
    ftp.send_login_commands("student", "golyeeHug6")

    target_address = (host, port)

    ################################################################################
    # STUDENT TODO 1: Send a PORT command for target_address. Then send data to it.
    # Hint: the provided examples/remote_port.py will be useful.
    # Important: if a port is open then run:
    #   hosts_ports[host].append(port)
    ################################################################################

    ftp.close()

for host in hosts:
  print("%s has ports (%s) open." % (host, ", ".join(map(str, hosts_ports[host]))))
