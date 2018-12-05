import socket

class RpiCamStreamNwIf:
  def __init__(self, config, service_discovery):
    self.portNo = config.get_config_val('image_data_port_no')
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serverSocket.bind(('', self.portNo))
    self.serverSocket.settimeout(0.001)
    self.connections = []
    service_discovery.add_service(self.portNo)

  def __handle_new_connections(self):
    try:
        self.serverSocket.listen(1)
        (connection, address) = self.serverSocket.accept()
    except socket.timeout:
        pass
    except:
        raise
    else:
        print("RpiCamStreamNwIf::__handle_new_connections: Connected to by " + str(address))
        self.connections.append((connection, address))

  def runnable(self):
    self.__handle_new_connections()

  def send(self, data):
    for connection in self.connections:
      try:
        dataSize = (len(data)).to_bytes(4, byteorder='little')
        connection[0].sendall(dataSize)
        connection[0].sendall(data)
      except Exception as e:
        print("Disconnecting connection due to: " + str(e))
        self.connections.remove(connection)