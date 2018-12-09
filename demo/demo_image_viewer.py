import tkinter
from threading import Thread
from threading import Condition

class DemoImageInjector(Thread):
  def __init__(self, image_viewer, stream_client):
    Thread.__init__(self)
    self.image_viewer = image_viewer
    self.stream_client = stream_client
    self.active = False
    self.start()

  def run(self):
    self.active = True
    self.stream_client.start()
    while self.active:
      image_data = self.stream_client.get_image()
      if self.active and None != image_data:
        self.image_viewer.show_image(image_data)
    print("DemoImageInjector stopped")

  def stop(self):
    self.active = False
    self.stream_client.stop()

#This is a very simple image viewer that would 
#need to be implemented using something quicker
#than tkinter
class DemoImageViewer():
  def __init__(self, resolution):
    self.resolution = resolution
    self.root = tkinter.Tk()
    self.frame = tkinter.Frame(self.root)
    self.frame.pack()

    self.canvas = tkinter.Canvas(self.frame, width=self.resolution[0], height=self.resolution[1], bg="#000000")
    self.canvas.pack( side = tkinter.TOP )
    self.image = tkinter.PhotoImage(width=self.resolution[0], height=self.resolution[1])
    self.canvas.create_image((self.resolution[0]/2, self.resolution[1]/2), image=self.image, state="normal")

    self.root.resizable(False, False)
    self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    self.image_injector = None
    self.active = True

  def show_image(self, image):
    byte_offset = 0
    x = 0
    y = 0
    R = 0
    G = 0
    B = 0
    hex_image = []
    hex_row = []
    hex_row.append('{')
    for byte in image:
      if 0 == byte_offset:
          R = byte
      elif 1 == byte_offset:
          G = byte
      elif 2 == byte_offset:
          B = byte
      byte_offset += 1
      if 3 == byte_offset:
        byte_offset = 0
        hex_row.append("#%02x%02x%02x " % (R, G, B))
        x += 1
        if x == self.resolution[0]:
          hex_row.append('}')
          hex_image.append(''.join(hex_row))
          hex_row = []
          hex_row.append(' {')
          x = 0
          y += 1
    if self.active and not self.image == None:
      self.image.put(''.join(hex_image), to=(0, 0, self.resolution[0], self.resolution[1]))


  def start_streaming(self, stream_client):
    self.bottomframe = tkinter.Frame(self.root)
    self.bottomframe.pack(side = tkinter.BOTTOM)
    self.stop_streaming = tkinter.Button(self.bottomframe, text="Stop streaming", fg="black", command=self.stop)
    self.stop_streaming.pack( side = tkinter.BOTTOM)    
    self.image_injector = DemoImageInjector(self, stream_client)

  def stop(self):
    self.image = None
    if None != self.image_injector:
      self.image_injector.stop()
      #self.image_injector.join()
    self.active = False

  def on_close(self):
    self.stop()
    self.root.destroy()

  def main_loop(self):
    self.root.mainloop()