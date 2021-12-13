from PIL import Image
import io
import math

DEFAULT_MAX_IMG_SIZE = 10 * 1024 * 1024
DEFAULT_SCALE = 0.9


def compress_img(
    img: Image.Image,
    max_img_size: float = DEFAULT_MAX_IMG_SIZE,
    scale: float = DEFAULT_SCALE
) -> Image.Image:
    assert 0 < scale < 1
    format = img.format
    while True:
        with io.BytesIO() as bytes:
            w, h = img.size
            # 存储在内存中时必须指定文件格式
            img.save(bytes, format=format)
            bytes_size = bytes.tell()
            print(f"bytes size: {bytes_size:10}, img size: {img.size}")
            if bytes_size > max_img_size:
                pct = math.sqrt(max_img_size / bytes_size)
                pct = min(pct, scale)
                w = int(w * pct)
                h = int(h * pct)
                img = img.resize((w, h), Image.ANTIALIAS)
            else:
                return img


if __name__ == "__main__":
    import os
    choice = 0
    if choice == 1:
        img_path = "/Users/mark/Projects/merge_imgs/backend/output/人生是一场永不落幕的演出.png"
        img_name = os.path.basename(img_path)
        print(f"img_name: {img_name}")
        img = Image.open(img_path)
        compressed_img = compress_img(img)
        compressed_img.save(img_name)
    elif choice == 0:
        dir_path = "/Users/mark/Projects/merge_imgs/backend/output"
        for img_name in os.listdir(dir_path):
            if img_name.endswith("png"):
                print(f"handling img: {img_name}")
                img_path = os.path.join(dir_path, img_name)
                img_size = os.stat(img_path).st_size
                if img_size > DEFAULT_MAX_IMG_SIZE:
                    print(f"comprssing...")
                    compress_img(Image.open(img_path)).save(img_path)
