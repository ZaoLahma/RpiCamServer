import json
import os.path

class RpiCamCfgException(Exception):
  pass

class RpiCamCfgInvalidCfgKeyException(RpiCamCfgException):
  def __init__(self, expression, message):
    self.expression = expression
    self.message = message

class RpiCamCfg:
  CFG_FILE_PATH = './config/rpi_cam_cfg.json'
  def __init__(self):
    curr_path = os.path.abspath(os.path.dirname(__file__))
    json_contents = None
    cfg_file_path = os.path.join(curr_path, self.CFG_FILE_PATH)
    with open(cfg_file_path) as json_file:
      json_contents = json_file.readlines()
    json_contents = ''.join(json_contents)
    self.config = json.loads(json_contents)

  def get_config(self, config_identifier):
    config_val = None
    try:
      config_val = self.config[config_identifier]
    except KeyError:
      expression = "config_identifier = {0}".format(config_identifier)
      message = "Config identifier not found in configuration"
      raise RpiCamCfgInvalidCfgKeyException(expression, message)
    return config_val