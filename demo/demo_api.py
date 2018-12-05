import socket

class DemoApi:
  @staticmethod
  def send_command(host, command):
    api_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      api_socket.connect(host)
    except:
      raise
    else:
      print("Connected to API at address {0}".format(host))
      command_size = (len(command)).to_bytes(4, byteorder='little')
      api_socket.sendall(command_size)
      api_socket.sendall(command.encode('utf-8'))
    api_socket.close()
    