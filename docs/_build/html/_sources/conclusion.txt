.. _ref_conclusion:

============================================================
Conclusion
============================================================

As you've seen, a single vulnerability can let an attacker hop straight into an unprotected network. There
are many discovered every year, and those looking hardest for them are those who want to keep them secret to
use them. In addition, spearfishing (sending employees fake emails that seem completely legitimate) is often
used to get software onto employee's workstations.

The approach must be to assume attackers will get onto your network and plan how you'll make their life more difficult, detect them and defend against them once they do.

------------------------------------------------------------
Learning from this Exercise
------------------------------------------------------------

A public FTP server is a little less common these days, but there might be a role for it. But you could have
prevented the issue by:

* Keeping FTP up-to-date with security patches.
* Automated vulnerability scanning.
* Isolating the public FTP server so that it cannot connect to anything else on your network.

You want to make clear divides in your network. Your webservers need read access to their databases, and some write access. But your public webservers don't (or shouldn't) need access to your company's Research & Development.

Think of the, "employees do not have access to the vault," signs banks have? The employees don't have keys to open the vault because anyone could walk in with a shotgun, or get a lightly-vetted job there and steal the contents one afternoon. Similarly you don't want someone to steal an employee's laptop at a conference and then download all your corporate blueprints.

The key way to separate these things is Screened Subnets. This is where you have a different IP ranges for the webservers to the Human Resources PCs to the corporate file stores, and any communication between them is subject to strict rules. This is the network example of having a one-way hatch for depositing money down a chute.

* Scanning the private network of the FTP server should have shown (at most) the other public webservers and nothing more important than that.

The aim cannot be to keep attackers out of the entire network. Resourced attackers or those good at spearfishing will undoubtedly get inside your network. But you can try to separate different aspects of your network, to make an attacker's job much more difficult and give you a chance to spot them. Unlike a vulnerable FTP server sending someone on the Internet your secret blueprints.
