#!/usr/bin/env python3
"""
Module containing function to update topics of a school document
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name

    Args:
        mongo_collection: PyMongo collection object
        name (str): The school name to update
        topics (list of str): The list of topics approached in the school

    Returns:
        None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})