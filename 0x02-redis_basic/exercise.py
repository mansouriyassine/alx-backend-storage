#!/usr/bin/env python3
"""
Cache module for Redis operations.
"""

import redis
import uuid
from typing import Union
from functools import wraps

class Cache:
    """
    Cache class for Redis operations.
    """

    def __init__(self) -> None:
        """
        Initializes a Redis client and flushes the instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis with a randomly generated key.

        Args:
            data: The data to be stored.

        Returns:
            The randomly generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn=None):
        """
        Retrieves the value associated with the given key from Redis.

        Args:
            key: The key to retrieve the value for.
            fn: Optional callable to convert the data back to desired format.

        Returns:
            The retrieved value.
        """
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves the value associated with the given key from Redis as a string.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The retrieved value as a string.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves the value associated with the given key from Redis as an integer.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The retrieved value as an integer.
        """
        return self.get(key, fn=int)

    def count_calls(method):
        """
        Decorator to count the number of times a method is called.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    def call_history(method):
        """
        Decorator to store the history of inputs and outputs for a function.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs_key = "{}:inputs".format(method.__qualname__)
            outputs_key = "{}:outputs".format(method.__qualname__)

            self._redis.rpush(inputs_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(outputs_key, str(output))

            return output
        return wrapper

    def replay(method):
        """
        Function to display the history of calls of a particular function.
        """
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        inputs = method._redis.lrange(inputs_key, 0, -1)
        outputs = method._redis.lrange(outputs_key, 0, -1)

        print("{} was called {} times:".format(method.__qualname__, len(inputs)))

        for args, output in zip(inputs, outputs):
            print("{}(*{}) -> {}".format(method.__qualname__, args, output))

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis with a randomly generated key.

        Args:
            data: The data to be stored.

        Returns:
            The randomly generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis with a randomly generated key.

        Args:
            data: The data to be stored.

        Returns:
            The randomly generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

if __name__ == "__main__":
    cache = Cache()

    # Task 0: Writing strings to Redis
    data = b"hello"
    key = cache.store(data)
    print(key)
    print(cache._redis.get(key))

    # Task 1: Reading from Redis and recovering original type
    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

    # Task 2: Incrementing values
    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))

    # Task 3: Storing lists
    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("secont")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))

    # Task 4: Retrieving lists
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    cache.replay(cache.store)