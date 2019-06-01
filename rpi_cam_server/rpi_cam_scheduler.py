class RpiCamScheduler:
  def __init__(self, cmd_handler):
    cmd_handler.register_command('kill_server_process', self.kill_server_process)
    self.active = False
    self.runnables = []

  def register_runnable(self, runnable):
    self.runnables.append(runnable)

  def kill_server_process(self, command, args):
    response = {"debug" : "RpiCamScheduler called"}
    response['result'] = "OK"
    self.active = False
    self.runnables = []
    return response

  def run(self):
    self.active = True
    while self.active:
      for runnable in self.runnables:
        runnable()