.. _ref_ftp_reference:

============================================================
FTP Protocol Reference
============================================================

------------------------------------------------------------
What is FTP?
------------------------------------------------------------

FTP stands for File Transfer Protocol. It dates from 1971 but is still in widespread use. It is used to share
files over the Internet - very much an old version of Dropbox or Google Drive.

FTP uses a Command socket and a Data socket, two independent connections for one FTP 'session.' To open an FTP Session, the FTP Client establishes a command connection by connecting to port 21 on the server. The
FTP Server then replies with a "welcome" message - generally the name and version of the running FTP server.

A lot of things about FTP seem unusual or bizarre now, but the FTP protocol predates HTTP (the protocol
you use to load websites). It was standardised about as we use it here by 1985. As such we have decades
of hindsight to judge it with. That it remains a common service reflects that it is 'good enough' to keep
using it rather than a more modern replacement.

------------------------------------------------------------
Authentication
------------------------------------------------------------

1. The FTP Client now sends a ``USER username_here`` message, to identify the user they wish to log in with.
2. If the username exists, the FTP Server replies with a ``331 Password required for student`` response - again on the Command connection.
3. The FTP Client now sends a ``PASS password_here`` message, givign the user's password.
4. If the username and password check out, the FTP Server responds with ``230 User student logged in``.

+---------+------------------------------------------------------+
|         | Command Messages or (*activity in italics*)          |
+=========+======================================================+
| Client: | (*connects to port 21 on the server*)                |
+---------+------------------------------------------------------+
| Server: | ``220 ProFTPD 1.3.5b Server``                        |
+---------+------------------------------------------------------+
| Client: | ``USER student``                                     |
+---------+------------------------------------------------------+
| Server: | ``331 Password required for student``                |
+---------+------------------------------------------------------+
| Client: | ``PASS golyeeHug6``                                  |
+---------+------------------------------------------------------+
| Server: | ``230 User student logged in``                       |
+---------+------------------------------------------------------+

------------------------------------------------------------
Using the Data Connection
------------------------------------------------------------

I mentioned that there are *two* types of connection in an FTP session. We've seen how the Command connection is used to pass commands and response messages back and forth, but no sign of the Data
Connection. The Data Connection only comes in when performing commands that provide some data beyond just
a status message. If uploading or downloading a file, the file contents go across a Data connection.

I say *a* data connection, because each data connection only carries the data for one command and is then
immediately closed. This is partly due to FTP's age: modern protocols would tend to include the data in
the command connection because it poses fewer problems.

To run a command that needs a data connection, the client first sends a ``PORT X,X,X,X,A,B`` command. The
``X,X,X,X`` encodes an IPv4 Address where the dots are replaced by commas. The ``A,B`` represents the Port to
connect to. Port numbers range from 1 to 65,535 (the range of a 16-bit unsigned integer) and thus the upper
8 bits are encoded as ``A`` and the lower 8 as `B`. Thus the socket ``192.168.1.1:21`` would be encoded as
``PORT 192,168,1,1,0,21``.

The server responds with a `200 PORT command successful` response, but in practice this merely means the
server was able to parse the `PORT` command. The data connection is only opened when the server is to
immediately send data.

The client can now execute a command that outputs data, such as ``LIST`` which lists the current directory.
The server will send a ``150 Opening ASCII mode data connection for file list`` response to indicate the
Data connection is being opened, and then the server will immediately send the data down the Data
connection. Once all the data is sent the server will close the connection and send a final
``226 Transfer complete`` response.

+---------+----------------------------------------------------------+
|         | Command Messages or (*activity in italics*)              |
+=========+==========================================================+
| Client: | (*listens on a random port, say 11240*)                  |
+---------+----------------------------------------------------------+
| Client: | ``PORT 192,168,56,1,43,232``                             |
+---------+----------------------------------------------------------+
| Server: | ``200 PORT command successful``                          |
+---------+----------------------------------------------------------+
| Client: | ``LIST``                                                 |
+---------+----------------------------------------------------------+
| Server: | (*opens a TCP connection to 192.168.56.1:11240*)         |
+---------+----------------------------------------------------------+
| Server: | ``150 Opening ASCII mode data connection for file list`` |
+---------+----------------------------------------------------------+
| Server: | (*sends a listing of the current directory*)             |
+---------+----------------------------------------------------------+
| Client: | (*receives a listing of the current directory*)          |
+---------+----------------------------------------------------------+
| Server: | (*closes the data connection*)                           |
+---------+----------------------------------------------------------+
| Server: | ``226 Transfer complete``                                |
+---------+----------------------------------------------------------+

------------------------------------------------------------
What happens if the Data Connection fails?
------------------------------------------------------------

``200 PORT command successful`` only means the ``PORT`` command was valid. The Server doesn't try to
connect until you ask it to send some data.

+---------+-------------------------------------------------------------+
|         | Command Messages or (*activity in italics*)                 |
+=========+=============================================================+
| Client: | (*doesn't listen on port 11240*)                            |
+---------+-------------------------------------------------------------+
| Client: | ``PORT 192,168,56,1,43,232``                                |
+---------+-------------------------------------------------------------+
| Server: | ``200 PORT command successful``                             |
+---------+-------------------------------------------------------------+
| Client: | ``LIST``                                                    |
+---------+-------------------------------------------------------------+
| Server: | (*fails opening a TCP connection to 192.168.56.1:11240*)    |
+---------+-------------------------------------------------------------+
| Server: | ``425 Unable to build data connection: Connection refused`` |
+---------+-------------------------------------------------------------+
| Server: | ``450 LIST: Connection refused``                            |
+---------+-------------------------------------------------------------+

------------------------------------------------------------
A Short, Incomplete but Useful Command Reference
------------------------------------------------------------

+----------------------+------------------------------------------------------------------------+
| COMMAND              | Description                                                            |
+======================+========================================================================+
| ``PORT w,x,y,z,p,q`` | Set the IPv4 Address and Port for the next data connection.            |
+----------------------+------------------------------------------------------------------------+
| ``LIST``             | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``PWD``              | Print the current working directory                                    |
+----------------------+------------------------------------------------------------------------+
| ``CWD new_path``     | Change the current working directory                                   |
+----------------------+------------------------------------------------------------------------+
| ``RETR filename``    | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``DELE filename``    | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``STOR filename``    | Lists the contents of the current directory                            |
+----------------------+------------------------------------------------------------------------+
| ``QUIT``             | Close the current FTP Session                                          |
+----------------------+------------------------------------------------------------------------+

A completer listing is available `here <https://en.wikipedia.org/wiki/List_of_FTP_commands>`_ but I believe you'll find it confusing, rather than useful, for the following tasks.
