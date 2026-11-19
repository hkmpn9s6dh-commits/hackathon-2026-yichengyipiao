"""本机路径带中文：cv2.imread/imwrite 会失败，统一用 PIL 收发。"""
import numpy as np
from PIL import Image


def read_bgr(path):
    im = Image.open(path).convert("RGB")
    return np.array(im)[:, :, ::-1].copy()          # RGB -> BGR


def read_rgba(path):
    im = Image.open(path).convert("RGBA")
    return np.array(im)


def write_rgba(path, arr_rgba):
    Image.fromarray(arr_rgba, "RGBA").save(path)


def write_bgr(path, arr_bgr, **kw):
    Image.fromarray(arr_bgr[:, :, ::-1]).save(path, **kw)
