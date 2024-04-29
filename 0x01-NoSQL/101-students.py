#!/usr/bin/env python3
"""
Top students
"""
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    
    Args:
        mongo_collection: pymongo collection object representing the students
        collection.
    
    Returns:
        list: A list of student documents sorted by average score in descending
        order.
    """
    students = list(mongo_collection.find({}))
    
    for student in students:
        total_score = sum(topic['score'] for topic in student['topics'])
        average_score = total_score / len(student['topics'])
        student['averageScore'] = average_score
    
    get_average_score = lambda x: x['averageScore']
    
    sorted_students = sorted(students, key=get_average_score, reverse=True)
    
    return sorted_students