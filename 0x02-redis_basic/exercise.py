#!/usr/bin/env python3
"""Redis"""

import redis
import uuid
from typing import Union, Optional, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method with call counting.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count and calls the
        original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a
    particular function.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method with input/output history storage.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores inputs and outputs history and calls
        the original method.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The function to replay the call history for.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    redis_instance = method.__self__._redis
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """Cache class"""
    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
            str, bytes, int, float, None]:
        """
        Retrieve the data from Redis and optionally apply a conversion
        function.

        Args:
            key (str): The key to retrieve from Redis.
            fn (Optional[Callable]): The function to convert the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally
            converted.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[str]: The retrieved string value.
        """
        data = self.get(key, lambda d: d.decode('utf-8'))
        return data

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[int]: The retrieved integer value.
        """
        data = self.get(key, int)
        return data
