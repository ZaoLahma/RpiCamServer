# RpiCamServer
A TCP server that allows transmission of pixel data from the Raspberry Pi camera to the local network. It currently supports fetching individual images, as well as sending a stream of images over the local network. The communication towards the RpiCamServer is done through a json interface.

## Documentation
The demo_main.py in the demo project serves as an API description for now. Might put more effort into better documentation later.

## How to run the demo project
The rpi_cam_main.py needs to be running before the demo_main.py is started. The demo acts as a client to the server.

### Get the project
`git clone https://github.com/ZaoLahma/RpiCamServer.git`

### Start the server
```
cd RpiCamServer
python3 rpi_cam_main.py
```
### Start the demo
```
cd RpiCamServer
cd demo
python3 demo_main.py
```

### Non Raspberry Pi testing
The RpiCamServer has a camera stub built into it, so for testing purposes it doesn't need to be running on the Raspberry Pi hardware. This means the server and demo project can be executed on the same machine. In this case the server will (slowly!) generate random pixel values that are pushed to the image interface to the demo project.

# Known issues
The server will sometimes fail to parse the json properly.
The json API is in need of refinement and will change in the future.
