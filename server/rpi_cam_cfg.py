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
    self.cfg_file_path = os.path.join(curr_path, self.CFG_FILE_PATH)
    with open(self.cfg_file_path) as json_file:
      json_contents = json_file.readlines()
    json_contents = ''.join(json_contents)
    self.config = json.loads(json_contents)

  def get_config_val(self, config_identifier):
    config_val = None
    try:
      config_val = self.config['config'][config_identifier]['value']
    except KeyError:
      expression = "config_identifier = {0}".format(config_identifier)
      message = "Config identifier not found in configuration"
      raise RpiCamCfgInvalidCfgKeyException(expression, message)
    print("{0} set to {1}".format(config_identifier, config_val))
    return config_val

  def set_config(self, config):
    response = {'config' : {}}
    for config_item in config.keys():
      response['config'].update(self.set_config_val(config_item, config[config_item]))
    return response

  def set_config_val(self, config_identifier, config_val):
    expected_data_type = self.config['config'][config_identifier]['type']

    print('expected_data_type {0}'.format(expected_data_type))

    if 'int' == expected_data_type:
      try:
         config_val = int(config_val)
         print('Could create int from {0}'.format(config_val))
      except:
        return {config_identifier : 'NOK - {0} not an integer'.format(config_val)}
    elif 'bool' == expected_data_type:
      if config_val != 'true' and config_val != 'false':
        return {config_identifier : 'Not true or false'}
    
    self.config['config'][config_identifier]['value'] = str(config_val)
    with open(self.cfg_file_path, 'w') as json_file:
      json.dump(self.config, json_file)
    print("Set {0} to {1}".format(config_identifier, config_val))  
    return {config_identifier : 'OK'}