#!/usr/bin/env python3
""" Task 1 """
from typing import Callable, Optional, Union
import uuid
import redis
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function"""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ gets args, output """
        # Don't assign args to another variable
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Creates and returns function that increments the count \
        for that key every time the method is called and returns \
        the value returned by the original method"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Increments count """
        name = method.__qualname__
        # Don't assign args to another variable
        self._redis.incr(name)
        return method(self, *args, **kwargs)
    return wrapper


def replay(fn: Callable):
    """display the history of calls of a particular function"""
    method_name = fn.__qualname__
    # redis_instance = fn.__self__._redis
    redis_instance = redis.Redis()
    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"
    count = redis_instance.get(method_name)
    if count is not None:
        count = int(count)
        IOTuple = zip(redis_instance.lrange(input_key, 0, -1),
                      redis_instance.lrange(output_key, 0, -1))
        print(f"{method_name} was called {count} times:")
        for inp, outp in list(IOTuple):
            input, output = inp.decode("utf-8"), outp.decode("utf-8")
            print(f"{method_name}(*{input}) -> {output}")


class Cache:
    """Cache class"""

    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key (e.g. using uuid),
        store the input data in Redis using the random key
        and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, float]:
        """ gets value and converts it to the desired format"""
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        elif value is not None:
            return value

    def get_str(self, key: str) -> str:
        """get string"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """get int"""
        return self.get(key, int)
