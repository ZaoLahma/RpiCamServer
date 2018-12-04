import rpi_cam_if
import rpi_cam_scheduler

class Main:
  @staticmethod
  def main():
    print("RpiCamServer starting")
    camera = rpi_cam_if.RpiCamIf((640, 480), 'rgb', 180)
    scheduler = rpi_cam_scheduler.RpiCamScheduler()
    scheduler.register_runnable(camera.runnable)
    scheduler.run()

if __name__ == "__main__":
  Main.main()