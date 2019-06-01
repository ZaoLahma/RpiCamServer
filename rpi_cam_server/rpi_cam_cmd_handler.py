class RpiCamCmdHandler:
  def __init__(self):
    print('RpiCamCmdHandler ready to handle commands')
    self.commands = {}

  def handle_commands(self, commands):
    print('commands {0}'.format(commands))
    response = {'commands' : {}}
    for command in commands:
      command_name = command['command']
      args = None
      try:
        args = command['args']
      except:
        args = None
      response['commands'].update(self.handle_command(command_name, args))
    return response

  def handle_command(self, command, args):
    print('handle_command {0}'.format(command))
    response = {command : {}}
    try:
      handlers = self.commands[command]
      for handler in handlers:
        response[command].update(handler(command, args))
    except:
      print('Failed to find handler for command. Registered commands {0}'.format(self.commands))
      response[command].update({"result" : "NOK - Command not recognized"})
    return response

  def register_command(self, command, handler):
    try:
      self.commands[command]
    except:
      self.commands[command] = []
    self.commands[command].append(handler)