import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from cp_ftp import FTP

# List of discovered host IP addresses.
hosts = ["192.168.56.102", "192.168.56.103"]
hosts_ports = {}

for host in hosts:
  hosts_ports[host] = []

  for port in range(1, 1024):
    # Make a new FTP connection each time for simplicity.
    ftp = FTP("192.168.56.101", debug=False)
    ftp.send_login_commands("student", "golyeeHug6")

    target_address = (host, port)

    ################################################################################
    # STUDENT TODO 1: Send a PORT command for target_address. Then send data to it.
    # Hint: the provided examples/remote_port.py will be useful.
    # Important: if a port is open then run:
    #   hosts_ports[host].append(port)
    ################################################################################

    # Send a PORT command pointing to target port on target host.
    ftp.send_port_command(target_address)
    # If the PORT command was somehow invalid, skip this host.
    response = ftp.recv_response()
    if response.code != 200:
      print(response)
      continue

    # Try sending file LIST output to target on chosen port.
    ftp.send_command("LIST")
    response = ftp.recv_response()
    print(target_address, response)

    # Success is indicated by this response:
    #   150 Opening ASCII mode data connection for file list
    if response.code == 150:
      hosts_ports[host].append(port)

    ftp.close()

for host in hosts:
  print("%s has ports %s open." % (host, ", ".join(map(str, hosts_ports[host]))))
