"""
DAY 3 - Signals, streaming data, process stats
Rules: no autocomplete, no docs, no AI. Narrate out loud as you code.
Edge cases are NOT spelled out. Finding them is part of the work -- read each
spec, ask what breaks it, and handle it. The tests check the ones that matter.
Run:  python day3.py
Target: all PASS in under 90 minutes.

A camera produces frames forever. A sensor logs forever. You cannot hold it all.
This file is about processing a stream: fixed memory, one pass, no full history.
"""
from collections import deque, defaultdict
import math


# ================= PART A: Process data (target 25 min) =================

def group_stats(records, key, value):
    """records: list of dicts. Group by record[key], and for each group return
        {group: {"n": int, "mean": float, "std": float}}
    std is the POPULATION standard deviation
    """
    # std = sqrt(sum(x - mean)**2 /N)
    groups = {}
    result = {}
    for record in records:
        k = record[key]
        v = record[value]
        if k not in groups:
            groups[k] = []
        groups[k].append(v)

    for group, values in groups.items():
        n = len(values)
        mean = sum(values) / len(values)
        variance = 0
        for num in values:
            variance += ((num - mean)**2)
        variance /= n
        std = math.sqrt(variance)
        result[group] = {'n': n,
                         'mean': float(mean),
                         'std': float(std)
                         }
    return result


def cpk(values, lsl, usl):
    """Process capability index.

        Cpk = min(Cpu, Cpl)

        Cpu = (USL - mu) / 3*sigma
        Cpl = (mu - LSL) / 3*sigma

    mu is the mean, sigma the population standard deviation.

    Cpk >= 1.33 is the usual manufacturing target: the spec window is
    comfortably wider than the process spread.
    """
    if len(values) <2:
        return None
    if len(set(values)) <= 1:
        return None
    
    mean = (sum(values) / len(values))
    variance = 0
    for measurment in values:
        variance += ((measurment - mean)**2)
    variance /= len(values)
    std = math.sqrt(variance)
    cpk = min(usl - mean, mean - lsl) / (3*std)
    return cpk




def first_out_of_spec(values, lsl, usl):
    """Return the index of the first value outside [lsl, usl], or -1 if all pass.
    One pass, no sorting.
    """
    for i in range(len(values)):
        if values[i] > usl or values[i] < lsl:
            return i
    return -1
    


def confusion(predicted, actual):
    """predicted, actual: equal-length lists of 0/1. 1 = defect.
    Return the four confusion-matrix counts plus precision and recall:
        {"tp": int, "fp": int, "tn": int, "fn": int,
         "precision": float, "recall": float}

    tp: called it a defect, it was one.
    fp: called it a defect, it was fine        -> false reject, good part scrapped.
    tn: called it fine, it was fine.
    fn: called it fine, it was a defect        -> false escape, bad part shipped.

    Precision: of everything you flagged, how much was really bad.
    Recall:    of everything really bad, how much you caught.
    """
    total = min(len(predicted), len(actual)) # In case they are not equal
    tp, fp, tn, fn = 0, 0, 0, 0

    for i in range(total):
        if (predicted[i]!=actual[i]):
            if predicted[i] == 1:
                fp+=1
            else:
                fn+=1
        else:
            if predicted[i] == 1:
                tp+=1
            else:
                tn+=1
    precision =  tp/ (tp + fp) if tp+fp !=0 else 0
    recall = (tp /(tp + fn)) if tp+fn !=0 else 0
    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": precision,
        "recall": recall
    }






# ================= PART B: Windows (target 25 min) =================

def moving_average(values, k):
    """Return a list of averages over every window of k consecutive values.
    """
    if k == 1:
        return values
    if k > len(values) or k ==0:
        return []

    
    averages = []
    r = 0
    window_sum = 0
    # [1, 2, 3, 4], k = 2

    for l in range(len(values)): # l is 0-3
        if r>= len(values):
            return averages
        
        if l == 0:
            window_sum += values[l]
            while r< len(values) and (r-l +1) != k:
                r+=1
                window_sum += values[r]
            
        else:
            window_sum += values[r]
        
        averages.append(window_sum/ k)
        r+=1
        window_sum -= values[l]

    return averages



def window_max(values, k):
    if k <= 0 or k > len(values):
        return []

    result = []
    for i in range(len(values) - k + 1):
        result.append(max(values[i:i+k]))
    return result

        

def drift_alarm(values, k, limit):
    """Return the index of the FIRST window of k values whose mean deviates from
    the mean of the FIRST k values by more than `limit` (absolute difference).
    The index is the START index of that window. Return -1 if no window drifts.
    Skip window 0 (it is the baseline).
    """
    averages = moving_average(values, k)
    if not averages:
        return -1

    baseline = 0
    for index, value in enumerate(averages):
        if index == 0:
            baseline = value
        else:
            if abs(value-baseline) > limit:
                return index
    return -1
        




# ================= PART C: Ring buffer (target 15 min) =================

class RingBuffer:
    """Fixed-capacity buffer. When full, a push overwrites the OLDEST value.

    Methods: __init__(capacity), push(value), __len__(), is_full(),
             to_list()  -- oldest first,
             mean()

    push reports what it evicted, if anything. An invalid capacity is an error.
    """

    def __init__(self, capacity):
        if capacity <=0:
            raise ValueError("capacity must be >=1")
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.start = 0
        self.n = 0
        self.total_sum = 0
    

    def push(self, value):
   
        if self.n < self.capacity:
            index = (self.start + self.n) % self.capacity
            evicted = self.buffer[index]
            self.buffer[index] = value
            self.n = min(self.n +1, self.capacity)
            self.total_sum += value
        else:
            index = (self.start + self.n) % self.capacity
            evicted = self.buffer[index]
            self.total_sum -= self.buffer[index] if self.buffer[index] is not None else 0
            self.total_sum += value
            self.buffer[index] = value
            self.start = 0 if (self.start == self.capacity -1) else self.start +1 

        return evicted


    def is_full(self):
        return self.n == self.capacity


    def to_list(self):
     return (self.buffer[self.start:] + self.buffer[0:self.start]) if self.n == self.capacity else self.buffer[self.start:self.n]

    def mean(self):
        return (self.total_sum / self.n) if self.n !=0 else None


    #dunder method (overloading)
    def __len__(self):
        return min(self.n, self.capacity)



    


# ================= PART D: Edges and debouncing (target 25 min) =================

def rising_edges(signal):
    """signal: list of 0/1. Return indices where the value goes 0 -> 1.
    The index reported is where the 1 appears.
    [0, 1, 1, 0, 1] -> [1, 4]
    """
    if len(signal) <2:
        return []
    rising = []

    l, r = 0, 1
    while r<len(signal):
        if (signal[l]^signal[r]) and signal[r]:
            rising.append(r)
        l+=1
        r+=1
    return rising



def falling_edges(signal):
    """Indices where the value goes 1 -> 0. Index is where the 0 appears.
    [0, 1, 1, 0, 1] -> [3]
    """
    if len(signal) <2:
        return []
    
    rising = []

    l, r = 0, 1
    while r<len(signal):
        if (signal[l]^signal[r]) and not signal[r]:
            rising.append(r)
        l+=1
        r+=1
    return rising




def debounce(signal, n):
    """A noisy sensor flickers. Only accept a state change after n consecutive
    samples of the new value.

    Return a list the same length as signal: the DEBOUNCED state at each index.
    The output starts at signal[0] and only changes once n consecutive samples
    of the opposite value have been seen -- the change is reported at the index
    of the nth sample.

    n=2:  [0,0,1,0,1,1,1,0,0]  ->  [0,0,0,0,0,1,1,1,0]
                    ^ lone 1 ignored     ^ two 1s: switch at idx 5
                                                     ^ two 0s: switch at idx 8
    """

    if not signal:
        return []
    
    result = signal.copy()
    state = signal[0]
    streak = 0

    for index, num in enumerate(signal):
        if num != state:
            streak+=1
            if streak <n:
                result[index] = state
            elif streak>=n:
                state = num
             
        if num == state:
            streak = 0

    
    return result


def pulse_widths(signal):
    """Return the length of every run of consecutive 1s, in order.
    [0,1,1,0,1,1,1,0] -> [2, 3]
    """
    if not signal:
        return []

    result = []
    i = 0
    while i < len(signal):
        if signal[i] != 1:
            i+=1
        else:
            counter = 1
            i+=1
            while i<len(signal) and signal[i] == 1:
                counter +=1
                i+=1
            result.append(counter)

    return result
            



# ======================= TESTS (don't edit) =======================

RECS = [
    {"station": "ST1", "width": 12.0},
    {"station": "ST1", "width": 14.0},
    {"station": "ST2", "width": 10.0},
    {"station": "ST1", "width": 16.0},
    {"station": "ST2", "width": 10.0},
    {"station": "ST3", "width": 99.0},
]


def t_group_stats():
    g = group_stats(RECS, "station", "width")
    assert set(g) == {"ST1", "ST2", "ST3"}
    assert g["ST1"]["n"] == 3
    assert abs(g["ST1"]["mean"] - 14.0) < 1e-9
    assert abs(g["ST1"]["std"] - math.sqrt(8 / 3)) < 1e-9
    assert abs(g["ST2"]["std"] - 0.0) < 1e-9
    assert g["ST3"]["n"] == 1 and g["ST3"]["std"] == 0.0
    assert group_stats([], "station", "width") == {}

def t_cpk():
    vals = [10, 10, 10, 10]
    assert cpk(vals, 9, 11) is None, "sigma == 0 -> None"
    assert cpk([10], 9, 11) is None
    v = [9.0, 10.0, 11.0]                      # mean 10, pop sigma sqrt(2/3)
    s = math.sqrt(2 / 3)
    assert abs(cpk(v, 7, 13) - (3 / (3 * s))) < 1e-9
    off = [11.0, 12.0, 13.0]                   # mean 12, closer to usl
    s2 = math.sqrt(2 / 3)
    assert abs(cpk(off, 7, 13) - (1 / (3 * s2))) < 1e-9

def t_first_out_of_spec():
    assert first_out_of_spec([1, 2, 3], 0, 5) == -1
    assert first_out_of_spec([1, 9, 3], 0, 5) == 1
    assert first_out_of_spec([-1, 2], 0, 5) == 0
    assert first_out_of_spec([], 0, 5) == -1
    assert first_out_of_spec([5, 0], 0, 5) == -1, "limits are inclusive"

def t_confusion():
    c = confusion([1, 0, 1, 1, 0], [1, 0, 0, 1, 1])
    assert c["tp"] == 2 and c["fp"] == 1 and c["tn"] == 1 and c["fn"] == 1
    assert abs(c["precision"] - 2 / 3) < 1e-9
    assert abs(c["recall"] - 2 / 3) < 1e-9
    z = confusion([0, 0], [0, 0])
    assert z["precision"] == 0.0 and z["recall"] == 0.0

def t_moving_average():
    assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]
    assert moving_average([5], 1) == [5.0]
    assert moving_average([1, 2], 5) == []
    assert moving_average([1, 2], 0) == []

def t_window_max():
    assert window_max([1, 3, -1, -3, 5], 3) == [3, 3, 5]
    assert window_max([4, 4, 4], 2) == [4, 4]
    assert window_max([1], 3) == []

def t_drift_alarm():
    flat = [10, 10, 10, 10, 10, 10]
    assert drift_alarm(flat, 2, 0.5) == -1
    drift = [10, 10, 10, 10, 20, 20]
    assert drift_alarm(drift, 2, 0.5) == 3
    assert drift_alarm([1, 2], 5, 1.0) == -1

def t_ring_buffer():
    try:
        RingBuffer(0)
        assert False, "capacity 0 must raise ValueError"
    except ValueError:
        pass
    rb = RingBuffer(3)
    assert len(rb) == 0 and rb.mean() is None and not rb.is_full()
    assert rb.push(1) is None
    assert rb.push(2) is None
    assert rb.push(3) is None
    assert rb.is_full() and len(rb) == 3
    assert rb.to_list() == [1, 2, 3]
    assert abs(rb.mean() - 2.0) < 1e-9
    assert rb.push(4) == 1, "must return the evicted value"
    assert rb.to_list() == [2, 3, 4]
    assert rb.push(5) == 2
    assert rb.to_list() == [3, 4, 5]
    assert len(rb) == 3

def t_rising_edges():
    assert rising_edges([0, 1, 1, 0, 1]) == [1, 4]
    assert rising_edges([1, 1, 1]) == []
    assert rising_edges([]) == []
    assert rising_edges([1]) == [], "no prior sample -> not an edge"

def t_falling_edges():
    assert falling_edges([0, 1, 1, 0, 1]) == [3]
    assert falling_edges([0, 0]) == []

def t_debounce():
    assert debounce([0, 0, 1, 0, 1, 1, 1, 0, 0], 2) == [0, 0, 0, 0, 0, 1, 1, 1, 0]
    assert debounce([0, 1, 0, 1, 0], 2) == [0, 0, 0, 0, 0], "all flicker suppressed"
    assert debounce([0, 1, 1, 1], 1) == [0, 1, 1, 1], "n<=1 -> passthrough"
    assert debounce([], 2) == []

def t_pulse_widths():
    assert pulse_widths([0, 1, 1, 0, 1, 1, 1, 0]) == [2, 3]
    assert pulse_widths([0, 1, 1]) == [2]
    assert pulse_widths([0, 0]) == []
    assert pulse_widths([1]) == [1]


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