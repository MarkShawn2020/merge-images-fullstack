from __future__ import annotations
from typing import List, Tuple
import os
from PIL import Image, ImageChops

BoxType = Tuple[int, int, int, int]


class ImgBox:
    def __init__(self) -> None:
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

    def get_box(self) -> BoxType:
        """返回图片裁剪四角的绝对坐标（上左下右）
        """
        return (self.x1, self.y1, self.x2, self.y2)

    def from_abs(self, x1: int, y1: int, x2: int, y2: int) -> ImgBox:
        """基于绝对坐标（上左下右）对图片进行裁剪
        """
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        return self

    def from_pct(self, x1: float, y1: float, x2: float, y2: float, w: int, h: int) -> ImgBox:
        """基于百分比（上左下右）对图片进行裁剪，需要配合图片的长宽参数
        """
        assert 0 <= x1 <= 1
        assert 0 <= y1 <= 1
        assert 0 <= x2 <= 1
        assert 0 <= y2 <= 1
        self.x1 = int(x1 * w)
        self.y1 = int(y1 * h)
        self.x2 = int(x2 * w)
        self.y2 = int(y2 * h)
        return self


class ImgItem:

    def __init__(self, img: Image, img_box: BoxType) -> None:
        self.img = img.crop(img_box)

    def get_width(self):
        return self.img.size[0]

    def get_height(self):
        return self.img.size[1]

    def get_img(self):
        return self.img


def get_merged_imgs(img_items: List[ImgItem]) -> Image:
    assert img_items.__len__() > 0

    sum_w = img_items[0].get_width()
    # 保持每张图片的宽度相等
    # TODO: 支持同一化不同宽度的图片
    for img in img_items[1:]:
        assert sum_w == img.get_width()

    sum_h = sum(i.get_height() for i in img_items)

    sum_img = Image.new("RGB", (sum_w, sum_h), (250, 250, 250))
    cur_h = 0
    for img_item in img_items:
        sum_img.paste(img_item.get_img(), box=(0, cur_h))
        cur_h += img_item.get_height()
        print(
            f"img_item_size: ({img_item.get_width(), img_item.get_height()}), cur_h: {cur_h}")
    return sum_img


def merge_imgs_and_save(img_path: str, img_items: List[ImgItem]):
    """
    Args:
        img_path (str): [description]
        img_items (List[ImgItem]): [description]
    """
    img_merged = get_merged_imgs(img_items)
    img_abs_path = os.path.abspath(img_path)
    img_merged.save(img_abs_path)
    print(f"finished saving image to: {img_abs_path}")
