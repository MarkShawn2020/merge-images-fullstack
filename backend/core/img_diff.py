from typing import List
from PIL import Image
import imagehash
import numpy as np

from backend.settings import DEFAULT_DIFF_THREAD


def get_hashes(imgs: List[Image.Image]) -> List[int]:
    return list(map(imagehash.average_hash, imgs))


def get_diffs_int(
        hashes: List[int],
) -> List[bool]:
    """[summary]
    Args:
        hashes (List[int]): [description]

    Returns:
        List[bool]: [description]
    """
    # 第一张图永远是“最独特的”，所以diff值最大
    return [np.Inf] + [(hashes[i] - hashes[i - 1]) for i in range(1, len(hashes))]


def get_diffs_bool(diffs: List[int], diff_thread: int = DEFAULT_DIFF_THREAD):
    assert isinstance(diff_thread, int)
    assert diff_thread >= 0
    return list(j >= diff_thread for j in diffs)
