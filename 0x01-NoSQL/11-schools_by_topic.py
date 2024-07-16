#!/usr/bin/env python3
"""This module covers searching schools based on topic"""


def schools_by_topic(mongo_collection, topic):
    """Searches the given topic and returns the schools of the matched topic.

    Args:
        moonmongo_collection (MongoDB collection): the school collection
        created in the MongoDB database.

        topic (string): The topic to be searched in schools.

    Returns:
        The list of school having a specific topic."""
    return mongo_collection.find({'topics': topic})
