.. _ref_exercise2:

============================================================
Exercise 2: Scanning a Private Network
============================================================

In Exercise 1 we scanned a publicly-accessible Internet server (set up solely for this exercise; scanning
real Internet servers you don't control may be illegal). In this Exercise we're going to use its FTP server
to see if that server is on a private network, and try to access services running across the private network.

The original FTP specification allowed for data connections being sent anywhere. However as the Internet
matured this became a security problem.

Back in 1995, the U.S. restricted the export of software using cryptography. The U.S. produced a lot of
software used worldwide, and still does. The aim was to force the rest of the world to use encryption that
the U.S. government could crack. However online open source software might just restrict downloads to U.S.
IP addresses. Much of this software was hosted on FTP servers.

Attention was drawn to FTP Bounce because it would let a foreign server download IP-restricted software by
using a U.S. server as an unwitting proxy.

[DIAGRAM]

This feature also allowed you to access services on the same private network as the FTP Server. You can
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
