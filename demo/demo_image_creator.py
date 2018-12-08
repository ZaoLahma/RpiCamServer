class DemoImageCreator:
  @staticmethod
  def create_color_image(file_name, resolution, data):
    max_val = max(data)
    with open(file_name, 'w') as image_file:
      image_file.write('P6 {0} {1} {2}\n'.format(resolution[0], resolution[1], max_val))

    with open(file_name, 'ab') as image_file:
      image_file.write(data)