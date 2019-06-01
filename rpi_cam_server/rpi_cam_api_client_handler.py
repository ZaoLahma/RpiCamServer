from threading import Thread
import socket
import struct
from . import rpi_cam_nw_tl

class RpiCamApiClientHandler(Thread):
  def __init__(self, client_id, api, connection):
    Thread.__init__(self)
    self.client_id = client_id
    self.api = api
    self.connection = connection
    self.start()
    self.active = False

  def run(self):
    print("RpiCamApiClientHandler started for client {0}".format(self.client_id))
    self.active = True
    while self.active:
      try:
        data = rpi_cam_nw_tl.RpiCamNwTL.receive_data(self, self.connection[0])
        self.api.handle_client_request(self, data)
      except Exception as e:
        print('Exception occurred {0}'.format(e))
        self.stop()        
        self.api.remove_client_handler(self)

  def is_active(self):
      return self.active

  def send(self, data):
    try:
      rpi_cam_nw_tl.RpiCamNwTL.send_data(self.connection[0], data)
    except Exception as e:
      self.stop()
      print('Failed to send response to client due to {0}'.format(e))

  def stop(self):
    self.active = False
    self.connection[0].close()
