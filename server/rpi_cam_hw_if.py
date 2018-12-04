try:
    import picamera
except ImportError:
    print("Not running on RPI - Using PiCamera stub")
    import rpi_cam_picamera_stub as picamera

import io

class RpiCamHwIf:
  def __init__(self, nwIf, resolution, image_format, rotation):
    self.nwIf = nwIf
    self.camera = picamera.PiCamera()
    self.camera.resolution = resolution
    self.camera.rotation = rotation
    self.image_format = image_format

  def runnable(self):
      currImage = io.BytesIO()
      xRes = self.camera.resolution[0]
      yRes = self.camera.resolution[1]
      currImage.write(xRes.to_bytes(2, byteorder='little'))
      currImage.write(yRes.to_bytes(2, byteorder='little'))
      self.camera.capture(currImage, self.image_format, use_video_port=True)
      self.nwIf.send(bytearray(currImage.getvalue()))

  