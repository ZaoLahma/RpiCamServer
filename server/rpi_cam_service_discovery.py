import socket

def getOwnIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('5.255.255.255', 1))
    IP = s.getsockname()[0]
    s.close()
    return IP

class RpiCamServiceDiscovery:
  def __init__(self, listenerPort, servicePortNo, service_discovery_header):
    self.servicePortNo = servicePortNo
    self.service_discovery_header = service_discovery_header
    self.ownIp = getOwnIp()
    self.serviceListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.serviceListenerSocket.bind(('224.1.1.1', listenerPort))
    self.serviceListenerSocket.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,
                    socket.inet_aton(self.ownIp))
    self.serviceListenerSocket.setsockopt(socket.SOL_IP,
                                          socket.IP_ADD_MEMBERSHIP,
                                          socket.inet_aton('224.1.1.1') +
                                          socket.inet_aton(self.ownIp))

    self.serviceListenerSocket.settimeout(0.001)

  def __handleServiceDiscoveryRequests(self):
    try:
        request = self.serviceListenerSocket.recvfrom(4096)
    except socket.timeout:
        pass
    except:
        raise
    else:
        print("RpiCamServiceDiscovery::__handleServiceDiscoveryRequests: New service request for " + str(request[0]) + " received from " + str(request[1]))
        reqString = str(request[0], 'utf-8')
        if reqString.startswith(self.service_discovery_header):
            splitReqString = str.split(reqString, '_')
            requestedPortNo = splitReqString[2]
            if requestedPortNo.endswith("\x00"):
                requestedPortNo = requestedPortNo[:-1]
            if int(requestedPortNo) == self.servicePortNo:
                response = bytearray()
                response.extend(map(ord, self.ownIp))
                responseSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                responseSocket.sendto(response, request[1])
                responseSocket.close()
            else:
                print("Discarded request. Wrong service")
        else:
            print("Discared request. Wrong header")

  def runnable(self):
    self.__handleServiceDiscoveryRequests()