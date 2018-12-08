import tkinter

#This is a very simple image viewer that would 
#need to be implemented using something quicker
#than tkinter
class DemoImageViewer:
  def __init__(self, resolution):
    self.resolution = resolution
    self.root = tkinter.Tk()
    self.frame = tkinter.Frame(self.root)
    self.frame.pack()

    self.bottomframe = tkinter.Frame(self.root)
    self.bottomframe.pack(side = tkinter.BOTTOM)

    self.canvas = tkinter.Canvas(self.frame, width=self.resolution[0], height=self.resolution[1], bg="#000000")
    self.canvas.pack( side = tkinter.TOP )
    self.image = tkinter.PhotoImage(width=self.resolution[0], height=self.resolution[1])
    self.canvas.create_image((self.resolution[0]/2, self.resolution[1]/2), image=self.image, state="normal")

    self.root.resizable(False, False)
    self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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
    self.image.put(''.join(hex_image), to=(0, 0, self.resolution[0], self.resolution[1]))

  def on_close(self):
    self.root.destroy()
    self.active = False

  def main_loop(self):
    self.root.mainloop()