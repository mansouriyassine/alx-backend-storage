#!/usr/bin/env python3
"""
Nginx Log Statistics
"""

from pymongo import MongoClient
from typing import Tuple


def get_nginx_statistics() -> Tuple:
    """
    Queries the nginx collection for specific data
    - Returns:
        - Total count of log documents
        - Counts of each HTTP method in the collection
        - Count of GET calls to /status path
    """
    client: MongoClient = MongoClient()
    db = client.logs
    collection = db.nginx
    http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    method_counts = []
    for method in http_methods:
        count = collection.count_documents({'method': method})
        method_counts.append({'method': method, 'count': count})
    total_count = collection.estimated_document_count()
    status_check_count = collection.count_documents({
        'method': 'GET',
        'path': '/status'
        })
    client.close()
    return total_count, method_counts, status_check_count


def print_nginx_statistics() -> None:
    """
    Prints statistics from nginx log queries
    """
    total_count, method_counts, status_check_count = get_nginx_statistics()
    print(f'Total logs: {total_count}')
    print('HTTP Methods:')
    for method in method_counts:
        print(f'\t{method.get("method")}: {method.get("count")}')
    print(f'GET /status requests: {status_check_count}')


if __name__ == '__main__':
    print_nginx_statistics()