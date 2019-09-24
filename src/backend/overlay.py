from PIL import Image, ImageDraw
import numpy as np

def overlay(rasp_id, imagePath, heatLayers):
    #[
    #  {
    #    top: 0
    #    left: 0
    #    radiusH: 0
    #    radiusV: 0
    #    level: 0.0
    #  }
    #]
    map = Image.open(imagePath)
    map_mat = np.array(map)

    dist_mat = map_mat * 1.0

    for heatLayer in heatLayers:
        heat = Image.new('RGB', (map.size[0], map.size[1]), (0, 0, 0))
        draw = ImageDraw.Draw(heat)
        draw.ellipse((heatLayer["left"]-heatLayer["radiusV"], heatLayer["top"]-heatLayer["radiusH"], heatLayer["left"] + heatLayer["radiusV"], heatLayer["top"]+heatLayer["radiusH"]), fill=(0, 255, 255))
        heat_mat = np.array(heat)
        dist_mat -= heat_mat * float(heatLayer["level"])

    Image.fromarray(dist_mat.clip(0, 255).astype(np.uint8)).save('static/tempfiles/output_'+str(rasp_id)+'.jpg', quality=95)
