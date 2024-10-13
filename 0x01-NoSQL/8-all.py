#!/usr/bin/env python3
""" 9th Task """


def list_all(mongo_collection):
    """ List all documents in Python """
    return mongo_collection.find()
