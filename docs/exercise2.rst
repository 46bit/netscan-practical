.. _ref_exercise2:

============================================================
Exercise 2: Scanning a Private Network
============================================================

In Exercise 1 we scanned a publicly-accessible server, and discovered it was running an FTP service. In this
exercise we're going to abuse that FTP server to reconnoiter the private network it is connected to. Then
we'll see if we can do anything useful to an attacker.

``nmap`` is software built specifically for Network Scanning. Here we're repurposing legitimate services to
scan networks we otherwise could not access.

For the purposes of this Exercise we have revived a security issue from the mid-90s, where people started to
use a design quirk of the FTP protocol in this manner. Modern exploits can deliver similar capabilities but
tend to be much more complex, which would complicate this simple example.

------------------------------------------------------------
Design of The FTP Protocol
------------------------------------------------------------

FTP stands for File Transfer Protocol. It dates from 1971 but is still in widespread use. It is a standard
for sharing files over the Internet - very much an old version of Dropbox or Google Drive. A typical session consists of an FTP client connecting to an FTP server on port 21. It then sends a login, e.g.
``USER student`` and ``PASS golyeeHug6``.

Provided the server accepts these details, the client can then send commands. Such as deleting a file with
``DELE file.txt``. If the deletion was successful, the server responds with a ``250 DELE command successful``
message.

************************************************************
Data Connections
************************************************************

The ``DELE`` command results in a simple success or failure message. But if you're downloading or uploading
file contents, FTP sends that data over a separate connection.

1. The Client sends ``PORT A,B,C,D,P1,P2`` to indicate the IP Address A.B.C.D and Port P1P2 that the server
   could open a data connection to.
2. The Client then sends a command which requires a data connection. Such as ``LIST`` for a list of files in
   the current directory. Or ``RETR file2.txt`` to get the contents of the file ``file2.txt``. Or
   ``STOR file3.txt`` to upload a file.
3. The Server connects to the address specified by the previous ``PORT`` command, sends the data, and closes
   the connection. For file uploads, the Server opens the connection and the client sends data and closes it.

.. _ref_exercise2_ftp_bounce:

************************************************************
FTP Bounce
************************************************************

There was no requirement for that ``PORT`` command to go to the Client's IP Address. You could send file
contents anywhere the FTP Server could access. If the FTP server was connected to a private network, such
as a home or corporate network, you could send data to hosts on that network.

This tells you there isn't an FTP server running on 192.168.56.102::

    Client: PORT 192,168,56,102,0,21
    Server: 200 PORT command successful

    Client: RETR evil_ftp_commands.txt
    Server: 425 Unable to build data connection: Connection refused
    Server: 450 LIST: Connection refused

This tells you there is an FTP server running on 192.168.56.103::

    Client: PORT 192,168,56,103,0,21
    Server: 200 PORT command successful

    Client: RETR evil_ftp_commands.txt
    Server: 150 Opening ASCII mode data connection for file list
    Server: 226 Transfer complete

You just sent the contents of ``evil_ftp_commands.txt`` to the FTP server on 192.168.56.103, and it will run
the contents as FTP commands. If you include a ``PORT`` command pointing to you, you can even have that FTP
Server send you a list of files or their contents.

This technique is named FTP Bounce, as you're bouncing requests off the FTP Server. With it you could:

* Discover their internal servers.
* Enumerate which services are running.
* Interact with internal, private FTP servers.
* Send commands to some shells and databases, but generally not read the output.

For the following tasks, you will find this useful: :ref:`ref_ftp_reference`

------------------------------------------------------------
Task 1: Experiment with FTP
------------------------------------------------------------

In ``ftp/examples`` you'll find a number of Python scripts. These are examples of how to do various
operations, as explained in :ref:`ref_ftp_reference`

1. Try saving some text as a file::

    examples/stor.py

2. Try listing files in the current directory::

    python3 examples/retr.py

3. Try retrieving a file::

    python3 examples/retr.py

4. Try deleting a file::

    python3 examples/retr.py

5. Try sending data to a another service::

    python3 examples/remote_port.py

You'll notice these examples all print the commands moving back and forth. This is controlled by a
``debug=True`` parameter you can see if you open up the files. Play about and get familiar with how things
work.

------------------------------------------------------------
Task 2: Discover hosts on the internal network
------------------------------------------------------------

This is the provided ``examples/remote_port.py``::

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

We'd like to quickly discover all hosts running on the ``192.168.0.X`` subnet. We could try every port on
every host ``192.168.0.1`` through ``192.168.0.255``, but that's ``255 * 65,536 = 16,711,680`` attempts.

To keep things quick, just check port ``22`` on each of those IP Addresses. To make things quicker, only scan
from ``192.168.0.101`` to ``192.168.0.132``.

Make a list of which IP Addresses connect successfully.

Hint: You can see the difference between successful/unsuccessful under :ref:`ref_exercise2_ftp_bounce`. See whether code 150 was recieved.

Hint: use a new ``FTP`` instance each time, and loop over each IP Address.

------------------------------------------------------------
Task 3: Port scan discovered hosts
------------------------------------------------------------

Now you want to find out which services are running on the hosts we discovered. You can do this by trying
each port from ``1`` to ``65,535``.

To keep things quick, only try privileged ports (those from ``1`` to ``1023``).

You should start to sense how you discover what is running, and get to look for options for attack.

You may also be save the output from each service onto a file on the file on the FTP Server, using ``RETR``.

------------------------------------------------------------
Extension Task: Exfiltrate data from a private FTP server
------------------------------------------------------------

For our next task we want to retrieve secret files from this network's private FTP server. You may have
noticed in Task 3 that there's an FTP server running on port 21 of ``192.168.56.102``. If you try
``nc 192.168.56.102 21`` you'll find you can't connect from your own computer. But you've found that
``192.168.56.101`` can.

Here's the trick: you can send the contents of a file to the FTP server on port 21 of ``192.168.56.102`` and
it'll interpret each line of the contents as a command. So you can tell it to do things. Like send you their
secret weapon blueprints.

You could put a ``PORT`` command corresponding to a ``new_data_address`` into that file, then put ``LIST``.
Then the ``192.168.56.102`` FTP server will send your computer a list of files you can get with ``ftp.recv_data()``.

This is actually quite tricky to do with limited knowledge. But if you get it working, congratulations!

:ref:`ref_conclusion`
