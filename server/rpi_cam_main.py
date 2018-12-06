import rpi_cam_hw_if
import rpi_cam_scheduler
import rpi_cam_stream_nw_if
import rpi_cam_service_discovery
import rpi_cam_cfg
import rpi_cam_api
import rpi_cam_cmd_handler

class Main:
  @staticmethod
  def main():
    print('RpiCamServer starting')

    config = rpi_cam_cfg.RpiCamCfg()

    scheduler = rpi_cam_scheduler.RpiCamScheduler()

    cmd_handler = rpi_cam_cmd_handler.RpiCamCmdHandler(scheduler)

    service_discovery = rpi_cam_service_discovery.RpiCamServiceDiscovery(config)
    stream_nw_if = rpi_cam_stream_nw_if.RpiCamStreamNwIf(config, service_discovery)
    camera = rpi_cam_hw_if.RpiCamHwIf(config, stream_nw_if)
    api = rpi_cam_api.RpiCamApi(config, cmd_handler, service_discovery)

    cmd_handler.register_actor(api)
    cmd_handler.register_actor(stream_nw_if)

    scheduler.register_runnable(camera.runnable)
    scheduler.register_runnable(stream_nw_if.runnable)
    scheduler.register_runnable(service_discovery.runnable)
    scheduler.register_runnable(api.runnable)
    scheduler.run()

if __name__ == "__main__":
  Main.main()