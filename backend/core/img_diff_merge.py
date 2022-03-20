from typing import List, Tuple
from backend.core.img_compress import compress_img
from backend.core.img_captain import get_captain_lines
from backend.core.img_diff import get_hashes, get_diffs_bool, get_diffs_int
from backend.core.img_merge import merge_imgs
from PIL import Image
import os
import re

from backend.settings import OUTPUT_DIR, VALID_IMG_TYPES, DEFAULT_BODY_PCTS, DEFAULT_DIFF_THREAD, DEFAULT_CAPTAIN_PCTS


def get_crop(img: Image, diff: bool, captain_pcts=DEFAULT_CAPTAIN_PCTS, body_pcts=DEFAULT_BODY_PCTS) \
        -> Tuple[float, float]:
    if diff:
        return body_pcts[1], body_pcts[3]
    captain_info = get_captain_lines(img, captain_pcts)
    print({"captain": captain_info})
    if captain_info["lines"] == 0:
        return body_pcts[1], body_pcts[3]
    y_mean = (captain_pcts[1] + captain_pcts[3]) / 2
    if captain_info["lines"] == 1:
        return y_mean, captain_pcts[3]
    else:
        return captain_pcts[1], captain_pcts[3]


def get_crops(imgs: List[Image.Image]) -> Image.Image:
    diff_thread = DEFAULT_DIFF_THREAD
    hashes = get_hashes(imgs)
    diffs = get_diffs_int(hashes)
    diffs_bool = get_diffs_bool(diffs, diff_thread)
    print({"diffs": diffs, "diffs_bool": diffs_bool, "diff_thread": diff_thread})

    crops = [get_crop(imgs[i], diffs_bool[i]) for i in range(len(imgs))]
    print({"crops": crops})
    return crops


def merge_imgs_of_dir(imgs_dir_path: str):
    print("merging imgs of dir: " + imgs_dir_path)
    imgs_dir_name = os.path.basename(imgs_dir_path)
    output_img_name = imgs_dir_name + ".png"

    print("reading imgs")
    imgs = [Image.open(os.path.join(imgs_dir_path, i))
            for i in sorted(os.listdir(imgs_dir_path)) if re.search("|".join(VALID_IMG_TYPES), i)]

    print("getting crops")
    crops = get_crops(imgs)

    print("merging img")
    final_img = merge_imgs(imgs, crops)

    print("compressing img")
    final_img = compress_img(final_img)

    print("saving img")
    final_img.save(os.path.join(OUTPUT_DIR, output_img_name))

    print("finished!")


if __name__ == "__main__":
    choice = 1
    if choice == 0:
        IMGS_ROOT_PATH = "/Users/mark/Pictures/截图/马男"
        for sub_dir_name in os.listdir(IMGS_ROOT_PATH):
            sub_dir_path = os.path.join(IMGS_ROOT_PATH, sub_dir_name)
            if os.path.isdir(sub_dir_path):
                merge_imgs_of_dir(sub_dir_path)
    elif choice == 1:
        IMGS_DIR_PATH = "/Users/mark/Pictures/截图/马男/关于未来，看到与想要"
        merge_imgs_of_dir(IMGS_DIR_PATH)
