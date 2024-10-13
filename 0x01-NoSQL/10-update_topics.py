#!/usr/bin/env python3
""" 11th Task """


def update_topics(mongo_collection, name,
                  topics):
    """ List all documents in Python """
    mongo_collection.update_many({"name": name},
                                 {"$set": {"topics": topics}})
