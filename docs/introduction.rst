.. _ref_introduction:

============================================================
Introduction
============================================================

This exercise is going to give a basic introduction to Network Security.

Network Scanning is the task of finding running services and hosts on a network.
In casual parlance, "what computers are connected to this router and what do they
seem to do?"

Attackers commonly perform it to understand private networks they have intruded onto.
Network Engineers also use it, to understand their own networks and fix problems before
Attackers can use them.

This practical teaches how to perform network scanning with commonly-used tools, how
to abuse services to act as private network scanners, and the mindsets to build
defendable services and networks.

To begin with here's a *basic* refresher on TCP networking.

------------------------------------------------------------
Ports
------------------------------------------------------------

At one time computers ran a single program at a time. That program had complete access to everything included to the computer, including any links to other computers. Any data received from a network would be passed to that single program.

Those days are long gone: modern computers are often running dozens of different programs that want internet access at the same time. This is called *multitasking*. Sharing one internet connection between them is a challenge: how do you decide which program should get which received data?

**Port numbers** are used to solve this problem. Each network packet includes a destination port number. A program that wants to communicate asks the Operating System if it can listen to a particular 16-bit numbered port. If no program is listening on that port, the Operating System allows it and starts forwarding packets with that port number to the program.

This is remarkably useful. It also presents an issue when you're trying to secure a computer system: how do you check if all the programs listening on the network are secure enough to be allowed to do so? From the attacker's point of view the same checks can be used to identify potentially vulnerable services to attack.

------------------------------------------------------------
Services
------------------------------------------------------------

In the decades since multitasking arrived, engineers have tried to standardise how you do particular things across a network. There is massive technical complexity in how networks function, and without some standardisation it would impossible to keep the Internet in one piece.

************************************************************
Example: opening a webpage
************************************************************

One example of this is opening `http://www.york.ac.uk/` in your browser.

* **DNS**: Your Operating System uses the DNS protocol to map the domain name `www.york.ac.uk` into the IP Address `144.32.128.115`. Lower levels of the networking stack can use this IP Address to send packets to and from the York server.
* **HTTP**: Your web browser now asks port `80` on `144.32.128.115` for that webpage. The request is phrased according to the HTTP protocol, which looks like this::

    GET / HTTP/1.1
    Host: www.york.ac.uk
    […]

  A webserver program on the computer at `144.32.128.115` is listening on port `80`. This is the default port the HTTP protocol specifies. It receives that message and replies according to the HTTP protocol.::

      HTTP/1.1 200 OK
      Date: Wed, 10 Aug 2016 11:26:18 GMT
      […]
      <!doctype html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>University of York</title>
      […]

Within a fraction of a second you're looking at the University of York website, thanks to decades of engineers and protocol authors designing services that work well together.

Here's some common services we'll see later:

* **Remote login**: FTP (port 21), SSH (port 22), Telnet (port 23)
  These are protocols designed for remotely administering servers. Generally they'll ask for a user+password combination for the server, or something to that effect like using a cryptographic key.
* **Web servers**: HTTP (port 80), HTTPS (port 443)
  These are protocols for serving webpages.
* **DNS** (port 53): used to resolve domain names like `york.ac.uk` or `tumblr.com` into a 32-bit or 128-bit value that network routers can use to route your packets.
* **NTP** (port 123): used to keep your computer's clock syncronised with online atomic clocks.

------------------------------------------------------------
Network Scanning
------------------------------------------------------------

You're the administrator of your personal computer. You own it and you configure it however you like. But
most people know nothing about networks or computer security. Even a lot of programmers know very little
about how networks work. As such your Operating System needs to keep your computer safe through secure
default settings: running few or no services and having a firewall up.

But this wouldn't work so well for a server you administer. If you need an FTP service and a HTTP service,
then you have to try and manage the risks. If it's only for people inside your company you could restrict
connections to the local network - but this can be worked around by an attacker, as we'll explore later.

**You need to firewall the things you don't want people connecting to (like a terrible chess program you wrote last week) and expose things that people need to use (like a webserver).**

------------

**Let's start performing network scanning:** :ref:`ref_exercise1`
