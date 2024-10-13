#!/usr/bin/env python3
""" 13th Task """
from pymongo import MongoClient


if __name__ == "__main__":
    """ Main Task """
    database = "logs"
    collection = "nginx"
    client = MongoClient('mongodb://127.0.0.1:27017')
    methods_mapping = {}
    logs_collection = client[database][collection]
    logs = logs_collection.find()
    logs_count = logs_collection.count_documents({})
    print(f"{logs_count} logs")
    print("Methods:")
    for log in logs:
        method = log.get("method")
        if method not in methods_mapping:
            methods_mapping[method] = 0
        methods_mapping[method] += 1

    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print(f"\tmethod {method}: {methods_mapping.get(method, 0)}")
    status_check_count = logs_collection.count_documents({
        "method": "GET",
        "path": "/status"
    })
    print(f"{status_check_count} status check")
