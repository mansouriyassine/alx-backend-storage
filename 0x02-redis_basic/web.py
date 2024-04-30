#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
import time
from functools import wraps

# Initialize Redis connection
redis_conn = redis.Redis()

def track_access(func):
    """
    Decorator to track the number of times a URL is accessed
    """
    @wraps(func)
    def wrapper(url):
        key = f"count:{url}"
        redis_conn.incr(key)
        return func(url)
    return wrapper

def cache_page(expiration=10):
    """
    Decorator to cache the result of a function with expiration time
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            key = f"cache:{url}"
            cached_content = redis_conn.get(key)
            if cached_content:
                return cached_content.decode('utf-8')
            else:
                content = func(url)
                redis_conn.setex(key, expiration, content)
                return content
        return wrapper
    return decorator

@track_access
@cache_page()
def get_page(url: str) -> str:
    """
    Retrieve HTML content of a URL and cache it with an expiration time
    """
    response = requests.get(url)
    return response.text