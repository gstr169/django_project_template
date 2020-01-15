import time
from contextlib import contextmanager
from django.core.cache import cache


def timer(f):
    s = {list, set, tuple}

    def decorated_func(*args, **kwargs):
        s_t = time.perf_counter()
        res = f(*args, **kwargs)
        f_t = time.perf_counter()
        class_info = ""
        if args and type(args[0]) not in s and isinstance(args[0], object):
            class_info = f" of {args[0]}"
        print(f"{f.__name__}{class_info} worked for {(f_t - s_t ):.5f} seconds")
        return res
    return decorated_func


@contextmanager
def cache_lock(lock_name, timeout: int = None, blocking_timeout: int = None, sleep=0.1) -> bool:
    lock = cache.lock(lock_name, timeout=timeout, blocking_timeout=blocking_timeout, sleep=sleep)
    acquired = lock.acquire()
    try:
        yield acquired
    finally:
        if acquired:
            lock.release()


@contextmanager
def cache_lock_await(lock_id, oid, expire: int = None, attempts: int = 20, interval: float = 0.5) -> bool:
    """
    Use this ONLY if you now what do you do.
    """
    status = False
    # trying to create lock, doing some attempts with defined interval
    for attempt in range(1, attempts):
        time.sleep(interval)
        status = cache.add(lock_id, oid, expire)
        # if lock was created, stop trying and return True
        if status:
            break
    # if lock wasn't created, return False
    try:
        yield status
    finally:
        if status:
            cache.delete(lock_id)