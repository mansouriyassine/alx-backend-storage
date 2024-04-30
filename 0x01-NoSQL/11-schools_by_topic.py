#!/usr/bin/env python3
"""
Module containing function to find schools by topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic

    Args:
        mongo_collection: PyMongo collection object
        topic (str): The topic to search for

    Returns:
        list: List of schools having the specified topic
    """
    schools = mongo_collection.find({"topics": topic})
    
    return list(schools)