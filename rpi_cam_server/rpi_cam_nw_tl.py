import struct

class RpiCamNwTL:
  @staticmethod
  def receive_blocking(receiver, socket, num_bytes):
    data = []
    while (len(data) < num_bytes) and receiver.is_active():
      try:
        packet = socket.recv(num_bytes - len(data))
        if not packet:
          continue
        data += packet
      except socket.timeout:
        pass
      except ConnectionResetError:
        break
    return bytearray(data)

  @staticmethod
  def receive_data(receiver, socket):
    header_size = 4
    header = RpiCamNwTL.receive_blocking(receiver, socket, header_size)
    data_size = bytearray(header[0:4])
    data_size = struct.unpack("<L", data_size)[0]
    data = RpiCamNwTL.receive_blocking(receiver, socket, data_size)
    return data

  @staticmethod
  def send_data(socket, data):
    data_size = (len(data)).to_bytes(4, byteorder='little')
    socket.sendall(data_size)
    socket.sendall(data)