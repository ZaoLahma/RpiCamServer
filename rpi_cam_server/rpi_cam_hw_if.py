import base64

try:
    import picamera
except ImportError:
    print("Not running on RPI - Using PiCamera stub")
    from . import rpi_cam_picamera_stub as picamera

import io

class RpiCamHwIf:
  def __init__(self, config, cmd_handler, nwIf):
    cmd_handler.register_command('start_streaming', self.start)
    cmd_handler.register_command('stop_streaming', self.stop)
    cmd_handler.register_command('capture_image_async', self.capture_image_async)
    cmd_handler.register_command('capture_image_sync', self.capture_image_sync)
    self.config = config
    self.nwIf = nwIf
    self.camera = picamera.PiCamera()
    self.__init_internal()
    self.active = False

  def __init_internal(self):
    self.camera.resolution = (int(self.config.get_config_val('image_x_res')), int(self.config.get_config_val('image_y_res')))
    self.camera.rotation = int(self.config.get_config_val('image_rotation'))
    self.image_format = self.config.get_config_val('image_format')
  
  def __capture_image(self, use_video_port=True):
    curr_image = io.BytesIO()
    self.camera.capture(curr_image, self.image_format, use_video_port=use_video_port)
    return bytearray(curr_image.getvalue())

  def __capture_and_send_image(self, use_video_port=True):
    image_data = self.__capture_image(use_video_port)
    self.nwIf.send(image_data)

  def capture_image_async(self, command, args):
    response = {"debug" : "RpiCamHwIf called"}
    if self.active == False:
      self.__init_internal()
      self.__capture_and_send_image(False)
      response['result'] = "OK"
    else:
      response['result'] = "NOK - Command not handled in current state"
    return response

  def capture_image_sync(self, command, args):
    print('capture_image_sync')
    response = {"debug" : "RpiCamHwIf called"}
    if self.active == False:
      self.__init_internal()
      image_data = self.__capture_image(False)
      image_data = base64.b64encode(image_data).decode('utf-8')
      response['result'] = "OK"
      response['image_data'] = image_data
    else:
      response['result'] = "NOK - Command not handled in current state"
    return response

  def start(self, command, args):
    response = {"RpiCamHwIf" : "Called"}
    self.active = True
    response['result'] = "OK"
    return response

  def stop(self, command, args):
    self.active = False
    return {"{0}".format("RpiCamHwIf") : "OK"}

  def runnable(self):
      if self.active:
        self.__capture_and_send_image()

  