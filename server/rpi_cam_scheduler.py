class RpiCamScheduler:
  def __init__(self, cmd_handler):
    cmd_handler.register_command('kill_server_process', self.stop)
    self.active = False
    self.runnables = []

  def register_runnable(self, runnable):
    self.runnables.append(runnable)

  def stop(self):
    self.active = False
    self.runnables = []
    return True

  def run(self):
    self.active = True
    while self.active:
      for runnable in self.runnables:
        runnable()