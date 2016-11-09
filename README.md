# Network Scanning Practical: Setup

## Requirements for this CyberPractical

* Requires `nmap` and `nc` (netcat) to be accessible to students.
* Requires several (virtual) hosts to be configured.
  * Students need to be able to scan `192.168.56.101`.
    * At least FTP, SSH, HTTP and HTTPS should be listening.
    * The FTP service **must** be the specially modified [ProFTPD 1.3.x-CYBERPRACTICALS](https://github.com/46bit/ftpbounce-proftpd). With any other modern FTP Server, Exercise 2's exploit will not work.
  * `192.168.56.101` should be connected to a private network.
    * `192.168.56.102` should be on that private network. Ideally have a few services running but not FTP.
    * `192.168.56.103` should be on that private netowrk. Ideally have just FTP running - again this **must** be the specially modified [ProFTPD 1.3.x-CYBERPRACTICALS](https://github.com/46bit/ftpbounce-proftpd). This server must have `notes/secret_blueprints.txt` saved in `~student` and readable by the `student` user.

The most self-contained way to achieve this would be having a few linux containers running on the main CyberPracticals VM. `192.168.56.101` would be that VM. The other hosts would be linux containers on an internal network. VMs will use a lot more disk space and configuration but will work exactly the same otherwise.

**If these IP Addresses are changed**, then you must update the Docuemntation and the various scripts in `ftp/*.py` and `ftp/examples/*.py`.

## Setup on the CyberPracticals VM

### Python Package Installation

```
pip3 install cp_ftp/
```

### Documentation

The built documentation is in `docs/_build/html`. If you've changed the IP addresses, make sure to update
them as detailed above and rebuild the documentation.

## Authorship

Built in August 2016 by [Michael Mokrysz](https://46b.it).
