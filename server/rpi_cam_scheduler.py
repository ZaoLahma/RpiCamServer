class RpiCamScheduler:
  def __init__(self):
    self.active = False
    self.runnables = []

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