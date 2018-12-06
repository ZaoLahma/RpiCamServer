class RpiCamCmdHandler:
  def __init__(self, scheduler):
    print('RpiCamCmdHandler ready to handle commands')
    self.actors = []
    self.scheduler = scheduler

  def handle_commands(self, commands):
    for command in commands:
      self.handle_command(command)
    response = {'commands' : "OK"}
    return response

  def handle_command(self, command):
    print('RpiCamCmdHandler::handle_command {0}'.format(command))
    if 'stop' == command:
      for actor in self.actors:
        actor.stop()
    elif 'start' == command:
      for actor in self.actors:
        actor.start()
    elif 'restart' == command:
      self.handle_command('stop')
      self.handle_command('start')
    elif 'kill_server_process' == command:
      self.handle_command('stop')
      self.scheduler.stop()

  def register_actor(self, actor):
    self.actors.append(actor)