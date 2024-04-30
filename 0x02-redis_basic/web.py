#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from functools import wraps

# Establish Redis connection
cache_store = redis.Redis()

def track_url_access(func):
    """Decorator to track URL access"""
    @wraps(func)
    def wrapper(url):
        """Wrapper function to track URL access"""
        cached_key = "cached:" + url
        cached_data = cache_store.get(cached_key)
        
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html_content = func(url)

        cache_store.incr(count_key)
        cache_store.set(cached_key, html_content)
        cache_store.expire(cached_key, 10)

        return html_content

    return wrapper

@track_url_access
def fetch_web_page(url: str) -> str:
    """Retrieve HTML content of a URL"""
    response = requests.get(url)
    return response.text