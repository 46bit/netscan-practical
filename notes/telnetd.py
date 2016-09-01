import socket, threading, os, sys, subprocess

port = 7890 if len(sys.argv) < 2 else int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))
s.listen(1)
print("TELNETD port=%d" % port)

welcome_message = 'Welcome to MUD\n1. Go west\n2. Open a window\n3. Quit\n'

welcome = '''
SYSTEM DEBUG INTERFACE
Authorised engineers only
'''

class daemon(threading.Thread):
  def __init__(self, socket_accept):
    threading.Thread.__init__(self)
    socket, address = socket_accept
    self.socket = socket
    self.address = address

  def run(self):
    print("(Client)")

    # display welcome message
    self.socket.send(bytes(welcome, "utf-8"))

    while(True):
      self.socket.send(bytes("> ", "utf-8"))

      # wait for keypress + enter
      data = str(self.socket.recv(1024)[:-2], "utf-8")
      print(".")
      if data == "quit": break

      try:
        output = subprocess.check_output(data, stderr=subprocess.STDOUT, shell=True)
        result = str(output, "utf-8")
      except subprocess.CalledProcessError as e:
        result = "(return code %d) %s" % (e.returncode, str(e.output, "utf-8"))
      except OSError as e:
        result = "(oserror %s)\n" % str(e, "utf-8")

      self.socket.send(bytes(result, "utf-8"))

    self.socket.close()

while True:
  daemon(s.accept()).start()
