# Network scanning practical

Computers connected to networks have to be defended. For home PCs they often refuse all incoming traffic that isn't for a connection they opened. This is the networking equivalent of not opening the door for someone you didn't invite around.

For servers the situation is a little different. Your favourite website exists to serve anyone who happens to connect to it. The servers can't ignore your HTTP requests. The server is probably in a datacentre building somewhere, with backup power supplies and really good quality internet, so the webmaster needs a way to connect to it.

## Ports

At one time computers ran a single program at a time. That program had complete access to everything included to the computer, including any links to other computers. Any data received from a network would be passed to that single program.

Those days are long gone: modern computers are often running dozens of different programs that want internet access at the same time. This is called *multitasking*. Sharing one internet connection between them is a challenge: how do you decide which program should get which received data?

**Port numbers** are used to solve this problem. Each network packet includes a destination port number. A program that wants to communicate asks the Operating System if it can listen to a particular 16-bit numbered port. If no program is listening on that port, the Operating System allows it and starts forwarding packets with that port number to the program.

This is remarkably useful. It also presents an issue when you're trying to secure a computer system: how do you check if all the programs listening on the network are secure enough to be allowed to do so? From the attacker's point of view the same checks can be used to identify potentially vulnerable services to attack.

## Services

In the decades since multitasking arrived, engineers have tried to standardise how you do particular things across a network. There is massive technical complexity in how networks function, and without some standardisation it would impossible to keep the Internet in one piece. 

> ### Example: opening a webpage
> 
> One example of this is opening `http://www.york.ac.uk/` in your browser.
> 
> * **DNS**: Your Operating System uses the DNS protocol to map the domain name `www.york.ac.uk` into the IP Address `144.32.128.115`. Lower levels of the networking stack can use this IP Address to send packets to and from the York server.
> * **HTTP**: Your web browser now asks port `80` on `144.32.128.115` for that webpage. The request is phrased according to the HTTP protocol, which looks like this:
> 
> ```
> GET / HTTP/1.1
> Host: www.york.ac.uk
> […]
> ```
> 
> A webserver program on the computer at `144.32.128.115` is listening on port `80`. This is the default port the HTTP protocol specifies. It receives that message and replies according to the HTTP protocol.
> 
> ```
> HTTP/1.1 200 OK
> Date: Wed, 10 Aug 2016 11:26:18 GMT
> […]
> <!doctype html>
> <html lang="en">
>
> <head>
>   <meta charset="UTF-8">
>   <title>University of York</title>
> […]
> ```
> 
> Within a fraction of a second you're looking at the University of York website, thanks to decades of engineers and protocol authors designing services that work well together.

Here's some common services we'll see later:

* **Remote login**: FTP (port 21), SSH (port 22), Telnet (port 23)
  These are protocols designed for remotely administering servers. Generally they'll ask for a user+password combination for the server, or something to that effect like using a cryptographic key.
* **Web servers**: HTTP (port 80), HTTPS (port 443)
  These are protocols for serving webpages.
* **DNS** (port 53): used to resolve domain names like `york.ac.uk` or `tumblr.com` into a 32-bit or 128-bit value that network routers can use to route your packets.
* **NTP** (port 123): used to keep your computer's clock syncronised with online atomic clocks.

## Network scanning

You're the administrator of your personal computer. You own it and you configure it however you like. But most people don't know anything about networks or computer security. Their operating systems need to be able to keep themselves safe rather than relying on the user. So they use firewalls: these are designed to only forward packets to listening programs if those programs requested the packets. This is a basic way to make your computer harder to attack.

But if you administer a server for your company or community, you probably want people to be able to get webpages or copy files to and from it. You can't ignore requests people send. So a firewall that drops all incoming requests isn't such a great idea.

**You need to firewall the things you don't want people connecting to (like a terrible chess program you wrote last week) and expose things that people need to use (like a webserver).** How to go about this?

### Task 1: Finding running services

Open **[46b.it](http://46b.it)** in your browser. This connects to that server with the HTTP and HTTPS protocols. So those services are running.

Now open a shell prompt. and try `ssh 46b.it`. You'll find it asks you to accept a key fingerprint but then (provided my security settings are right) you get `Permission denied (publickey).` So the SSH protocol is running as well. This is a way to administer a server remotely.

But are you going to try all 65,535 services by hand? Nope. That's what programs are for! Let's use one called **nmap**. Run `nmap 46b.it`:

``` sh
$ nmap 46b.it
Nmap scan report for 46b.it (104.236.192.168)
PORT     STATE    SERVICE
22/tcp   open     ssh           # ooh, SSH
25/tcp   filtered smtp          # ever used `ping`?
80/tcp   open     http          # ooh, HTTP
443/tcp  open     https         # ooh, HTTPS
[...]
```

This gives a nice list of which ports seem to have a program listening to them. Finding out what ports are being listened upon is an essential step in securing a server. Checking for any vulnerable services is also a common first step in attacking a server.

**Remember: running this against a server you don't control or across a network you don't control is not necessarily legal.** Don't do it.

### Task 2: Examining running services

A lot of the services we use have only a few widely-used implementations. Security problems in them are constantly being discovered and patched, and if you find a years-old version running you might be able to use a well-known attack against it.

You might also find relatively unknown programs running, ones that have never even considered security. Case in point: embedded systems, which can range from tiny chips in adapters to huge routers. They tend to have management or debugging programs, which were hopefully disabled before getting sent to customers. In practice companies often neglect security, as they're unlikely to pay the price down the line for it.

Take another look at the `nmap` results for the virtual machine and see what you can find. Try running `telnet IP_ADDRESS PORT`. Can you find anything interesting? Look up shell commands for deleting files and try them. Look up shell commands for printing out files and try them.

This example is artificial but you do find things almost this bad in the real-world. Even in real industrial facilities. Poor industrial security has been attacked in practice, to destroy Iranian centrifuges (Stuxnet) or a German blast furnace.

## Network defence

The basics are to find and plug holes **before** you deploy systems and **before** someone else uses the problem against you.

**Programs and systems have security bugs**. Every available service will be scanned and attacked by bots. So ideally we only make available services that *have* to be accessible and that are well-vetted.

Keeping services to only be available within your network limits an attacker. They need some sort of foothold in your organisation to even start attacking the firewalled services. This could be a hacked printer, a malicious employee, or an infected PC. These are all quite plausible but you've constrained the opportunities for attack.

### Hunt for problems before you deploy - and fix them!

**Scan for problems yourself.**
Before you make something available to the internet, `nmap` it and check which services are listening. Check the critical ones are configured securely. Firewall noncritical ones to only be accessible to the necessary network users. Disable unnecessary ones.

### Task 3: Disable insecure services

``` sh
ssh root@IP_ADDRESS
sudo systemctl disable 
```

### Task 3: Setup `iptables`, a Linux Firewall
