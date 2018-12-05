import socket
import rpi_cam_api_client_handler

class RpiCamApi():
  def __init__(self, config, service_discovery):
    print("RpiCamApi starting")
    self.requests = []
    self.client_handlers = []
    self.portNo = config.get_config_val('api_port_no')
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serverSocket.bind(('', self.portNo))
    self.serverSocket.settimeout(0.001)
    service_discovery.add_service(self.portNo)

  def __handle_new_connections(self):
    try:
        self.serverSocket.listen(1)
        (connection, address) = self.serverSocket.accept()
        client_handler = rpi_cam_api_client_handler.RpiCamApiClientHandler(len(self.client_handlers), self, (connection, address))
    except socket.timeout:
        pass
    except:
        raise
    else:
        print("RpiCamApi::__handle_new_connections: Connected to by " + str(address))
        self.client_handlers.append(client_handler)

  def handle_client_request(self, client_handler, request):
    print("Received request {0} from client {1}".format(''.join(map(chr, request)), client_handler.client_id))

  def runnable(self):
    self.__handle_new_connections()
