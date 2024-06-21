#!/usr/bin/env python3
import uuid 
import redis
from typing import Optional, Callable, Union
from functools import wraps


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