#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker"""
from functools import wraps
import redis
import requests
from typing import Callable

_redis = redis.Redis()


def count(method: Callable) -> Callable:
    """decorator to count """
    @wraps(method)
    def wrapper(url):
        count_key = f'count:{url}'
        _redis.incr(count_key)
        cached = _redis.get(f'{url}')

        if cached:
            return cached.decode('utf-8')
        content = method(url)
        _redis.set(f'{url}', content, 10)
        return content
    return wrapper


@count
def get_page(url: str) -> str:
    """get page content

    Args:
        url: str

    Returns:
        str(the page content)
    """
    content = requests.get(url)

    return content.text
