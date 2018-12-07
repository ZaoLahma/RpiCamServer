import demo_service_discover
import demo_api
import json

class DemoMain:
  @staticmethod
  def main():
    print('Demo main called')

    #Find the API service on the local network
    api_service = 4440
    api_ip_address = demo_service_discover.DemoServiceDiscover.find_service(api_service)
    api_socket = demo_api.DemoApi.connect((api_ip_address, api_service))

    #Request update of configuration api_port_no and image_format
    api_test_string = '{ "request" : { "config" : { "api_port_no" : "4440" , "image_format" : "rgb" } } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_response = demo_api.DemoApi.receive_response(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Setting an integer configuration parameter to something other than integer should fail
    api_test_string = '{ "request" : { "config" : { "api_port_no" : "this3434shouldfail" } } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_response = demo_api.DemoApi.receive_response(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Request the configuration
    api_test_string = '{ "request" : { "commands" : [ "get_config" ] } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_response = demo_api.DemoApi.receive_response(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Let's find the image_data_port_no
    config = json.loads(api_response)
    image_data_port_no = config['response']['commands']['get_config']['config']['image_data_port_no']

    #Two valid commands followed by two invalid
    api_test_string = '{ "request" : { "commands" : [ "capture_image", "start_streaming", "thisshouldfail", "anotherfailcommand" ] } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_response = demo_api.DemoApi.receive_response(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Requesting a capture_image now should fail as the streaming service is active
    api_test_string = '{ "request" : { "commands" : [ "capture_image" ] } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    api_response = demo_api.DemoApi.receive_response(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Last request shows a combination of a config request followed by a kill of the server process
    api_test_string = '{ "request" : { "config" : { "image_data_port_no" : "3070" }, "commands" : [ "kill_server_process" ] } }'
    demo_api.DemoApi.send_command(api_socket, api_test_string)
    #We won't get a response from a kill_server_process request. Close the socket.
    api_socket.close()

if __name__ == '__main__':
  print('Demo starting')
  DemoMain.main()