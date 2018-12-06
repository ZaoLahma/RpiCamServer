import socket
import rpi_cam_api_client_handler
import json

class RpiCamApi():
  def __init__(self, config, service_discovery):
    print('RpiCamApi starting')
    self.config = config
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
        print('RpiCamApi::__handle_new_connections: Connected to by ' + str(address))
        self.client_handlers.append(client_handler)

  def handle_client_request(self, client_handler, request):
    req_string = request.decode('utf-8')
    print('Received request {0} from client {1}'.format(req_string, client_handler.client_id))
    json_object = json.loads(req_string)
    print('json_object {0}'.format(json_object))
    req_types = json_object.keys()
    for req_type in req_types:
      print('req_type {0}'.format(req_type))
      if 'config' == req_type:
        self.config.set_config(json_object[req_type])
      elif 'command' == req_type:
        print("Command received")

  def runnable(self):
    self.__handle_new_connections()
