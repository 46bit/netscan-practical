# Network Scanning Practical: Setup

## Requirements for this CyberPractical

* Requires `nmap` and `nc` (netcat) to be accessible to students.
* Requires several (virtual) hosts to be configured.
  * Students need to be able to scan `192.168.56.101`.
    * At least FTP, SSH, HTTP and HTTPS should be listening.
    * The FTP service **must** be the specially modified [ProFTPD 1.3.x-CYBERPRACTICALS](https://git.cs.york.ac.uk/cyber-practicals/proftpd). With any other modern FTP Server, Exercise 2's exploit will not work.
  * `192.168.56.101` should be connected to a private network.
    * `192.168.56.102` should be on that private network. Ideally have a few services running but not FTP.
    * `192.168.56.103` should be on that private netowrk. Ideally have just FTP running - again this **must** be the specially modified [ProFTPD 1.3.x-CYBERPRACTICALS](https://git.cs.york.ac.uk/cyber-practicals/proftpd). This server must have `notes/secret_blueprints.txt` saved in `~student` and readable by the `student` user.

The most self-contained way to achieve this would be having a few linux containers running on the main CyberPracticals VM. `192.168.56.101` would be that VM. The other hosts would be linux containers on an internal network. VMs will use a lot more disk space and configuration but will work exactly the same otherwise.

**If these IP Addresses are changed**, then you must update the Docuemntation and the various scripts in `ftp/*.py` and `ftp/examples/*.py`.

## Setup on the CyberPracticals VM

### Python Package Installation
```
pip3 install cp_ftp/
```

### Run the documentation server
```
./run.sh
```

Leave this running in the background. `CTRL+C` will kill it and all the child processes when you're done.

## Get started
Go to [The Documentation](http://localhost:3000).
