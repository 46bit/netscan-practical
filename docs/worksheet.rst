### Task 1: Finding running services

Open **[46b.it](http://46b.it)** in your browser. This connects to that server with the HTTP and HTTPS protocols. So those services are running.

Now open a shell prompt. and try `ssh 46b.it`. You'll find it asks you to accept a key fingerprint but then (provided my security settings are right) you get `Permission denied (publickey).` So the SSH protocol is running as well. This is a way to administer a server remotely.

But are you going to try all 65,535 services by hand? Nope. That's what programs are for! Let's use one called **nmap**. Run `nmap 46b.it`::

    $ nmap 46b.it
    Nmap scan report for 46b.it (104.236.192.168)
    PORT     STATE    SERVICE
    22/tcp   open     ssh           # ooh, SSH
    25/tcp   filtered smtp          # ever used `ping`?
    80/tcp   open     http          # ooh, HTTP
    443/tcp  open     https         # ooh, HTTPS
    [...]

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

::

    ssh root@IP_ADDRESS
    sudo systemctl disable

### Task 3: Setup `iptables`, a Linux Firewall
