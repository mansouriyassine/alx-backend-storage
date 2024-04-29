#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def nginx_log_stats():
    """
    Function to retrieve stats about Nginx logs
    """
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    method_counts = {}
    for method in http_methods:
        count = collection.count_documents({'method': method})
        method_counts[method] = count

    status_check_count = collection.count_documents({
        'method': 'GET',
        'path': '/status'
        })

    # Top 10 IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = collection.aggregate(pipeline)

    client.close()

    return total_logs, method_counts, status_check_count, top_ips


def print_nginx_stats():
    """
    Function to print stats about Nginx logs
    """
    total_logs, method_counts, status_check_count, top_ips = nginx_log_stats()

    print(f"{total_logs} logs")

    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")

    print(f"{status_check_count} status check")

    print("IPs:")
    for ip_data in top_ips:
        ip = ip_data["_id"]
        count = ip_data["count"]
        print(f"\t{ip}: {count}")


if __name__ == "__main__":
    print_nginx_stats()