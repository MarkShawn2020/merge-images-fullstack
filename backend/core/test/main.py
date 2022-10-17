import os
import pathlib
import re
from PIL import Image
from core.img_merge import merge_imgs

ALLOWED_IMG_SUFFIX = [".tiff", ".png", ".jpg"]

working_dir = "/Users/mark/Pictures/微信精选/平成狸合战/极乐之船"
drops = [
    # 1, 3, 4, 5, 6, 7, 8, 10
]

dir_name = os.path.basename(working_dir)
output_dir = os.path.join(working_dir, "output")
output_path = os.path.join(output_dir, dir_name + ".jpg")

print("input dir: " + working_dir)
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
print("output path: " + output_path)

imgs = []
crops = []

img_names = sorted([i for i in os.listdir(working_dir) if pathlib.Path(i).suffix in ALLOWED_IMG_SUFFIX],
                   key=lambda x: int(re.search(r'\d+', x).group()))

UNIT = 5
END = 91


def get_crop_y(img_name):
    if "-" not in img_name:
        return (0, END)
    elif "--" in img_name:
        return (END - UNIT * 2, END)
    return (END - UNIT, END)


for index, img_name in enumerate(img_names):
    print("INCLUDING file: " + img_name)
    img_path = os.path.join(working_dir, img_name)
    imgs.append(Image.open(img_path))
    crops.append(get_crop_y(img_name))

img = merge_imgs(imgs, crops)
img.save(output_path)
# img.show()
print("finished")
