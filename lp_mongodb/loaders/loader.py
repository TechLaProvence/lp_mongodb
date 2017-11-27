#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/TechLaProvence/lp_mongodb

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 figarocms dhardy@figarocms.fr

import base64
from pymongo import MongoClient
from bson.objectid import ObjectId

def __conn__(self):
    connection = MongoClient(
      self.context.config.MONGO_LP_SERVER_HOST,
      self.context.config.MONGO_LP_SERVER_PORT
    )
    db = connection[self.context.config.MONGO_LP_SERVER_DB]
    storage = db[self.context.config.MONGO_LP_SERVER_COLLECTION]

    return connection, db, storage

def load(self, url, callback):
    connection, db, storage = __conn__(self)
    try:
        document = storage.find_one({ '_id': ObjectId(url) }, { self.context.config.MONGO_LP_DOC_FIELD: True })
        file_data = base64.b64decode(document[self.context.config.MONGO_LP_DOC_FIELD])
        callback(file_data)
    except (KeyError, TypeError):
        callback(None)