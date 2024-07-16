#!/usr/bin/env python3
"""This module covers insertion of a document to MongoDB in Python"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document to MongoDB.

    Args:
        mongo_collection (MongoDB collection): This the an existing collection
        in MongoDB server.

        kwargs (keyword arguments): These are the keyword arguments passed as
        parameters.

    Returns:
        The new inserted id to the database."""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
