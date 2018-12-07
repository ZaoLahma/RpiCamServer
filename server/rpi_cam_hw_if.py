try:
    import picamera
except ImportError:
    print("Not running on RPI - Using PiCamera stub")
    import rpi_cam_picamera_stub as picamera

import io

class RpiCamHwIf:
  def __init__(self, config, cmd_handler, nwIf):
    cmd_handler.register_command('start_streaming', self.start)
    cmd_handler.register_command('stop_streaming', self.stop)
    cmd_handler.register_command('capture_image', self.capture_image)
    self.config = config
    self.nwIf = nwIf
    self.camera = picamera.PiCamera()
    self.__init_internal()
    self.active = False

  def __init_internal(self):
    self.camera.resolution = (int(self.config.get_config_val('image_x_res')), int(self.config.get_config_val('image_y_res')))
    self.camera.rotation = int(self.config.get_config_val('image_rotation'))
    self.image_format = self.config.get_config_val('image_format')

  def __capture_and_send_image(self, use_video_port=True):
    currImage = io.BytesIO()
    self.camera.capture(currImage, self.image_format, use_video_port=use_video_port)
    self.nwIf.send(bytearray(currImage.getvalue()))

  def capture_image(self):
    if self.active == False:
      self.__init_internal()
      self.__capture_and_send_image(False)
      return {"RpiCamHwIf" : "OK"}
    else:
      return {"RpiCamHwIf" : "NOK - Command not handled in current state"}

  def start(self):
    self.active = True
    return {"{0}".format("RpiCamHwIf") : "OK"}

  def stop(self):
    self.active = False
    return {"{0}".format("RpiCamHwIf") : "OK"}

  def runnable(self):
      if self.active:
        self.__capture_and_send_image()

  