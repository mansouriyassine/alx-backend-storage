import requests
import redis

def get_page(url: str) -> str:
    """
    Function to obtain the HTML content of a URL and cache it with expiration time.
    """
    r = redis.Redis()
    count_key = "count:{}".format(url)
    page_key = "page:{}".format(url)

    # Increment access count
    r.incr(count_key)

    # Check if page is cached
    cached_page = r.get(page_key)
    if cached_page:
        return cached_page.decode("utf-8")

    # Fetch page content
    response = requests.get(url)
    page_content = response.text

    # Cache page content with expiration time
    r.setex(page_key, 10, page_content)

    return page_content