#!/usr/bin/env python3
"""This module covers finding documents in MongoDB"""


def list_all(mongo_collection):
    """Lists all documents.

    Args:
        MongoDB collection.

    Returns:
        A List of all documents in MongoDB, or empty list if no document found
    """
    return list(mongo_collection.find())
