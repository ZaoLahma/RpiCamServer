class RpiCamCmdHandler:
  def __init__(self):
    print('RpiCamCmdHandler ready to handle commands')
    self.commands = {}

  def handle_commands(self, commands):
    response = {'commands' : {}}
    for command in commands:
      response['commands'].update(self.handle_command(command))
    return response

  def handle_command(self, command):
    print('handle_command {0}'.format(command))
    response = {command : {}}
    try:
      handlers = self.commands[command]
      for handler in handlers:
        response[command].update(handler())
    except:
      response[command].update({"result" : "NOK - Command not recognized"})
    return response

  def register_command(self, command, handler):
    try:
      self.commands[command]
    except:
      self.commands[command] = []
    self.commands[command].append(handler)