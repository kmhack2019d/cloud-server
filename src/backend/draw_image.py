from PIL import Image, ImageDraw
import numpy as np

map = Image.open('static/dummy/image.jpg')
map_mat = np.array(map)

dist_mat = map_mat * 1.0

heat = Image.new('RGB', (map.size[0], map.size[1]), (0, 0, 0))
draw = ImageDraw.Draw(heat)
draw.ellipse((150, 150, 350, 350), fill=(0, 255, 255))

heat_mat = np.array(heat)

dist_mat -= heat_mat * float(100000000)

Image.fromarray(dist_mat.clip(0, 255).astype(np.uint8)).save('output.jpg', quality=95)
