import random

class PiCameraStubException(Exception):
  pass

class PiCameraStubImageFormatException(PiCameraStubException):
  def __init__(self, expression, message):
    self.expression = expression
    self.message = message

class PiCamera:
  def __init__(self):
    print("Creating a PiCamera stub")
    self.resolution = (0, 0)
    self.rotation = 0

  def __getRandomColorVal(self):
    return random.randint(0, 255).to_bytes(1, byteorder='little')

  def capture(self, buffer, image_format, use_video_port):
    for _ in range(0, (self.resolution[0] * self.resolution[1])):
      if 'rgb' == image_format:
        buffer.write(self.__getRandomColorVal())
        buffer.write(self.__getRandomColorVal())
        buffer.write(self.__getRandomColorVal())
      else:
        expression = "image_format = {0}".format(image_format)
        raise PiCameraStubImageFormatException(expression, "Image format not supported by the PiCamera stub")
