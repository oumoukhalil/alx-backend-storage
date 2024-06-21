#!/usr/bin/env python3
import uuid 
import redis
from typing import Optional, Callable, Union
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """count number time of calling cache method"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ call history"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs = f"{method.__qualname__}:input"
        outputs = f"{method.__qualname__}:output"
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """function to display the history of calls of a particular function.
    Args:
        method: the function to display its history
    Returns:
         None
    """
    Cache = redis.Redis()
    name = method.__qualname__
    calls = Cache.get(name).decode("utf-8")
    input_key = f"{name}:input"
    output_key = f"{name}:output"
    inputs = Cache.lrange(input_key, 0, -1)
    outputs = Cache.lrange(output_key, 0, -1)
    print(f"{name} was called {calls} times:")

    for i, o in zip(inputs, outputs):
        print(f"{name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")
class Cache :
    """class cach to to store cache"""
    def __init__(self):
        """constructor 
        _redis:private instance of redis
        fulschdb:to delete all in te db"""
        self._redis = redis.Redis()
        self._redis.flushdb()
        
    def store(self,data: Union[str,bytes,float,int]) ->str:
        """store to store with a random key
        data str: bytes,int ,float"""
        key = str(uuid.uuid4())
        self._redis.set(key,data)
        return key

    def get(self,key: str,fn: Optional [Callable] = None )-> Union [str,float,bytes, int,None]:
        """methode to get data  by the key"""
        data=self._redis.get(key)
        if fn is not None:
            data = fn(data)
            return data
        def get_str(self, key: str) -> str:
            
       	 """get cache in string"""
        data = self.get(key)
        
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """get cache in int"""
        data = self.get(key)
        try:
            data = int(data.decode("utf-8"))
        except Exception:
            data = 0

        return data

