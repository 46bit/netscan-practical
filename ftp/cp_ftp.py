import os, sys, socket, time, collections
from socket import _GLOBAL_DEFAULT_TIMEOUT

__all__ = ["FTP"]

# The standard FTP server control port
FTP_PORT = 21
# The sizehint parameter passed to readline() calls
MAXLINE = 8192

# Exception raised when an error or invalid response is received
class Error(Exception): pass

all_errors = (Error)

# Line terminators (we always output CRLF, but accept any of CRLF, CR, LF)
CRLF = '\r\n'

FTPResponseTuple = collections.namedtuple('FTPResponse', 'code text')

class FTP:
  debugging = False
  host = ''
  port = FTP_PORT
  maxline = MAXLINE
  sock = None
  file = None
  welcome = None
  encoding = "latin-1"
  data_address = None
  data_sock = None
  data_file = None

  def __init__(self, host, port=FTP_PORT, debug=False):
    self.debugging = debug
    self.connect(host, port)

  def connect(self, host, port=FTP_PORT):
    self.host = host
    self.port = FTP_PORT

    self.sock = socket.create_connection((self.host, self.port))
    # IPv6 seems to use something other than PORT. It's easier to stick with IPv4 in this hurry.
    assert self.sock.family == socket.AF_INET

    self.file = self.sock.makefile("r", encoding=self.encoding)
    self.welcome = self.recv_response()

  def send_command(self, command):
    if self.debugging:
      print(" [COMMAND] %s" % command)
    line = command + CRLF
    self.sock.sendall(line.encode(self.encoding))

  def recv_response(self):
    line = self.file.readline(self.maxline + 1)
    if len(line) > self.maxline:
      raise Error("got more than %d bytes" % self.maxline)
    if not line:
      raise EOFError
    if line[-2:] == CRLF:
      line = line[:-2]
    elif line[-1:] in CRLF:
      line = line[:-1]

    if self.debugging:
      # \n to break up output
      print("[RESPONSE] %s\n" % line)
    code = int(line[:3])
    return FTPResponseTuple(code, line)

  def send_login_commands(self, user, password=''):
    self.send_command("USER %s" % user)
    resp = self.recv_response()
    if 400 <= resp.code: return resp

    if 300 <= resp.code <= 399:
      self.send_command("PASS %s" % password)
      resp = self.recv_response()

    return resp

  def send_port_command(self, address):
    address_bytes = address[0].split(".")
    port_bytes = [repr(address[1] // 256), repr(address[1] % 256)]
    bytes = address_bytes + port_bytes
    self.send_command("PORT %s" % ",".join(bytes))

  def new_data_address(self):
    if self.data_sock:
      data_sock = self.data_sock
      self.data_sock = None
      if data_sock is not None:
        data_sock.close()

    self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.data_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.data_sock.bind((self.sock.getsockname()[0], 0))
    self.data_address = self.data_sock.getsockname()
    self.data_sock.listen(1)
    return self.data_address

  def recv_data(self):
    if self.data_address is None:
      raise Error("No data address set. Are you trying to receive data from a foreign data connection?")
    conn, addr = self.data_sock.accept()

    data = []
    while True:
        data_segment = conn.recv(8192)
        if not data_segment: break
        data.append(data_segment)
    #conn.shutdown(1)
    conn.close()
    data = ''.join(data)

    if self.debugging:
      sys.stdout.write("[DATA FOLLOWS]\n%s" % data)
      sys.stdout.flush()
    return data

  def close(self):
    self.send_command("QUIT")

    data_sock = self.data_sock
    self.data_sock = None
    if data_sock is not None:
      data_sock.close()

    try:
      file = self.file
      self.file = None
      if file is not None:
        file.close()
    finally:
      sock = self.sock
      self.sock = None
      if sock is not None:
        sock.close()

if __name__ == "__main__":
  ftp = FTP("192.168.56.101", debug=True)
  ftp.send_login_commands("student", "golyeeHug6")
  print("")

  data_address = ftp.new_data_address()
  ftp.send_port_command(data_address)
  ftp.recv_response()
  print("")

  ftp.send_command("LIST")
  ftp.recv_response()
  ftp.recv_data()
  ftp.recv_response()
  print("")

  data_address = ftp.new_data_address()
  ftp.send_port_command(data_address)
  ftp.recv_response()
  print("")

  ftp.send_command("RETR example.txt")
  ftp.recv_response()
  ftp.recv_data()
  ftp.recv_response()
  print("")

  ftp.close()

  ######################

  ftp = FTP("192.168.56.101", debug=True)
  ftp.send_login_commands("student", "golyeeHug6")
  print("")

  target_address = ("192.168.56.102", 21)
  ftp.send_port_command(target_address)
  ftp.recv_response()
  print("")

  ftp.send_command("LIST")
  ftp.recv_response()
  ftp.recv_response()
  print("")

  ftp.send_command("RETR example.txt")
  ftp.recv_response()
  ftp.recv_response()
  print("")

  ftp.close()

  ######################
