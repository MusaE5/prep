"""
DAY 2 - 2D grids, connected components, filters
Rules: no autocomplete, no docs, no AI. Narrate out loud as you code.
Run:  python day2.py
Target: all PASS in under 2 hours.

A grayscale image is a 2D array of pixel values.
Defect detection = threshold it, group the pixels, measure the groups.
That is exactly what this file walks through.
"""
from collections import deque
import numpy as np


# ================= PART A: Thresholding (target 20 min) =================

def threshold_py(img, t):
    """PURE PYTHON. img: list of lists of numbers.
    Return a new list of lists: 1 where pixel > t, else 0. Do not modify img.
    [[1, 9], [8, 2]], 5 -> [[0, 1], [1, 0]]
    """

    result = []
    for arr in img:
        sub_arr = []
        for pixel in arr:
            if pixel>t:
                sub_arr.append(1)
            else:
                sub_arr.append(0)
        result.append(sub_arr)
    return result

    


def threshold_np(img, t):
    """NUMPY, no Python loops. Return a uint8 array: 255 where img > t, else 0.
    Hint: np.where takes (condition, value_if_true, value_if_false).
    """
    result = np.where(img>t, 255, 0 )
    return result.astype(np.uint8)


def otsu_like(img, t_values):
    """img: 2D numpy array. t_values: list of candidate thresholds.
    For each t, split pixels into foreground (> t) and background (<= t).
    Return the t that MAXIMIZES between-class variance:
        w_b * w_f * (mean_b - mean_f) ** 2
    where w_b, w_f are the fraction of pixels in each class.
    Skip any t where either class is empty. Ties -> smallest t.

    This is the core of Otsu's method: automatic threshold selection.
    """
    max_t = None
    for t in t_values: 
        below = img<=t
        w_b, w_f = np.mean(below), np.mean(~below)
        if (w_b == 0 or w_f == 0):
            continue
        mean_b, mean_f = np.mean(img[below]), np.mean(img[~below]) 
        variance = w_b * w_f * (mean_b - mean_f)**2
        if max_t is None:
            max_t = (variance, t)
        elif variance > max_t[0]:
            max_t = (variance, t)
        elif variance == max_t[0] and t< max_t[1]:
            max_t = (variance, t)


    return max_t[1] if max_t is not None else None


    



# ================= PART B: Connected components (target 45 min) =================

def neighbors(r, c, rows, cols, connectivity=4):
    """Return in-bounds neighbor coords of (r, c) as a list of (row, col).
    connectivity=4 -> N, S, E, W.  connectivity=8 -> also the diagonals.
    Order does not matter.
    """
    result = []
    offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    if connectivity == 8:
        offsets  = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]

    for dr, dc in offsets:
        new_r, new_c = r+dr, c+dc
        # Check if out of bounds
        if(new_r >= rows or new_c >=cols or new_r < 0 or new_c <0):
            continue
        else:
            result.append((new_r, new_c))
    return result






    

    


def count_blobs(binary, connectivity=4):
    """binary: list of lists of 0/1. Return the number of connected regions of 1s.
    [[1,1,0],
     [0,1,0],
     [0,0,1]]  -> 2 with connectivity=4, 1 with connectivity=8
    """
    pass


def blob_stats(binary, connectivity=4):
    """Return a list of dicts, one per blob, sorted by area DESC then by
    (min_row, min_col) ASC:
        {"area": int,
         "bbox": (min_row, min_col, max_row, max_col),   # inclusive
         "centroid": (mean_row, mean_col)}               # floats
    """
    pass


def largest_blob_mask(binary, connectivity=4):
    """Return a new grid (list of lists) with ONLY the largest blob's pixels as 1,
    everything else 0. If there are no blobs, return a grid of all 0s.
    Ties -> the blob whose (min_row, min_col) is smallest.
    """
    pass


# ================= PART C: Filters (target 30 min) =================

def mean_filter_3x3(img):
    """PURE PYTHON. img: list of lists of numbers.
    Each output pixel = average of its 3x3 neighbourhood.
    Border handling: only average the neighbours that exist (no padding).
    Return floats. Do not modify img.
    """
    pass


def sobel_magnitude(img):
    """NUMPY in, NUMPY out. img: 2D float array.
    Apply the 3x3 Sobel kernels to every pixel that has a full 3x3 neighbourhood,
    then return sqrt(gx**2 + gy**2).
    Output shape is (rows-2, cols-2) -- no padding, borders dropped.

    Gx = [[-1, 0, 1],     Gy = [[-1, -2, -1],
          [-2, 0, 2],           [ 0,  0,  0],
          [-1, 0, 1]]           [ 1,  2,  1]]

    Loops over the OUTPUT pixels are fine here.
    """
    pass


# ================= PART D: Transforms (target 15 min) =================

def rotate90_cw(img):
    """PURE PYTHON, no numpy. Rotate a list-of-lists 90 degrees clockwise.
    [[1,2],
     [3,4]] -> [[3,1],
                [4,2]]
    """
    pass


def transpose_py(img):
    """PURE PYTHON. Swap rows and columns. Works on non-square grids."""
    pass


# ======================= TESTS (don't edit) =======================

BIN = [
    [1, 1, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0],
]


def t_threshold_py():
    src = [[1, 9], [8, 2]]
    assert threshold_py(src, 5) == [[0, 1], [1, 0]]
    assert src == [[1, 9], [8, 2]], "must not modify the input"
    assert threshold_py([[5, 5]], 5) == [[0, 0]], "strictly greater than"

def t_threshold_np():
    out = threshold_np(np.array([[1, 9], [8, 2]]), 5)
    assert out.dtype == np.uint8
    assert out.tolist() == [[0, 255], [255, 0]]

def t_otsu_like():
    img = np.array([[10, 10, 200], [10, 200, 200]], dtype=float)
    assert otsu_like(img, [5, 50, 150, 250]) == 50

def t_neighbors():
    assert sorted(neighbors(0, 0, 3, 3, 4)) == [(0, 1), (1, 0)]
    assert sorted(neighbors(1, 1, 3, 3, 4)) == [(0, 1), (1, 0), (1, 2), (2, 1)]
    assert len(neighbors(1, 1, 3, 3, 8)) == 8
    assert sorted(neighbors(0, 0, 3, 3, 8)) == [(0, 1), (1, 0), (1, 1)]

def t_count_blobs():
    assert count_blobs(BIN, 4) == 4
    assert count_blobs(BIN, 8) == 4
    diag = [[1, 0], [0, 1]]
    assert count_blobs(diag, 4) == 2
    assert count_blobs(diag, 8) == 1
    assert count_blobs([[0, 0], [0, 0]]) == 0

def t_blob_stats():
    s = blob_stats(BIN, 4)
    assert len(s) == 4
    assert s[0]["area"] == 3
    assert s[0]["bbox"] == (0, 0, 1, 1)
    assert abs(s[0]["centroid"][0] - 1 / 3) < 1e-9
    assert abs(s[0]["centroid"][1] - 2 / 3) < 1e-9
    assert [b["area"] for b in s] == [3, 2, 2, 1]
    assert s[1]["bbox"] == (0, 4, 1, 4)
    assert s[2]["bbox"] == (3, 2, 3, 3)
    assert s[3]["bbox"] == (3, 0, 3, 0)
    assert blob_stats([[0, 0]]) == []

def t_largest_blob_mask():
    assert largest_blob_mask(BIN, 4) == [
        [1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    assert largest_blob_mask([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]

def t_mean_filter():
    src = [[1, 2], [3, 4]]
    out = mean_filter_3x3(src)
    assert all(abs(v - 2.5) < 1e-9 for row in out for v in row)
    assert src == [[1, 2], [3, 4]], "must not modify the input"
    out2 = mean_filter_3x3([[0, 0, 0], [0, 9, 0], [0, 0, 0]])
    assert abs(out2[1][1] - 1.0) < 1e-9
    assert abs(out2[0][0] - 9 / 4) < 1e-9

def t_sobel():
    img = np.array([
        [0, 0, 255, 255],
        [0, 0, 255, 255],
        [0, 0, 255, 255],
        [0, 0, 255, 255],
    ], dtype=float)
    out = sobel_magnitude(img)
    assert out.shape == (2, 2)
    assert np.allclose(out, 1020.0), "vertical edge -> strong gx, zero gy"
    flat = sobel_magnitude(np.ones((4, 4)))
    assert np.allclose(flat, 0.0)

def t_rotate90():
    assert rotate90_cw([[1, 2], [3, 4]]) == [[3, 1], [4, 2]]
    assert rotate90_cw([[1, 2, 3], [4, 5, 6]]) == [[4, 1], [5, 2], [6, 3]]

def t_transpose():
    assert transpose_py([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("t_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__[2:]}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__[2:]}  {e or '(wrong output)'}")
        except Exception as e:
            print(f"FAIL  {t.__name__[2:]}  ({type(e).__name__}: {e})")
    print(f"\n{passed}/{len(tests)} passed")