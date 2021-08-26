#!/usr/bin/env python

import gevent
print('using gevent my monkey patching')
_ = gevent.monkey.patch_all()

import pymongo
from bson import json_util
from bson.json_util import loads
from bson import ObjectId
from locust import User, events, task, constant, tag
import time

mdbClient = pymongo.MongoClient("mongodb+srv://pentaho:pentaho@winvargo.6ngvd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&readPreference=secondary")
coll = mdbClient.sample_airbnb.listingsAndReviews

class MetricsLocust(User):
    @task(1)
    def _async_find(self):
        try:
            tic = time.time();
            # Get the record from the TEST collection now
            coll.find_one({}, {"_id":1})
            events.request_success.fire(request_type="pymongo", name="singleFetch", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            gevent.sleep(0)
        except Exception as e:
            print(f'Exception: '
                  f'{str(e)}')
