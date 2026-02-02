from tqdm import trange
import time

def process(t: int):
    assert t > 0, "t must be positive"
    for _ in trange(100):
        time.sleep(t / 100)
