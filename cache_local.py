import os
import json
from functools import wraps
from hashlib import sha1

MAX_FILENAME_LENGTH = 40
CACHE_DIR = os.path.join(os.path.dirname(__file__), '_cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


class CacheNotFound(Exception):
    pass


def _args_to_fname(name, args, kwargs)-> str:
    arg_kw = str(args) + str(kwargs)
    arg_kw = "".join(c if c.isalnum() else '_' for c in arg_kw)
    fname = name + '_' + arg_kw
    while '__' in fname:
        fname = fname.replace('__', '_')
    if len(fname) > MAX_FILENAME_LENGTH:
        # name too long. using hash.
        fname = sha1(fname.encode()).hexdigest()
    return fname


def _save_result_to_file(fname, result):
    mode = 'w'
    if isinstance(result, dict):
        result = json.dumps(result, indent=4)
    if isinstance(result, bytes):
        mode = 'wb'
    with open(os.path.join(CACHE_DIR, fname), mode) as f:
        f.write(result)


def _read_cache_from_file(fname):
    mode = 'r'
    if fname.startswith('fullimage'):
        mode = 'rb'
    try:
        with open(os.path.join(CACHE_DIR, fname), mode) as f:
            print(f"reading from cache: {fname}")
            result = f.read()
            if isinstance(result, str):
                if result.startswith('{') or result.startswith('['):
                    result = json.loads(result)
            return result
    except FileNotFoundError:
        raise CacheNotFound


def cache_local(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        fname = _args_to_fname(decorated.__name__, args, kwargs)
        try:
            result = _read_cache_from_file(fname)
        except CacheNotFound:
            result = f(*args, **kwargs)
            print(f"saving cache: {fname}")
            _save_result_to_file(fname, result)
        return result

    return decorated
