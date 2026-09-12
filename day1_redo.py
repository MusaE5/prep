"""
DAY 1 REDO - cold retest
Do NOT open day1.py. No notes, no docs, no AI.
Time each function. Target: all 5 passing in under 20 minutes total.
Run:  python day1_redo.py
"""
from collections import Counter, defaultdict, deque
import heapq
import numpy as np


# ---- 1. target 3 min ----
def top_defects(defects, k):
    """Return the k most common defect types as [(type, count), ...], most common first.
    ["scratch","pinhole","scratch","streak","scratch","pinhole"], 2
      -> [("scratch", 3), ("pinhole", 2)]
    """
    freq = {}
    pairs = []
    for defect in defects:
        if defect not in freq:
            freq[defect] = 0
        freq[defect] +=1

    for key, value in freq.items():
        pairs.append((key, value))

    pairs = sorted(pairs, key = lambda x: x[1], reverse = True)
    return pairs[:k]


    
    


# ---- 2. target 3 min ----
def mean_by_station(readings):
    """readings: list of (station, value). Return {station: mean}.
    [("ST1", 10), ("ST2", 4), ("ST1", 12)] -> {"ST1": 11.0, "ST2": 4.0}
    """
    stations = {}

    for s in readings:
        station = s[0]
        if station not in stations:
            stations[station] = []
        stations[station].append(s[1])

    for k, v in stations.items():
        stations[k] = sum(stations[k]) / len(stations[k])
    return stations



# ---- 3. target 7 min ----
def parse_log(lines):
    """Valid line format: 'timestamp,station,measurement,value'
    e.g. '2026-09-23T10:01:05,ST3,width_mm,12.41'
    Return list of dicts: {"ts": str, "station": str, "meas": str, "value": float}
    Strip whitespace around every field.
    Skip: blank lines, wrong field count, non-numeric value.
    """
    result = []
    def isFloat(num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        
    for s in lines:
        words = s.split(',')
        if len(words) != 4:
            continue
        stripped = [word.strip() for word in words]
        if not isFloat(stripped[3]):
            continue
        result.append({
            'ts': stripped[0],
            'station': stripped[1],
            'meas': stripped[2],
            'value': float(stripped[3])
        })
    return result




# ---- 4. target 3 min, NO Python loops ----
def bright_pixels(img, thresh):
    """Return (count, coords) for pixels > thresh.
    coords: list of (row, col) tuples in row-major order.
    """
    #img is a numpy array
    coords = np.argwhere(img>thresh)
    coords.tolist()
    count = len(coords)
    return (count, [tuple(coord) for coord in coords])
    


# ---- 5. target 4 min, NO Python loops ----
def to_uint8(img):
    """Scale a float array linearly so min->0, max->255. Round, return dtype uint8.
    If all values are equal, return zeros (uint8) of the same shape.
    """
    low, hi = img.min(), img.max()
    if low == hi:
        return np.zeros(img.shape, dtype = np.uint8)
    img = ((img - low) * 255) / (hi-low)
    img = img.round()
    return img.astype(np.uint8)
    


# ======================= TESTS (don't edit) =======================

LOG = [
    "2026-09-23T10:01:05,ST1,width_mm,12.41",
    "2026-09-23T10:01:06,ST1,width_mm,12.60",
    "",
    "2026-09-23T10:01:07,ST2,width_mm,12.38",
    "garbage line",
    "2026-09-23T10:01:08,ST2,width_mm,abc",
    " 2026-09-23T10:01:09 , ST2 , width_mm , 12.20 ",
    "2026-09-23T10:01:10,ST1,width_mm,12.45",
]


def t_top_defects():
    d = ["scratch", "pinhole", "scratch", "streak", "scratch", "pinhole"]
    assert top_defects(d, 2) == [("scratch", 3), ("pinhole", 2)]
    assert top_defects(d, 10) == [("scratch", 3), ("pinhole", 2), ("streak", 1)]
    assert top_defects([], 2) == []

def t_mean_by_station():
    assert mean_by_station([("ST1", 10), ("ST2", 4), ("ST1", 12)]) == {"ST1": 11.0, "ST2": 4.0}
    assert mean_by_station([]) == {}

def t_parse_log():
    r = parse_log(LOG)
    assert len(r) == 5
    assert r[3] == {"ts": "2026-09-23T10:01:09", "station": "ST2", "meas": "width_mm", "value": 12.20}
    assert isinstance(r[0]["value"], float)
    assert parse_log([]) == []

def t_bright_pixels():
    count, coords = bright_pixels(np.array([[1, 9, 3], [8, 2, 7]]), 5)
    assert count == 3
    assert coords == [(0, 1), (1, 0), (1, 2)], "must be a list of real tuples"
    c2, co2 = bright_pixels(np.zeros((3, 3)), 5)
    assert c2 == 0 and co2 == []

def t_to_uint8():
    out = to_uint8(np.array([[0.0, 2.0], [4.0, 10.0]]))
    assert out.dtype == np.uint8
    assert out.tolist() == [[0, 51], [102, 255]]
    # catches a missing round()
    out2 = to_uint8(np.array([[0.0, 1.0], [2.0, 7.0]]))
    assert out2.tolist() == [[0, 36], [73, 255]], "did you round before casting?"
    flat = to_uint8(np.full((2, 3), 7.0))
    assert flat.dtype == np.uint8 and flat.shape == (2, 3) and flat.sum() == 0


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