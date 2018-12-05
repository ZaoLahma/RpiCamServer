import demo_service_discover
import demo_api

class DemoMain:
  @staticmethod
  def main():
    print("Demo main called")
    api_service = 4440
    api_ip_address = demo_service_discover.DemoServiceDiscover.find_service(api_service)
    demo_api.DemoApi.send_command((api_ip_address, api_service), '{ "config" : { "api_port_no" : 4440 } }')

if __name__ == "__main__":
  print("Demo starting")
  DemoMain.main()