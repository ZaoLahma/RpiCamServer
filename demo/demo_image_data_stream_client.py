from threading import Thread
import demo_nw_if

class DemoImageDataStreamClient(Thread):
  def __init__(self, server_socket):
    Thread.__init__(self)
    self.server_socket = server_socket
    self.active = False
    self.image_data = None

  def run(self):
    self.active = True
    while self.active:
      self.image_data = demo_nw_if.DemoNwIf.receive_data(self.server_socket)
    print("DemoImageDataStreamClient stopped")

  def get_image(self):
    return self.image_data

  def stop(self):
    self.active = False
    self.server_socket.close()