import socket

class DemoServiceDiscover:
  @staticmethod
  def find_service(service):
    service_address = None
    data = bytearray()
    address = bytearray()
    data.extend(map(ord, str(service)))
    service_discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    service_discovery_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    service_discovery_socket.sendto(data,  ("224.1.1.1", 3000))
    service_discovery_socket.settimeout(2)
    try:
        address = service_discovery_socket.recv(13)
    except socket.timeout:
        pass
    except:
        raise
    else:
        service_discovery_socket.close()
        service_address = str(address, 'utf-8').split('\x00')
        if len(service_address):
            service_address = service_address[0]
        print("Service {0} found at {1}".format(service, service_address))
    return service_address
    