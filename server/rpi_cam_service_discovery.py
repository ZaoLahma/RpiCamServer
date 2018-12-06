import socket

def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('5.255.255.255', 1))
    IP = s.getsockname()[0]
    s.close()
    return IP

class RpiCamServiceDiscovery:
  def __init__(self, config):
    self.listener_port = int(config.get_config_val('service_discovery_listener_port'))
    self.services = []
    self.own_ip = get_own_ip()
    self.serviceListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.serviceListenerSocket.bind(('224.1.1.1', self.listener_port))
    self.serviceListenerSocket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,
                    socket.inet_aton(self.own_ip))
    self.serviceListenerSocket.setsockopt(socket.SOL_IP,
                                          socket.IP_ADD_MEMBERSHIP,
                                          socket.inet_aton('224.1.1.1') +
                                          socket.inet_aton(self.own_ip))

    self.serviceListenerSocket.settimeout(0.001)

  def __handle_service_discovery_requests(self):
    try:
        request = self.serviceListenerSocket.recvfrom(4096)
    except socket.timeout:
        pass
    except:
        raise
    else:
        print("RpiCamServiceDiscovery::__handle_service_discovery_requests: New service request for " + str(request[0]) + " received from " + str(request[1]))
        req_string = request[0].decode('utf-8')
        requested_port_no = req_string
        if requested_port_no.endswith("\x00"):
            requested_port_no = requested_port_no[:-1]
        service_provided = False
        for service in self.services:
            if int(requested_port_no) == service:
                response = bytearray()
                response.extend(map(ord, self.own_ip))
                response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                response_socket.sendto(response, request[1])
                response_socket.close()
                service_provided = True
                break
        if not service_provided:
            print("Discarded request. Service {0} not provided".format(int(requested_port_no)))

  def add_service(self, service):
      self.services.append(service)
      print("Service {0} published".format(service))

  def runnable(self):
    self.__handle_service_discovery_requests()