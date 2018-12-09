class DemoImageCreator:
  @staticmethod
  def create_color_image(file_name, resolution, data, write_file=True):
    max_val = max(data)
    header = 'P6 %u %u %u\n' % (resolution[0], resolution[1], max_val)
    header = header.encode()
    ppm_data = bytearray(header)
    ppm_data.extend(data)

    if write_file:
      with open(file_name, 'wb') as image_file:
        image_file.write(ppm_data)

    return ppm_data