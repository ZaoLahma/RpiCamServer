import socket
import struct

class DemoNwIf:
  @staticmethod
  def connect(host):
    api_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      api_socket.connect(host)
    except:
      raise
    else:
      print("Connected to API at address {0}".format(host))
    return api_socket

  @staticmethod
  def send_command(api_socket, command):
    #Protocol is 4 bytes size and then a json string. Hence we send the command_size first
    command_size = (len(command)).to_bytes(4, byteorder='little')
    api_socket.sendall(command_size)
    print('Sending command {0}'.format(command))
    api_socket.sendall(command.encode('utf-8'))

  @staticmethod
  def receive_blocking(socket, num_bytes):
    data = []
    while (len(data) < num_bytes):
      try:
        packet = socket.recv(num_bytes - len(data))
        if not packet:
          continue
        data += packet
      except OSError:
        break
      except socket.timeout:
        pass
    return bytearray(data)

  @staticmethod
  def receive_data(socket):
    header_size = 4
    header = DemoNwIf.receive_blocking(socket, header_size)
    data_size = bytearray(header[0:4])
    try:
      data_size = struct.unpack("<L", data_size)[0]
      data = DemoNwIf.receive_blocking(socket, data_size)
    except:
      return None
    return data
