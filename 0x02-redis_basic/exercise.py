#!/usr/bin/env python3
"""
Cache module
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

class Cache:
    """
    Cache class for storing data in Redis
    """
    def __init__(self) -> None:
        """Initialize Cache instance with Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """Decorator to count method calls"""
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis with the given key
        If fn is provided, apply the conversion function to the retrieved data
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve string data from Redis with the given key
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve integer data from Redis with the given key
        """
        return self.get(key, fn=int)

if __name__ == "__main__":
    cache = Cache()

    cache.store(b"first")
    print(cache.get("Cache.store"))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get("Cache.store"))