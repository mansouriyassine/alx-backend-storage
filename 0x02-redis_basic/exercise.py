#!/usr/bin/env python3
"""
Cache module
"""
import uuid
import redis
from typing import Union, Callable, Any
import functools

class Cache:
    """
    Cache class for storing data in Redis
    """
    def __init__(self):
        """Initialize Cache instance with Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
        """
        Retrieve data from Redis with the given key
        If fn is provided, apply the conversion function to the retrieved data
        """
        if not self._redis.exists(key):
            return None
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve string data from Redis with the given key
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve integer data from Redis with the given key
        """
        return self.get(key, fn=int)

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count method calls
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            count = self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """
        Decorator to store history of inputs and outputs for a function
        """
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

    def replay(self, func: Callable) -> None:
        """
        Display the history of calls of a particular function
        """
        inputs_key = f"{func.__qualname__}:inputs"
        outputs_key = f"{func.__qualname__}:outputs"
        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)
        print(f"{func.__qualname__} was called {len(inputs)} times:")
        for inp, out in zip(inputs, outputs):
            print(f"{func.__qualname__}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")

if __name__ == "__main__":
    cache = Cache()
    cache.store = cache.count_calls(cache.store)
    cache.store = cache.call_history(cache.store)
    cache.store(b"first")
    cache.store(b"second")
    cache.store(b"third")
    cache.replay(cache.store)