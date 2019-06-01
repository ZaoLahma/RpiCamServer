import demo_service_discover
import demo_nw_if
import demo_image_viewer
import demo_image_creator
import demo_image_data_stream_client
import base64
import json
import time

class DemoMain:
  @staticmethod
  def main():
    print('Demo main called')

    #Find the API service on the local network
    api_service = 4440
    api_ip_address = demo_service_discover.DemoServiceDiscover.find_service(api_service)

    #Connect to control interface
    api_socket = demo_nw_if.DemoNwIf.connect((api_ip_address, api_service))

    #Request update of configuration api_port_no and image_format
    api_test_string = '{ "request" : { "commands" : [ { "command" : "set_config", "args" : { "api_port_no" : "4440" , "image_format" : "rgb" } } ] } }'

    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Setting an integer configuration parameter to something other than integer should fail
    api_test_string = '{ "request" : { "commands" : [ { "command" : "set_config", "args" : { "api_port_no" : "this3434shouldfail" } } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Request the configuration
    api_test_string = '{ "request" : { "commands" : [ { "command" : "get_config" } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Let's find the image_data_port_no
    config = json.loads(api_response)
    image_data_port_no = int(config['response']['commands']['get_config']['result']['config']['image_data_port_no']['value'])
    
    #Connect to the image_data interface
    data_socket = demo_nw_if.DemoNwIf.connect((api_ip_address, image_data_port_no))
    
    #Lower the image resolution to avoid having to wait forever for the image data
    low_res = (256, 256)
    api_test_string = '{ "request" : { "commands" : [ { "command" : "set_config", "args" : { "image_x_res" : "%u", "image_y_res" : "%u" } } ] } }' % (low_res[0], low_res[1])
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Request an image asynchronously on the data channel
    api_test_string = '{ "request" : { "commands" : [ { "command" : "capture_image_async" } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    #This should typically be done in another thread
    print('Waiting for image data. This might take a while...')
    image_data = demo_nw_if.DemoNwIf.receive_data(data_socket)
    image_file_name = "test.ppm"
    print('Saving image to {0}'.format(image_file_name))
    demo_image_creator.DemoImageCreator.create_color_image(image_file_name, low_res, image_data)
    print('Showing image...')
    demo_viewer = demo_image_viewer.DemoImageViewer(low_res)
    demo_viewer.show_image(image_data)
    demo_viewer.main_loop()
    print('{0} bytes image data received'.format(len(image_data)))
    #Let's check if the server accepted the request
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))
    response = json.loads(api_response)
    result = response['response']['commands']['capture_image_async']['result']
    if "OK" == result:
      print("API reports OK")
    data_socket.close()

    #Request a base64 encoded image synchronously
    api_test_string = '{ "request" : { "commands" : [ { "command" : "capture_image_sync" } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    response = json.loads(api_response)
    result = response['response']['commands']['capture_image_sync']['result']
    if "OK" == result:
      print("API reports OK - decoding image")
      encoded_image_data = response['response']['commands']['capture_image_sync']['image_data']
      image_data = base64.b64decode(encoded_image_data)
      image_file_name = "test.ppm"
      print('Saving image to {0}'.format(image_file_name))
      demo_image_creator.DemoImageCreator.create_color_image(image_file_name, low_res, image_data)
      print('Showing image...')
      demo_viewer = demo_image_viewer.DemoImageViewer(low_res)
      demo_viewer.show_image(image_data)
      demo_viewer.main_loop()

    #One valid command followed by two invalid
    api_test_string = '{ "request" : { "commands" : [ {"command" : "capture_image_async" }, { "command" : "thisshouldfail" }, { "command" : "anotherfailcommand" } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Start streaming images
    data_socket = demo_nw_if.DemoNwIf.connect((api_ip_address, image_data_port_no))
    stream_client = demo_image_data_stream_client.DemoImageDataStreamClient(data_socket)
    demo_viewer = demo_image_viewer.DemoImageViewer(low_res)
    api_test_string = '{ "request" : { "commands" : [ { "command" : "start_streaming" } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))
    response = json.loads(api_response)
    result = response['response']['commands']['start_streaming']['result']
    if "OK" == result:
      print("Opening image stream...")
      demo_viewer.start_streaming(stream_client)
      demo_viewer.main_loop()
    data_socket.close()

    #Requesting a capture_image now should fail as the streaming service is active
    api_test_string = '{ "request" : { "commands" : [ { "command" : "capture_image" } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))

    #Disconnect and reestablish the connection
    api_test_string = '{ "request" : "disconnect" }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    api_response = demo_nw_if.DemoNwIf.receive_data(api_socket).decode('utf-8')
    print('Received response {0}'.format(api_response))
    api_socket.close()
    api_socket = demo_nw_if.DemoNwIf.connect((api_ip_address, api_service))

    #Last request shows a combination of a config request followed by a kill of the server process
    api_test_string = '{ "request" : { "commands" : [ { "command" : "set_config", "args" : { "image_data_port_no" : "3070" } }, { "command" : "stop_streaming" }, { "command" : "kill_server_process" } ] } }'
    demo_nw_if.DemoNwIf.send_command(api_socket, api_test_string)
    #We won't get a response from a kill_server_process request. Close the socket.
    api_socket.close()

if __name__ == '__main__':
  print('Demo starting')
  DemoMain.main()