# RpiCamServer
A TCP server that allows transmission of pixel data from the Raspberry Pi camera to the local network. It currently supports fetching individual images, as well as sending a stream of images over the local network.

The demo project serves as an API description for now. Might put more effort into a better description later.

How to run the demo project:
<br><b>python3 rpi_cam_main.py</b>
<br><b>python3 demo_main.py</b>

The rpi_cam_main.py needs to be running before the demo_main.py is started.

The RpiCamServer has a camera stub built into it, so for testing purposes it doesn't need to be running on the Raspberry Pi hardware. If no real camera is attached, it will (slowly!) generate random pixel values that are pushed to the image interface.

TODO:
A simple GUI for the demo project
