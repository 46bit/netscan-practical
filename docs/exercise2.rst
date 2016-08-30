.. _ref_exercise2:

============================================================
Exercise 2: Scanning a Private Network
============================================================

In Exercise 1 we scanned a publicly-accessible server, and discovered it was running an FTP service. In this
exercise we're going to abuse that FTP server to reconnoiter the private network it is connected to. Then
we'll see if we can do anything useful to an attacker.

For the purposes of this Exercise we have revived a security issue from the mid-90s, where people started to
use a design quirk of the FTP protocol in this manner. Modern exploits can deliver similar capabilities but
tend to be much more complex, which would complicate this simple example.

------------------------------------------------------------
Design of The FTP Protocol
------------------------------------------------------------

This gives a qualitative explanation of what FTP is and how it works. For full details (potentially useful
for the Tasks below) see the :ref:`ref_ftp_reference`.

FTP stands for File Transfer Protocol. It dates from 1971 but is still in widespread use. It is a standard
for sharing files over the Internet - very much an old version of Dropbox or Google Drive. A typical session consists of an FTP client connecting to an FTP server on port 21. It then sends a login, e.g.
``USER student`` and ``PASS golyeeHug6``.

Provided the server accepts these details, the client can then send commands. Such as deleting a file,
``DELE file.txt``. They can also get data from the server. For commands which return data, such as a list of
files in the current directory or the contents of a file, FTP uses a separate connection to send that data.

The Client sends ``PORT A,B,C,D,P1,P2`` to indicate the IP Address A.B.C.D and Port P1P2 that the server can
open the data connection to. Then the client can ask for a file list by sending ``LIST``. Or download a file
by sending ``RETR file2.txt``. Or upload a file by sending ``STOR file3.txt``. In that last case, the server
opens the Data connection and the client sends the data along it.

This feature also allows you to access services on the same private network as the FTP Server. You can
specify any IP address and port in the ``PORT`` command - including ones you can't access on its local
private network. Such as ``192.168.56.102``, which is in the private subnet.

Usefully for network scanning, the FTP Server tells you over the command port whether it was able to
establish a data connection or not. But that's after opening a TCP connection and sending data that might
be the contents of a file you uploaded.

[EXCERPT]

FTP Bounce lets you send chosen TCP data to a specified IP Address and Port, and tells you whether a
connection could be established. This lets you do lots of things useful for learning about someone's
network:

* Discover their internal servers.
* Enumerate which services are running.
* Interact with internal, private FTP servers.
* Send commands to some shells and databases, but generally not read the output.

------------------------------------------------------------
Task 1: Experiment with FTP
------------------------------------------------------------

In ``ftp/examples`` you'll find a number of Python scripts. These are examples of how to do various
operations, as explained in `the FTP reference <ftp-reference.html#a-short-incomplete-but-useful-command-reference>`_.

::

    # Try uploading a file.
    python3 examples/stor.py

    # Try listing files in the current directory.
    python3 examples/retr.py

    # Try retrieving a file.
    python3 examples/retr.py

    # Try deleting a file.
    python3 examples/retr.py

    # Try sending data to a another service.
    python3 examples/remote_port.py

You'll notice these examples all print the commands moving back and forth. This is controlled by a
``debug=True`` parameter you can see if you open up the files. Play about and get familiar with how things
work.

------------------------------------------------------------
Task 2: Discover hosts on the internal network
------------------------------------------------------------

Try adapting ``examples/remote_port.py`` to send data to port 22 of each IP Address on ``192.168.X.X``. So
you'll want to iterate through ``192.168.0.1``, …, ``192.168.0.255``, ``192.168.1.0``, …, ``192.168.1.255``,
…, ``192.168.255.255``. Make a list of which IP Addresses did connect, as these are the hosts on their
private network.

------------------------------------------------------------
Task 3: Port scan discovered hosts
------------------------------------------------------------

Now you're going to find what TCP services are running on a machine on the FTP Server's private network.
Namely on ``192.168.56.102``. To do this, you'll want to detect successful vs unsuccessful openings of the
data connection.

Use the code from ``python3 examples/remote_port.py`` to access port ``22`` on ``192.168.56.102``, where SSH
will be running. Note down the final response you get. Then try a random high port (e.g. 34989) and see what
the response is when nothing is on that port.

Now go try this for all ports from 1 to 65,535. Try searching what those port numbers correspond to, if
anything. You can also use the ``RETR`` command to read anything the service outputs upon connecting into
a file on the FTP server.

You should start to sense how you discover what is running, and get to look for options for attack.

------------------------------------------------------------
Task 4: Exfiltrate data from a private FTP server
------------------------------------------------------------

For our next task we want to retrieve secret files from this network's private FTP server. You may have
noticed in Task 3 that there's an FTP server running on port 21 of ``192.168.56.102``. If you try
``nc 192.168.56.102 21`` you'll find you can't connect from your own computer. But you've found that
``192.168.56.101`` can.

Here's the trick: you can send the contents of a file to the FTP server on port 21 of ``192.168.56.102`` and
it'll interpret each line of the contents as a command. So you can tell it to do things. Like send you their
secret weapon blueprints.

`Conclusion → <conclusion.html>`_
