.. _ref_answers:

============================================================
Answers
============================================================

------------------------------------------------------------
Exercise 1
------------------------------------------------------------

These answers are largely down to your exact network setup.

------------------------------------------------------------
Exercise 2
------------------------------------------------------------

************************************************************
Task 2: Discover hosts on the internal network
************************************************************

::

    import sys, os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
    from cp_ftp import FTP

    # List of discovered host IP addresses.
    hosts = []

    for last_octet in range(101, 132):
      # Make a new FTP connection each time for simplicity.
      ftp = FTP("192.168.56.101", debug=False)
      ftp.send_login_commands("student", "golyeeHug6")

      # Send a PORT command pointing to port 22 on this target.
      host = "192.168.56.%d" % last_octet
      target_address = (host, 22)
      ftp.send_port_command(target_address)
      # If the PORT command was somehow invalid, skip this target.
      response = ftp.recv_response()
      if response.code != 200:
        print(response)
        continue

      # Try sending file LIST output to target on port 22.
      ftp.send_command("LIST")
      response = ftp.recv_response()
      print(target_address, response)

      # Success is indicated by this response:
      #   150 Opening ASCII mode data connection for file list
      if response.code == 150:
        hosts.append(target_address)

      ftp.close()

    print(hosts)

************************************************************
Task 3: Port scan discovered hosts
************************************************************

::

    import sys, os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
    from cp_ftp import FTP

    # List of discovered host IP addresses.
    hosts = []

    for port in range(1, 65536):
      # Make a new FTP connection each time for simplicity.
      ftp = FTP("192.168.56.101", debug=False)
      ftp.send_login_commands("student", "golyeeHug6")

      # Send a PORT command pointing to target port on target host.
      target_address = ("192.168.56.101", port)
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
        hosts.append(target_address)

      ftp.close()

    print(hosts)

************************************************************
Extension Task: Exfiltrate data from a private FTP server
************************************************************

:ref:`ref_license`
