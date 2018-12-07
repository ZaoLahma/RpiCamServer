class RpiCamCmdHandler:
  def __init__(self):
    print('RpiCamCmdHandler ready to handle commands')
    self.commands = {}

  def handle_commands(self, commands):
    response = {'commands' : {}}
    for command in commands:
      response['commands'].update(self.handle_command_new(command))
    return response

  def handle_command_new(self, command):
    print('handle_command_new {0}'.format(command))
    try:
      handlers = self.commands[command]
      command_valid = True
      for handler in handlers:
        if False == handler():
          command_valid = False
      if True == command_valid:
        return {"{0}".format(command) : "OK"}
      else:
        return {"{0}".format(command) : "NOK - Command not handled in this state"}
    except:
      return {"{0}".format(command) : "NOK - Command not recognized"}

  def register_command(self, command, handler):
    try:
      self.commands[command]
    except:
      self.commands[command] = []
    self.commands[command].append(handler)