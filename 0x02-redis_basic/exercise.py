#!/usr/bin/env python3
"""
Cache module
"""
import uuid
import redis
from typing import Union, Callable, Any

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
        if not self._redis.exists(key):
            return None
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)

def count_calls(method: Callable) -> Callable:
    import functools

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        count = self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    import functools

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        inputs_key = f"{key}:inputs"
        outputs_key = f"{key}:outputs"
        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, result)
        return result

    return wrapper

def replay(func: Callable):
    inputs_key = f"{func.__qualname__}:inputs"
    outputs_key = f"{func.__qualname__}:outputs"
    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)
    print(f"{func.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{func.__qualname__}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")

cache = Cache()
cache.store = count_calls(cache.store)
cache.store = call_history(cache.store)