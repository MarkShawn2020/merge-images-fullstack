from PIL import Image
import numpy as np
from typing import Dict, List

import os

DEFAULT_CAPTAIN_PCTS = [45, 80, 55, 95]
DEFAULT_DENSITY_THREAD = 0.1


def _get_ratio(img: Image.Image, pcts: List[float]) -> float:
    w, h = img.size
    # reference: python 图片二值化处理（处理后为纯黑白的图片）_大蛇王的博客-CSDN博客_python二值化, https://blog.csdn.net/t8116189520/article/details/80271804
    mask = [0] * 200 + [1] * 56
    img = img.crop((w/100*pcts[0], h/100*pcts[1],
                   w/100*pcts[2], h/100*pcts[3])).convert("L").point(mask, "1")
    # 对偏白的图片检测效果还不够好，要想这个算法准确度高，还得提高对文字的区分度，比如单连通面积等，测例：/Users/mark/Pictures/截图/马男/超长的书名/截屏2021-12-11 下午2.57.20.png
    #    for test!
    # img.show()
    arr = np.array(img)
    arr.size
    ratio = arr.sum() / arr.size
    return ratio


def get_captain_lines(img: Image.Image, pcts: List[float] = DEFAULT_CAPTAIN_PCTS,
                      density_thread: int = DEFAULT_DENSITY_THREAD) -> dict:
    """[推测图片中字幕的行数]

    Args:
        img (Image): [description]
        pcts (List[float], optional): [左上右下的切割百分比，用于定位图片中的字幕位置，建议尽量居中密集]. Defaults to DEFAULT_PCTS.

    Returns:
        float: [description]
    """
    x1, y1, x2, y2 = pcts
    y_mean = (y1 + y2) / 2
    # print(f'inferring captain lines, size": {img.size}, "pcts": {pcts}')
    r1 = _get_ratio(img, [x1, y1, x2, y_mean])
    r2 = _get_ratio(img, [x1, y_mean, x2, y2])

    l1 = (int)(r1 > density_thread)
    l2 = (int)(r2 > density_thread)
    # 只有上行没有下行，这存在的概率很小
    assert not (l1 and not l2)
    lines = l1 + l2

    return {"r1": r1, "r2": r2, "lines": lines, "thread": density_thread}


if __name__ == "__main__":
    SAMPLE_DIR = "/Users/mark/Projects/merge_imgs/backend/img_captain/test/samples"
    imgs = [Image.open(os.path.join(SAMPLE_DIR, i))
            for i in sorted(os.listdir(SAMPLE_DIR))[-1:]]
    for img in imgs:
        print(get_captain_lines(img))
