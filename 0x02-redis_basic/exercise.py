#!/usr/bin/env python3
"""
Cache module
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    '''Decorator to count method calls'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper to count method calls'''
        self.__redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''Decorator to store history of calls'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper to store history of calls'''
        input_data = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_data)
        output_data = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output_data)
        return output_data
    return wrapper


def replay(fn: Callable):
    '''Function to display history of calls'''
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print("{} was called {} times:".format(func_name, c))
    inputs = r.lrange("{}:inputs".format(func_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(func_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


class Cache:
    '''Cache class to interact with Redis'''
    def __init__(self):
        '''Initialize Redis client and flush database'''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()


    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store data in Redis and return key'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key


    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''Retrieve data from Redis'''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value


    def get_str(self, key: str) -> str:
        '''Retrieve string data from Redis'''
        value = self._redis.get(key)
        return value.decode("utf-8")


    def get_int(self, key: str) -> int:
        '''Retrieve integer data from Redis'''
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value