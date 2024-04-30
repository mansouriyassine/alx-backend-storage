#!/usr/bin/env python3
"""
Cache module for Redis operations.
"""

import redis
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

CacheData = Union[str, bytes, int, float]

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count method calls.
        """
        method_name = method.__qualname__
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of method calls.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store method call history.
        """
        method_name = method.__qualname__
        inputs_key = f"{method_name}:inputs"
        outputs_key = f"{method_name}:outputs"
        self._redis.rpush(inputs_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(result))
        return result
    return wrapper

class RedisCache:
    """
    Redis Cache class for storing and retrieving data.
    """

    def __init__(self) -> None:
        """
        Initialize the Redis connection and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: CacheData) -> str:
        """
        Store data in Redis and return a unique key for retrieval.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def retrieve(self, key: str,
                 convert_fn: Optional[Callable] = None) -> CacheData:
        """
        Retrieve data from Redis using the specified key.
        Optionally, apply a conversion function to the retrieved data.
        """
        data = self._redis.get(key)
        if convert_fn:
            return convert_fn(data)
        return data

    def replay(self, method_name: str) -> None:
        """
        Replay the history of method calls and their outputs.
        """
        inputs_key = f"{method_name}:inputs"
        outputs_key = f"{method_name}:outputs"
        inputs = self._redis.lrange(inputs_key, 0, -1)
        outputs = self._redis.lrange(outputs_key, 0, -1)
        print(f"{method_name} was called {len(inputs)} times:")
        for method_input, method_output in zip(inputs, outputs):
            print(f"{method_name}({method_input}) -> {method_output}")