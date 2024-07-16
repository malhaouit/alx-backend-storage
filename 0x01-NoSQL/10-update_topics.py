#!/usr/bin/env python3
"""This module covers updating a matched document"""


def update_topics(mongo_collection, name, topics):
    """Updates all topics of a school document based on the name

    Args:
        mongo_collection (MongoDB collection): the school collection created
        in MongoDB database.
        name (String): The name of the school.
        topics (List): The list of all topics covered in the school.

    Returns:
        None"""
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
