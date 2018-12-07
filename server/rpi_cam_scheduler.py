class RpiCamScheduler:
  def __init__(self, cmd_handler):
    cmd_handler.register_command('kill_server_process', self)
    self.active = False
    self.runnables = []

  def handle_command(self, command):
    if 'kill_server_process' == command:
      self.stop()
      return True
    return False

  def register_runnable(self, runnable):
    self.runnables.append(runnable)

  def stop(self):
    self.active = False
    self.runnables = []

  def run(self):
    self.active = True
    while self.active:
      for runnable in self.runnables:
        runnable()