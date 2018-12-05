import rpi_cam_hw_if
import rpi_cam_scheduler
import rpi_cam_stream_nw_if
import rpi_cam_service_discovery
import rpi_cam_cfg
import rpi_cam_api

class Main:
  @staticmethod
  def main():
    print('RpiCamServer starting')

    config = rpi_cam_cfg.RpiCamCfg()

    service_discovery = rpi_cam_service_discovery.RpiCamServiceDiscovery(config)
    nwIf = rpi_cam_stream_nw_if.RpiCamStreamNwIf(config, service_discovery)
    camera = rpi_cam_hw_if.RpiCamHwIf(config, nwIf)
    api = rpi_cam_api.RpiCamApi(config, service_discovery)

    scheduler = rpi_cam_scheduler.RpiCamScheduler()
    scheduler.register_runnable(camera.runnable)
    scheduler.register_runnable(nwIf.runnable)
    scheduler.register_runnable(service_discovery.runnable)
    scheduler.register_runnable(api.runnable)
    scheduler.run()

if __name__ == "__main__":
  Main.main()