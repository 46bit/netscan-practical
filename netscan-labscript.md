# Network scanning practical

Computers connected to networks have to be defended. For home PCs they often refuse all incoming traffic that isn't for a connection they opened. This is the networking equivalent of not opening the door for someone you didn't invite around.

For servers the situation is a little different. Your favourite website exists to serve anyone who happens to connect to it. The servers can't ignore your HTTP requests. The server is probably in a datacentre building somewhere, with backup power supplies and really good quality internet, so the webmaster needs a way to connect to it.

## Services

> ### Ports
> 
> When your computer gets some data from the network, how does it decide which program it is for? The Operating System has no idea what the content of it is, just some basic headers.
> 
> Turns out those headers include a **Port Number**, between 0 and 65536. When you start a program that wants to receive data, it asks the Operating System for a particular number. Then when the OS gets a packet of data, it forwards it to the program *listening* on that port (or discards it if one isn't.)

Over time people have devised different protocols for different things you want to do. These are standards that specify how programs should interact over the network for a particular design. 

For instance if you want to log in to a server you probably need to send a username and password - but it needs specifying what those packets look like and how they get encrypted.

Here's some common services we'll see later:

* **Remote login**: FTP (port 21), SSH (port 22), Telnet (port 23)
  These are protocols designed for remotely administering servers. Generally they'll ask for a user+password combination for the server, or something to that effect like using a cryptographic key.
* **Web servers**: HTTP (port 80), HTTPS (port 443)
  These are protocols for serving webpages.
* Many, many other services.

## The attacker mindset

### Task 1: Finding running services

Open **[46b.it](http://46b.it)** in your browser. At first it's an ordinary HTTP connection, which redirects to a HTTPS one. So you know both of those are running.

Open a shell prompt. and try `ssh 46b.it`. You'll find it asks you to accept a key fingerprint but then (provided my security settings are right) you get `Permission denied (publickey).` So SSH is running as well.

But are you going to try every possible service? Nope. A program could do that for us. Let's use one called **nmap**. Run `nmap 46b.it`:

``` sh
$ nmap 46b.it
Nmap scan report for 46b.it (104.236.192.168)
PORT     STATE    SERVICE
22/tcp   open     ssh				# ooh, SSH
25/tcp   filtered smtp
80/tcp   open     http				# ooh, HTTP
443/tcp  open     https				# ooh, HTTPS
[...]
```

Ooh. A neat list of what's running. Remember as always that running this against a server you don't control or across a network you don't control may be illegal.

### Task 2: Real-world issues with systems

Embedded Systems are often not built with the greatest care for security. We'll examine a virtual (but quite realistic) one now.

The first task is seeing what you can find. Try nmapping it on `192.168.59.1`. Do you spot something new on a high-numbered port?

Try connecting to it: `telnet localhost:PORT_HERE`. Notice anything interesting? This is something you really do find on embedded devices, even ones deployed in real industrial facilities. 

### Why do we care?

In this example, our Steel Furnace just got wrecked because a little microcontroller responsible for turning off the heater was told to `rm -rf /*`.

**Programs and systems have security bugs**. Every available service will be scanned and attacked at some point by bots. So ideally we only want to make available things that *have* to be accessible and that are well-vetted.

Keeping services to only be available within your network limits an attacker. They need some sort of foothold in your organisation to even start attacking the firewalled services. This could be a hacked printer, a malicious employee, or an infected PC. These are all quite plausible but you've constrained the opportunities for attack.

## Prevention

### Hunt for problems before you deploy - and fix them!

**Scan for problems yourself.**
Before you make something available to the internet, `nmap` it and check which services are listening. Check the critical ones are configured securely. Firewall noncritical ones to only be accessible to the necessary network users. Disable unnecessary ones.

### Task 3: Disable insecure services

### Task 3: Setup `iptables`, a Linux Firewall
