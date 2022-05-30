import os
import pathlib
import re
from PIL import Image
from img_merge import merge_imgs

ALLOWED_IMG_SUFFIX = [".tiff", ".png"]

working_dir = "/Users/mark/Pictures/Elmedia Player/少年派的奇幻漂流/风景-我只剩下一具凡身在苦苦支撑"
drops = [
    # 1,2,3,4,5
]

dir_name = os.path.basename(working_dir)
output_dir = os.path.join(working_dir, "output")
output_path = os.path.join(output_dir, dir_name + ".png")

print("input dir: " + working_dir)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
print("output path: " + output_path)

imgs = []
crops = []

img_names = sorted([i for i in os.listdir(working_dir) if pathlib.Path(i).suffix in ALLOWED_IMG_SUFFIX],
                   key=lambda x: int(re.search(r'\d+', x).group()))
for index, img_name in enumerate(img_names):
    print("INCLUDING file: " + img_name)
    img_path = os.path.join(working_dir, img_name)
    imgs.append(Image.open(img_path))
    crops.append((85 if index in drops else 0, 100))

img = merge_imgs(imgs, crops)
img.show()
img.save(output_path)
print("finished")
