import os

BACKEND_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BACKEND_DIR, "output")

VALID_IMG_TYPES = ["png", "jpg", "jpeg"]

DEFAULT_BODY_PCTS = [0, 5, 100, 95]
DEFAULT_DIFF_THREAD = 5  # 两张图片的哈希值相差多少视为不同
DEFAULT_CAPTAIN_PCTS = [45, 80, 55, 95]
DEFAULT_DENSITY_THREAD = 0.1
DEFAULT_RATIO_THREAD = 56
DEFAULT_MAX_IMG_SIZE = 10 * 1024 * 1024 * 0.9  # 微信公众号限制图片大小于10Mb
DEFAULT_MAX_IMG_DIMENSION = 6000000  # 微信公众号限制长宽乘积小于600万
DEFAULT_MIN_SCALE_RATIO = 0.9  # 每一次的最低压缩比率
