#!/usr/bin/env python3
"""
Module containing function to list all documents in a collection
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection

    Args:
        mongo_collection: PyMongo collection object

    Returns:
        list: List of all documents in the collection
    """
    documents = mongo_collection.find({})
    
    return list(documents)