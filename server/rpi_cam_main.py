import rpi_cam_hw_if
import rpi_cam_scheduler
import rpi_cam_nw_if
import rpi_cam_service_discovery
import rpi_cam_cfg

class Main:
  @staticmethod
  def main():
    print('RpiCamServer starting')

    config = rpi_cam_cfg.RpiCamCfg()

    image_data_port_no = config.get_config('image_data_port_no')
    nwIf = rpi_cam_nw_if.RpiCamNwIf(image_data_port_no)

    service_discovery_active = config.get_config('service_discovery_active')
    service_discovery = None
    if service_discovery_active:
      listener_port = config.get_config('service_discovery_listener_port')
      service_discovery_header = config.get_config('service_discovery_header')
      service_discovery = rpi_cam_service_discovery.RpiCamServiceDiscovery(listener_port, image_data_port_no, service_discovery_header)

    image_resolution = (config.get_config('image_x_res'), config.get_config('image_y_res'))
    image_format = config.get_config('image_format')
    image_rotation = config.get_config('image_rotation')
    camera = rpi_cam_hw_if.RpiCamHwIf(nwIf, image_resolution, image_format, image_rotation)

    scheduler = rpi_cam_scheduler.RpiCamScheduler()
    scheduler.register_runnable(camera.runnable)
    scheduler.register_runnable(nwIf.runnable)
    if service_discovery_active:
      scheduler.register_runnable(service_discovery.runnable)
    scheduler.run()

if __name__ == "__main__":
  Main.main()