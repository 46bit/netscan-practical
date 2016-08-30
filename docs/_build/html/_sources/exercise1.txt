.. _ref_exercise1:

============================================================
Exercise 1: Scanning servers
============================================================

The internet is a public network. Billions of computers are connected in one form or another. We can try
connecting to any port on any IP address. But home routers and companies usually have their own
internal, private network. We can only connect to IP addresses and ports on a private network by going
through a router configured to allow that.

The first exercise will be learning how to see what services are accessible on an Internet server. In the
Introduction I explained what ports are, and we're going to connect to port 1, 2, …, 65535 to see which are
listening.

------------------------------------------------------------
Task 1: Manually with netcat
------------------------------------------------------------

We'd like to connect to each port in turn, and see if our connection is successful, is rejected, or times
out. A successful connection tells us a service is listening on that port, and often the service sends you
its name when you open the connection. A rejected connection is immediately closed, which commonly means a
firewall in place. A connection that times out is either firewalled or nothing was listening on that port.

We can use netcat to open a connection to a chosen IP address and port, then see what comes back ::

    # Connect over TCP to 192.168.56.103 port 22 (notated as 192.168.56.103:22).
    # netcat is often called nc
    $ nc 192.168.56.103 22
    SSH-2.0-OpenSSH_6.7p1 Debian-5+deb8u2

    # You'll want to Ctrl+C to exit now

So there's an SSH server running on ``22``. You could run this by hand for every port 1, 2, …, 65535. But
that's going to take a lot of your time. Let's use an automated scanner instead.

------------------------------------------------------------
Task 2: Automated port scanning with ``nmap``
------------------------------------------------------------

``nmap`` is an automated scanning tool. It's engineered to scan networks and servers quickly, but has a lot
of options to throttle it and for different sorts of scanning. We're going to use a very simple mode for now
- the ``nmap`` equivalent of performing Task 1 by hand for every port. ::

    $ nmap 192.168.56.103
    Starting Nmap 7.12 ( https://nmap.org ) at 2016-08-30 12:05 BST
    Nmap scan report for 192.168.56.103
    Host is up (0.0017s latency).
    Not shown: 996 closed ports
    PORT    STATE SERVICE
    21/tcp  open  ftp
    22/tcp  open  ssh
    80/tcp  open  http
    443/tcp open  https

    Nmap done: 1 IP address (1 host up) scanned in 0.09 seconds

Port 80 (HTTP) and 443 (HTTPS) are a webserver. Port 22 is SSH, used for logging into a shell remotely.
But Port 21 is FTP, which is used for sharing files. In the next exercise we'll learn how services can be
used to access private networks!
