#!/usr/bin/env python3
"""Redis"""

import redis
import uuid
from typing import Union


class Cache:
    """Class"""

    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
            Union[str, bytes, int, float, None]: The retrieved data,
            optionally converted.
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
