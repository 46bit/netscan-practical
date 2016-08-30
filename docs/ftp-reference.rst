.. _ref_ftp_reference:

============================================================
Introduction to the FTP Protocol
============================================================

FTP uses a Command socket and a Data socket, two independent connections for one FTP 'session.' To open an FTP Session, the FTP Client establishes a command connection by connecting to port 21 on the server. The
FTP Server then replies with a "welcome" message - generally the name and version of the running FTP server.

A lot of things about FTP seem unusual or bizarre now, but the FTP protocol predates HTTP (the protocol
you use to load websites). It was standardised about as we use it here by 1985. As such we have decades
of hindsight to judge it with. That it remains a common service reflects that it is 'good enough' to keep
using it rather than a more modern replacement.

------------------------------------------------------------
Authentication
------------------------------------------------------------

1. The FTP Client now sends a ``USER username_here`` message, to identify the user they wish to log in with.
2. If the username exists, the FTP Server replies with a ``331 Password required for student`` response - again on the Command connection.
3. The FTP Client now sends a ``PASS password_here`` message, givign the user's password.
4. If the username and password check out, the FTP Server responds with ``230 User student logged in``.

+---------+------------------------------------------------------+
|         | Command Messages or (*activity in italics*)          |
+=========+======================================================+
| Client: | (*connects to port 21 on the server*)                |
+---------+------------------------------------------------------+
| Server: | ``220 ProFTPD 1.3.5b Server``                        |
+---------+------------------------------------------------------+
| Client: | ``USER student``                                     |
+---------+------------------------------------------------------+
| Server: | ``331 Password required for student``                |
+---------+------------------------------------------------------+
| Client: | ``PASS golyeeHug6``                                  |
+---------+------------------------------------------------------+
| Server: | ``230 User student logged in``                       |
+---------+------------------------------------------------------+

------------------------------------------------------------
Using the Data Connection
------------------------------------------------------------

I mentioned that there are *two* types of connection in an FTP session. We've seen how the Command connection is used to pass commands and response messages back and forth, but no sign of the Data
Connection. The Data Connection only comes in when performing commands that provide some data beyond just
a status message. If uploading or downloading a file, the file contents go across a Data connection.

I say *a* data connection, because each data connection only carries the data for one command and is then
immediately closed. This is partly due to FTP's age: modern protocols would tend to include the data in
the command connection because it poses fewer problems.

To run a command that needs a data connection, the client first sends a ``PORT X,X,X,X,A,B`` command. The
``X,X,X,X`` encodes an IPv4 Address where the dots are replaced by commas. The ``A,B`` represents the Port to
connect to. Port numbers range from 1 to 65,535 (the range of a 16-bit unsigned integer) and thus the upper
8 bits are encoded as ``A`` and the lower 8 as `B`. Thus the socket ``192.168.1.1:21`` would be encoded as
``PORT 192,168,1,1,0,21``.

The server responds with a `200 PORT command successful` response, but in practice this merely means the
server was able to parse the `PORT` command. The data connection is only opened when the server is to
immediately send data.

The client can now execute a command that outputs data, such as ``LIST`` which lists the current directory.
The server will send a ``150 Opening ASCII mode data connection for file list`` response to indicate the
Data connection is being opened, and then the server will immediately send the data down the Data
connection. Once all the data is sent the server will close the connection and send a final
``226 Transfer complete`` response.

+---------+----------------------------------------------------------+
|         | Command Messages or (*activity in italics*)              |
+=========+==========================================================+
| Client: | (*listens on a random port, say 11240*)                  |
+---------+----------------------------------------------------------+
| Client: | ``PORT 192,168,56,1,43,232``                             |
+---------+----------------------------------------------------------+
| Server: | 200 PORT command successful                              |
+---------+----------------------------------------------------------+
| Client: | ``LIST``                                                 |
+---------+----------------------------------------------------------+
| Server: | (*opens a TCP connection to 192.168.56.1:11240*)``       |
+---------+----------------------------------------------------------+
| Server: | ``150 Opening ASCII mode data connection for file list`` |
+---------+----------------------------------------------------------+
| Server: | (*sends a listing of the current directory*)             |
+---------+----------------------------------------------------------+
| Client: | (*receives a listing of the current directory*)          |
+---------+----------------------------------------------------------+
| Server: | (*closes the data connection*)                           |
+---------+----------------------------------------------------------+
| Server: | ``226 Transfer complete``                                |
+---------+----------------------------------------------------------+

------------------------------------------------------------
A Short, Incomplete but Useful Command Reference
------------------------------------------------------------

+----------------------+------------------------------------------------------------------------+
| COMMAND              | Description                                                            |
+======================+========================================================================+
| ``PORT w,x,y,z,p,q`` | Set the IPv4 Address and Port for the next data connection.            |
+----------------------+------------------------------------------------------------------------+
| ``LIST``             | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``PWD``              | Print the current working directory                                    |
+----------------------+------------------------------------------------------------------------+
| ``CWD new_path``     | Change the current working directory                                   |
+----------------------+------------------------------------------------------------------------+
| ``RETR filename``    | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``DELE filename``    | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``STOR filename``    | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``QUIT``             | Close the current FTP Session                                          |
+----------------------+------------------------------------------------------------------------+

A completer listing is available `here <https://en.wikipedia.org/wiki/List_of_FTP_commands>`_ but I believe you'll find it confusing, rather than useful, for the following tasks.

..
    ----------------------
    FTP
    ----------------------

    The FTP protocol uses 2 TCP connections.

    Opening a connection:

    1. The FTP server listens on port 21 for incoming TCP connections.
    2. An FTP client opens a connection to the server on port 21.
    3. The FTP server accepts the connection and requests a username.
    4. The FTP client provides a username.
    5. If the username is valid, the server requests a password.
    6. The FTP client provides a password.
    7. If the username and password are valid, the server logs you in.

    Issuing a command (in Active Mode):

    1. The FTP client starts listening for a data connection, on a randomly picked port.
    2. The FTP client tells the server an IP address and Port it can open a data connection to.
    3. The FTP client issues another command, one that requires or returns data. Such as a file upload or
       download, or a directory listing.
    4. The FTP server opens the data connection to the provided address. It then sends an success/failure
       message to the client using the command connection.
    5. For something returning data, the server sends data down the data connection. Otherwise the client
       sends data up the data connection.
    6. Once that is complete, the server sends a success/failure message to the client using the command
       connection.

    Messages across the Command connection while connecting to FTP:

    +--------------------------+---------------------------------------------------------+
    | CLIENT SENDS             | SERVER SENDS                                            |
    +==========================+=========================================================+
    | *connect to port 21*     |                                                         |
    +--------------------------+---------------------------------------------------------+
    |                          | 220 ProFTPD 1.3.5b Server                               |
    +--------------------------+---------------------------------------------------------+
    | **USER student**         |                                                         |
    +--------------------------+---------------------------------------------------------+
    |                          | 331 Password required for student                       |
    +--------------------------+---------------------------------------------------------+
    | **PASS golyeeHug6**      |                                                         |
    +--------------------------+---------------------------------------------------------+
    |                          | 230 User student logged in                              |
    +--------------------------+---------------------------------------------------------+

    Messages across the Command connection while Retrieving a file list to a local port:

    +-------------------------------+------------------------------------------------------+
    | CLIENT SENDS                  | SERVER SENDS                                         |
    +===============================+======================================================+
    | *listens on port 11240*       |                                                      |
    +-------------------------------+------------------------------------------------------+
    | **PORT 192,168,56,1,43,232**  |                                                      |
    +-------------------------------+------------------------------------------------------+
    |                               | 200 PORT command successful                          |
    +-------------------------------+------------------------------------------------------+
    | **LIST**                      |                                                      |
    +-------------------------------+------------------------------------------------------+
    |                               | *opens a TCP connection to 192.168.56.1:11240*       |
    +-------------------------------+------------------------------------------------------+
    |                               | 150 Opening ASCII mode data connection for file list |
    +-------------------------------+------------------------------------------------------+
    | (receives data on port 11240) |                                                      |
    +-------------------------------+------------------------------------------------------+
    |                               | 226 Transfer complete                                |
    +-------------------------------+------------------------------------------------------+

    Messages across the Command connection while Sending a file list to the commands of another FTP server:

    +--------------------------+---------------------------------------------------------+
    | CLIENT SENDS             | SERVER SENDS                                            |
    +==========================+=========================================================+
    | **PORT 8,8,8,8,0,21**    |                                                         |
    +--------------------------+---------------------------------------------------------+
    |                          | 200 PORT command successful                             |
    +--------------------------+---------------------------------------------------------+
    | **LIST**                 |                                                         |
    +--------------------------+---------------------------------------------------------+
    |                          | *tries opening a TCP connection to 192.168.56.1:11240*  |
    +--------------------------+---------------------------------------------------------+
    |                          | 425 Unable to build data connection: Connection refused |
    +--------------------------+---------------------------------------------------------+
    |                          | 450 LIST: Connection refused                            |
    +--------------------------+---------------------------------------------------------+
    |                          |                                                         |
    +--------------------------+---------------------------------------------------------+

    Logging in::

        (client)                     (server)
                                     ← 220 ProFTPD 1.3.5b Server (ProFTPD Default Installation) [192.168.56.101]
        USER student         →       # authenticate
                                     ← 331 Password required for student
        PASS golyeeHug6         →
                                     ← 230 User student logged in

    Setting the IP Address and Port for the data connection::

        (client)                     (server)
        PORT 192,168,56,1,43,232 →   # have the server open data connections to 192.168.56.1:11240
                                     ← 200 PORT command successful

    Listing the current directory when something is listening on the data port::

        (client)                     (server)
        LIST →                       # list the files in the current directory, to the data connection
                                     ← 150 Opening ASCII mode data connection for file list
                                     ← 226 Transfer complete

    Listing the current directory when *nothing* is listening on the data port::

        (client)                     (server)
        LIST →                       # list the files in the current directory, to the data connection
                                     ← 425 Unable to build data connection: Connection refused
                                     ← 450 LIST: Connection refused

    This exercise uses the File Transfer Protocol. This is an old yet still common protocol for sharing files. ::

        USER student               # authenticate
        PASS golyeeHug6

        PORT 192,168,56,1,43,232   # have the server open data connections to 192.168.56.1:11240
        LIST                       # list the files in the current directory, to the data connection
        RETR example.txt           # print the content of example.txt, to the data connection

        QUIT                       # end session

    We wouldn't normally issue these commands by hand. The `ftp` command line tool acts as a more convenient wrapper around the underlying commands. We need to recieve the LIST output and file contents on port 11240, which would otherwise require hand-cranking something like `netcat`.

    To do the above in ``ftp``, we'd type::

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
