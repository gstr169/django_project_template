import time
from contextlib import contextmanager
from django.core.cache import cache


def timer(f):
    def decorated_func(*args, **kwargs):
        s_t = time.perf_counter()
        res = f(*args, **kwargs)
        f_t = time.perf_counter()
        class_info = ""
        if args and isinstance(args[0], object):
            class_info = f" of {args[0]}"
        print(f"{f.__name__}{class_info} worked for {(f_t - s_t ):.5f} seconds")
        return res
    return decorated_func


@contextmanager
def cache_lock(lock_id, oid, expire: int = None) -> bool:
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, expire)
    try:
        yield status
    finally:
        # redis delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)


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