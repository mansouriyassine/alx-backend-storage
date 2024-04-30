#!/usr/bin/env python3
"""
Module containing function to insert a new document in a collection
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs

    Args:
        mongo_collection: PyMongo collection object
        **kwargs: Key-value pairs representing the fields of the document to be inserted

    Returns:
        str: The _id of the newly inserted document
    """
    return mongo_collection.insert_one(kwargs).inserted_id