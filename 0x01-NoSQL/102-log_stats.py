#!/usr/bin/env python3
"""
Log stats - new version
"""
from pymongo import MongoClient


def get_nginx_stats(mongo_collection):
    """
    Queries nginx collection for specific data.

    Args:
        mongo_collection: pymongo collection object representing the nginx
        collection.

    Returns:
        tuple: A tuple containing:
            - The count of all documents in the collection.
            - A dictionary containing the count of each method in the collection.
            - A dictionary containing the top 10 most present IPs in the collection.
    """
    doc_count = mongo_collection.count_documents({})

    method_stats = {}
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = mongo_collection.count_documents({'method': method})
        method_stats[method] = method_count

    top_ips = {}
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    ip_results = mongo_collection.aggregate(pipeline)
    for ip_result in ip_results:
        top_ips[ip_result["_id"]] = ip_result["count"]

    return doc_count, method_stats, top_ips


def print_nginx_stats(doc_count, method_stats, top_ips):
    """
    Prints stats from nginx query.

    Args:
        doc_count (int): Total count of documents.
        method_stats (dict): Dictionary containing the count of each method.
        top_ips (dict): Dictionary containing the top 10 most present IPs.
    """
    print(f'{doc_count} logs')
    print('Methods:')
    for method, count in method_stats.items():
        print(f'\tmethod {method}: {count}')
    print('IPs:')
    for ip, count in top_ips.items():
        print(f'\t{ip}: {count}')


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    doc_count, method_stats, top_ips = get_nginx_stats(logs_collection)

    print_nginx_stats(doc_count, method_stats, top_ips)