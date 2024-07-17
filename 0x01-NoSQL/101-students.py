#!/usr/bin/env python3
"""Top students"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        List of students with their average score included and sorted by
        average score.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    students = list(mongo_collection.aggregate(pipeline))

    return students
