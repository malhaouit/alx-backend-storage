#!/usr/bin/env python3
"""This script provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""

    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx = db.nginx

    total_logs = nginx.count_documents({})
    print("{} logs".format(total_logs))

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = nginx.count_documents({'method': method})
        print("    method {}: {}".format(method, method_count))

    number = nginx.count_documents({'path': '/status', 'method': 'GET'})
    print("{} status check".format(number))


if __name__ == "__main__":
    log_stats()
