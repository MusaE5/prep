"""
DAY 1 - Python fluency drills
Rules: no autocomplete, no docs, no AI. Narrate out loud as you code.
Fill in each function, then run:   python day1.py
Target: all PASS in under 90 minutes total.
"""



# ================= PART A: Core data structures (target 25 min) =================

def top_defects(defects, k):
    """Return the k most common defect types as [(type, count), ...], most common first.
    ["scratch","pinhole","scratch","streak","scratch","pinhole"], 2
      -> [("scratch", 3), ("pinhole", 2)]
    """
    # list of tuples
    #Return k most
    # Order in descending magnitude of appearance

    freq = {}
    for s in defects:
        if s not in freq:
            freq[s] = 0
        freq[s] += 1

    ranked = sorted(freq.items(), key = lambda x: x[1], reverse = True)

    return ranked[:k]



def mean_by_station(readings):
    """readings: list of (station, value). Return {station: mean}.
    [("ST1", 10), ("ST2", 4), ("ST1", 12)] -> {"ST1": 11.0, "ST2": 4.0}
    """
    means = {}
    for (station, value) in readings:
        if station not in means:
            means[station] = []
        means[station].append(value)

    # {station: [v1, v2 ...]}
    for (station, value) in means.items():
        appearences = len(value)
        total = 0
        for num in value:
            total+= num
        mean = total/appearences 
        means[station] = mean

    return means

        


def dedupe_keep_order(ids):
    """Remove duplicates, keep first-occurrence order, O(n).
    [3, 1, 3, 2, 1] -> [3, 1, 2]
    """
    occured = set()
    result = []
    for id in ids:
        if id not in occured:
            occured.add(id)
            result.append(id)
    return result

  


def rank_parts(parts):
    """parts: [(part_id, defect_count)]. Sort by count DESC, then part_id ASC.
    [("B", 2), ("A", 2), ("C", 5)] -> [("C", 5), ("A", 2), ("B", 2)]
    """
    parts.sort(key = lambda p:(-p[1], p[0]))
    return parts
    

from collections import deque
def last_n(stream, n):
    """Return the last n items of any iterable as a list, using O(n) memory.
    range(10), 3 -> [7, 8, 9]
    """
    # we want fifo
    q = deque(maxlen=n)
    for i in stream:
        q.append(i)
    return list(q)

import heapq
def k_fastest(cycle_times, k):
    """Return the k smallest cycle times, ascending. Use heapq.
    [5.2, 3.1, 4.8, 2.9, 6.0], 2 -> [2.9, 3.1]
    """

    h = []
    result = []
    for cycle in cycle_times:
        heapq.heappush(h,cycle)

    for i in range(k):
        result.append(heapq.heappop(h))
    return result



def invert(d):
    """Invert {name: id} into {id: name} with a dict comprehension."""
    return {kv[1]: kv[0] for kv in d.items()}
  


# ================= PART B: Parsing (target 20 min) =================

def parse_log(lines):
    """Valid line format: 'timestamp,station,measurement,value'
    e.g. '2026-09-23T10:01:05,ST3,width_mm,12.41'
    Return list of dicts: {"ts": str, "station": str, "meas": str, "value": float}
    Strip whitespace around every field.
    Skip: blank lines, wrong field count, non-numeric value.
    """
    # [{}, {}, {}]
    def isFloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    keys = ['ts','station','meas','value']
    result = []

    for s in lines:
        words = s.split(',')
        if len(words) != 4 or not isFloat(words[-1]):
            continue

        stripped = [item.strip() for item in words]
        stripped[-1] = float(stripped[-1])
        result.append(dict(zip(keys,stripped)))
    return result




def yield_by_station(records, lsl, usl):
    """records: output of parse_log. Pass if lsl <= value <= usl.
    Return {station: passed/total rounded to 3 decimals}.
    """

    stations = {}
    
    for log in records:
        station = log['station']
        if station not in stations:
            # first element will contain pass, second will contain total
            stations[station] = [0, 0]

        if not (lsl<=log['value']<=usl):
            stations[station][1] +=1
        else:
            stations[station][0] +=1
            stations[station][1] +=1

    for k, v in stations.items():
        stations[k] = round((v[0] /v[1]),3)
    return stations
    
    


        




# ================= PART C: Classes (target 20 min) =================

class Sensor:
    """
    __init__(self, name)         -> store name, empty readings list
    add(self, value)             -> append a reading
    mean(self)                   -> mean of readings, None if empty
    __repr__(self)               -> "Sensor(name='T1', n=3)"
        Use the runtime class name so subclasses print their own name.
    """
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add(self, value):
        self.readings.append(value)

    def mean(self):
        if not self.readings:
            return None
        else:
            total = sum(self.readings)
            return total/ len(self.readings)
        
    def __repr__(self):
        return f"{type(self).__name__}(name='{self.name}', n={len(self.readings)})"






class ThresholdSensor(Sensor):
    """
    __init__(self, name, low, high)  -> must call super().__init__
    anomalies(self)                  -> [(index, value)] for readings outside [low, high]
    """

    def __init__(self, name, low, high):
        super().__init__(name)
        self.low = low
        self.high = high

    def anomalies(self):
        result = []
        for i in range(len(self.readings)):
            if not self.low<=self.readings[i]<=self.high:
                result.append((i, self.readings[i]))
        return result





# ================= PART D: NumPy (target 20 min, NO Python loops) =================
import numpy as np

def to_uint8(img):
    """Scale a float array linearly so min->0, max->255. Round, return dtype uint8.
    If all values are equal, return zeros (uint8) of the same shape.
    """
    
    img = (((img - img.min()) * 255) / (img.max() - img.min())) if img.max() != img.min() else np.zeros(img.shape)
    img = np.round(img)
    img = img.astype(np.uint8)
    return img


def bright_pixels(img, thresh):
    """Return (count, coords) for pixels > thresh.
    coords: list of (row, col) tuples in row-major order.
    """
    coords = np.argwhere(img>thresh)

    count = len(coords)
    return (count, coords)




def column_profile(img):
    """img: rows x cols. Return (col_means, col_stds, noisiest_col).
    noisiest_col = index of column with the highest std. Use axis=.
    """
    col_means = img.mean(axis = 0)
    col_stds  = img.std(axis = 0)
    noisiest_col = col_stds.argmax()
    return (col_means, col_stds, noisiest_col)
    


def crop_and_flip(img, r0, r1, c0, c1):
    """Return img[r0:r1, c0:c1] flipped left-to-right. One line."""
    return img[r0:r1, c0:c1][:, ::-1]
    


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

def t_mean_by_station():
    assert mean_by_station([("ST1", 10), ("ST2", 4), ("ST1", 12)]) == {"ST1": 11.0, "ST2": 4.0}

def t_dedupe():
    assert dedupe_keep_order([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert dedupe_keep_order([]) == []

def t_rank_parts():
    assert rank_parts([("B", 2), ("A", 2), ("C", 5)]) == [("C", 5), ("A", 2), ("B", 2)]

def t_last_n():
    assert last_n(range(10), 3) == [7, 8, 9]
    assert last_n([1, 2], 5) == [1, 2]

def t_k_fastest():
    assert k_fastest([5.2, 3.1, 4.8, 2.9, 6.0], 2) == [2.9, 3.1]

def t_invert():
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}

def t_parse_log():
    r = parse_log(LOG)
    assert len(r) == 5
    assert r[3] == {"ts": "2026-09-23T10:01:09", "station": "ST2", "meas": "width_mm", "value": 12.20}

def t_yield():
    assert yield_by_station(parse_log(LOG), 12.30, 12.50) == {"ST1": 0.667, "ST2": 0.5}

def t_sensor():
    s = Sensor("T1")
    assert s.mean() is None
    for v in [1, 2, 3]:
        s.add(v)
    assert s.mean() == 2.0
    assert repr(s) == "Sensor(name='T1', n=3)"

def t_threshold_sensor():
    t = ThresholdSensor("T2", 0, 10)
    for v in [5, -1, 11, 7]:
        t.add(v)
    assert isinstance(t, Sensor)
    assert t.anomalies() == [(1, -1), (2, 11)]
    assert t.mean() == 5.5
    assert repr(t) == "ThresholdSensor(name='T2', n=4)"

def t_to_uint8():
    out = to_uint8(np.array([[0.0, 2.0], [4.0, 10.0]]))
    assert out.dtype == np.uint8
    assert out.tolist() == [[0, 51], [102, 255]]
    flat = to_uint8(np.full((2, 3), 7.0))
    assert flat.dtype == np.uint8 and flat.shape == (2, 3) and flat.sum() == 0

def t_bright_pixels():
    count, coords = bright_pixels(np.array([[1, 9, 3], [8, 2, 7]]), 5)
    assert count == 3
    assert [tuple(map(int, c)) for c in coords] == [(0, 1), (1, 0), (1, 2)]

def t_column_profile():
    img = np.array([[1, 10, 5], [1, 20, 5], [1, 30, 5]], dtype=float)
    means, stds, col = column_profile(img)
    assert np.allclose(means, [1, 20, 5])
    assert np.allclose(stds, [0, np.std([10, 20, 30]), 0])
    assert col == 1

def t_crop_and_flip():
    img = np.arange(16).reshape(4, 4)
    assert crop_and_flip(img, 1, 3, 0, 3).tolist() == [[6, 5, 4], [10, 9, 8]]


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("t_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__[2:]}")
            passed += 1
        except AssertionError:
            print(f"FAIL  {t.__name__[2:]}  (wrong output)")
        except Exception as e:
            print(f"FAIL  {t.__name__[2:]}  ({type(e).__name__}: {e})")
    print(f"\n{passed}/{len(tests)} passed")