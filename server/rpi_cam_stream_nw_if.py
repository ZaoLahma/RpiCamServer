import socket
import rpi_cam_nw_tl

class RpiCamStreamNwIf:
  def __init__(self, config, service_discovery):
    self.config = config
    self.service_discovery = service_discovery
    self.connections = []
    self.active = False

  def __handle_new_connections(self):
    try:
        self.server_socket.listen(1)
        (connection, address) = self.server_socket.accept()
    except socket.timeout:
        pass
    except:
        raise
    else:
        print("RpiCamStreamNwIf::__handle_new_connections: Connected to by " + str(address))
        self.connections.append((connection, address))

  def runnable(self):
    if self.active:
      self.__handle_new_connections()

  def __init_internal(self):
    self.portNo = self.config.get_config_val('image_data_port_no')
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind(('', self.portNo))
    self.server_socket.settimeout(0.001)
    self.service_discovery.add_service(self.portNo)

  def start(self):
    self.__init_internal()
    self.active = True

  def stop(self):
    self.active = False
    for connection in self.connections:
      connection[0].close
    self.connections = []

  def send(self, data):
    for connection in self.connections:
      try:
        rpi_cam_nw_tl.RpiCamNwTL.send_data(data, connection[0])
      except Exception as e:
        print('Closing connection due to {0}'.format(e))
        self.connections.remove(connection)