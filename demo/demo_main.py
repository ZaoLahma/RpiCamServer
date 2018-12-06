import demo_service_discover
import demo_api

class DemoMain:
  @staticmethod
  def main():
    print('Demo main called')
    api_service = 4440
    api_ip_address = demo_service_discover.DemoServiceDiscover.find_service(api_service)
    api_socket = demo_api.DemoApi.connect((api_ip_address, api_service))

    api_test_string = '{ "request" : { "config" : { "api_port_no" : "4440" } } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_response = demo_api.DemoApi.receive_response(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    api_test_string = '{ "request" : { "config" : { "api_port_no" : "this3434shouldfail" } } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_response = demo_api.DemoApi.receive_response(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))
    
    api_test_string = '{ "request" : { "config" : { "image_data_port_no" : "3070" }, "commands" : [ "kill_server_process" ] } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_socket.close()

if __name__ == '__main__':
  print('Demo starting')
  DemoMain.main()