import rpi_cam_hw_if
import rpi_cam_scheduler
import rpi_cam_nw_if
import rpi_cam_cfg

class Main:
  @staticmethod
  def main():
    print('RpiCamServer starting')

    config = rpi_cam_cfg.RpiCamCfg()

    portNo = config.get_config('app_port_no')
    nwIf = rpi_cam_nw_if.RpiCamNwIf(portNo)

    image_resolution = (config.get_config('image_x_res'), config.get_config('image_y_res'))
    image_format = config.get_config('image_format')
    image_rotation = config.get_config('image_rotation')
    camera = rpi_cam_hw_if.RpiCamHwIf(nwIf, image_resolution, image_format, image_rotation)

    scheduler = rpi_cam_scheduler.RpiCamScheduler()
    scheduler.register_runnable(camera.runnable)
    scheduler.register_runnable(nwIf.runnable)
    scheduler.run()

if __name__ == "__main__":
  Main.main()