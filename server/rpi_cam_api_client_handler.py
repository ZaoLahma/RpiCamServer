from threading import Thread
import socket
import struct

class RpiCamApiClientHandler(Thread):
  def __init__(self, client_id, api, connection):
    Thread.__init__(self)
    self.client_id = client_id
    self.api = api
    self.connection = connection
    self.start()
    self.active = False

  def __receive_blocking(self, numBytes):
      data = []
      while len(data) < numBytes:
          try:
              packet = self.connection[0].recv(numBytes - len(data))
              if not packet:
                  continue
              data += packet
          except socket.timeout:
              pass
      return bytes(data)

  def run(self):
    print("RpiCamApiClientHandler started for client {0}".format(self.client_id))
    self.active = True
    while self.active:
      header_size = 4
      header = self.__receive_blocking(header_size)
      data_size = bytearray(header[0:4])
      data_size = struct.unpack("<L", data_size)[0]
      data = self.__receive_blocking(data_size)
      self.api.handle_client_request(self, data)


  def send(self, data):
    self.connection[0].sendall(data)