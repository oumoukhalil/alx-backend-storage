#!/usr/bin/env python3
import uuid 
import redis
from typing import Optional, Callable, Union

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
            
