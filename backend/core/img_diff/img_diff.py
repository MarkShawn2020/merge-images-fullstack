from typing import List
from PIL import Image
import imagehash

MAX_INT = 1000

DEFAULT_DIFF_THREAD = 5


def get_hashes(imgs: List[Image.Image]) -> List[int]:
    return list(map(imagehash.average_hash, imgs))


def get_diffs_int(
    hashes: List[int],
) -> List[bool]:
    """[summary]
    MAX_INT 是为了保证第一张图永远是“最独特的”，因为越不相近（即diff越大）越独特
    Args:
        hashes (List[int]): [description]

    Returns:
        List[bool]: [description]
    """
    return [MAX_INT] + [(hashes[i] - hashes[i-1]) for i in range(1, len(hashes))]


def get_diffs_bool(diffes: List[int], diff_thread: int = DEFAULT_DIFF_THREAD):
    assert isinstance(diff_thread, int)
    assert diff_thread >= 0
    return list(j >= diff_thread for j in diffes)
