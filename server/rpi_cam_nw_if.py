import socket

class RpiCamNwIf:
  def __init__(self, portNo):
    self.portNo = portNo
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serverSocket.bind(('', self.portNo))
    self.connections = []

  def __handleNewConnections(self):
    try:
        self.serverSocket.settimeout(0.001)
        self.serverSocket.listen(1)
        (connection, address) = self.serverSocket.accept()
    except socket.timeout:
        pass
    except:
        raise
    else:
        print("RpiCamNwIf::__handleNewConnections: Connected to by " + str(address))
        self.connections.append((connection, address))

  def runnable(self):
    self.__handleNewConnections()

  def send(self, data):
    for connection in self.connections:
      try:
        #print(len(data))
        dataSize = (len(data)).to_bytes(4, byteorder='little')
        connection[0].sendall(dataSize)
        connection[0].sendall(data)
      except Exception as e:
        print("Disconnecting connection due to: " + str(e))
        self.connections.remove(connection)