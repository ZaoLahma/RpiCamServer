import socket
from . import rpi_cam_api_client_handler
import json

class RpiCamApi():
  def __init__(self, config, cmd_handler, service_discovery):
    cmd_handler.register_command('kill_server_process', self.kill_server_process)
    self.active = False
    self.config = config
    self.cmd_handler = cmd_handler
    self.service_discovery = service_discovery
    self.start()

  def __init_internal(self):
    print('RpiCamApi starting')
    self.portNo = int(self.config.get_config_val('api_port_no'))
    self.service_discovery.add_service(self.portNo)
    self.requests = []
    self.client_handlers = []
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serverSocket.bind(('', self.portNo))
    self.serverSocket.settimeout(0.001)
    self.active = True

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

  def start(self):
    self.__init_internal()

  def kill_server_process(self, command, args):
    response = {"debug" : "RpiCamApi called"}
    self.active = False
    for client_handler in self.client_handlers:
      client_handler.stop()
    self.connections = []
    response['result'] = "OK"
    return response

  def handle_client_request(self, client_handler, request):
    req_string = request.decode('utf-8')
    print('Received request {0} from client {1}'.format(req_string, client_handler.client_id))
    json_object = json.loads(req_string)
    response = {'response' : {}}
    disconnect = False
    if 'disconnect' == json_object['request']:
      disconnect = True
      response['response'] = { json_object['request'] : {}}
      response['response'][json_object['request']] = {'result' : 'OK'}
    else:
      req_types = json_object['request'].keys()
      for req_type in req_types:
        print('req_type {0}'.format(req_type))
        response['response'].update(self.cmd_handler.handle_commands(json_object['request'][req_type]))
    print('before dumps')
    response = json.dumps(response)
    print('after dumps')

    try:
      client_handler.send(response.encode('utf-8'))
      if "True" == self.config.get_config_val('api_is_stateless') or disconnect:
        client_handler.stop()
        self.remove_client_handler(client_handler)
    except Exception as e:
      print('Error when sending response to client: {0}'.encode(e))
      self.remove_client_handler(client_handler)

  def remove_client_handler(self, client_handler):
    try:
      self.client_handlers.remove(client_handler)
    except Exception as e:
      print("Could not remove client_handler {0}".format(e))

  def runnable(self):
    if self.active:
      self.__handle_new_connections()
