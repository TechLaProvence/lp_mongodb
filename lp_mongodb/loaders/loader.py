#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/TechLaProvence/lp_mongodb

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 figarocms dhardy@figarocms.fr

import base64
import gridfs
from pymongo import MongoClient
from bson.objectid import ObjectId
from tornado.concurrent import return_future

def __conn__(self):
    connection = MongoClient(
      self.context.config.MONGO_LP_SERVER_HOST,
      self.context.config.MONGO_LP_SERVER_PORT
    )
    db = connection[self.context.config.MONGO_LP_SERVER_DB]
    storage = db[self.context.config.MONGO_LP_SERVER_COLLECTION]

    return connection, db, storage

@return_future
def get(self, path, callback):
    connection, db, storage = self.__conn__()

    stored = storage.find_one({'path': path})

    if not stored or self.__is_expired(stored):
        callback(None)
        return

    fs = gridfs.GridFS(db)

    contents = fs.get(stored['file_id']).read()

    callback(str(contents))
