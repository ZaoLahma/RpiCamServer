try:
    import picamera
except ImportError:
    print("Not running on RPI - Using PiCamera stub")
    import rpi_cam_picamera_stub as picamera

import io

class RpiCamHwIf:
  def __init__(self, config, nwIf):
    self.nwIf = nwIf
    self.camera = picamera.PiCamera()
    self.camera.resolution = (int(config.get_config_val('image_x_res')), int(config.get_config_val('image_y_res')))
    self.camera.rotation = int(config.get_config_val('image_rotation'))
    self.image_format = config.get_config_val('image_format')

  def runnable(self):
      currImage = io.BytesIO()
      self.camera.capture(currImage, self.image_format, use_video_port=True)
      self.nwIf.send(bytearray(currImage.getvalue()))

  