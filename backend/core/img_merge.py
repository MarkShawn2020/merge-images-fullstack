from typing import List, Tuple
from PIL import Image

CropY1Y2 = Tuple[float, float]


def merge_imgs(
        imgs: List[Image.Image],
        crops: List[CropY1Y2] = None,
) -> Image.Image:
    assert imgs.__len__() > 0
    base_img = imgs[0]
    N = imgs.__len__()
    if crops is not None:
        assert isinstance(crops, List)
        assert crops.__len__() == N

    final_w = base_img.size[0]
    final_h = 0  # 不直接与final_w一起初始化，是因为图片经过裁切后高度可能变化

    paste_hs = []
    for i in range(N):
        if imgs[i].size[0] != final_w:
            imgs[i] = imgs[i].resize(
                (final_w, (int)(final_w / imgs[i].size[0] * imgs[i].size[1])))
        w, h = imgs[i].size
        y1 = 0
        y2 = h
        if crops is not None:
            # assert isinstance(crops[i], CropY1Y2), 类型注解只能检查基本数据类型，所以这里需要自己写校验
            assert isinstance(crops[i], Tuple)
            assert crops[i].__len__() == 2
            for j in crops[i]:
                assert 0 <= j <= 100
            assert crops[i][0] <= crops[i][1]

            y1 = int(h / 100 * crops[i][0])
            y2 = int(h / 100 * crops[i][1])
            h = y2 - y1
            imgs[i] = imgs[i].crop((0, y1, w, y2))
        paste_hs.append(final_h)
        final_h += h

    print(
        f"final image size: ({final_w}, {final_h}), total: {final_w * final_h} pixels")
    final_img = Image.new(base_img.mode, (final_w, final_h), (250, 250, 250))
    for i in range(N):
        final_img.paste(imgs[i], (0, paste_hs[i]))

    return final_img
