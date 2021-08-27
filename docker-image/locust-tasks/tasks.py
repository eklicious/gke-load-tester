#!/usr/bin/env python

# This makes all the pymongo requests async by leveraging gevents
import gevent
print('using gevent my monkey patching')
_ = gevent.monkey.patch_all()

import pymongo
from bson import json_util
from bson.json_util import loads
from bson import ObjectId
from locust import User, events, task, constant, tag, between
import time

# Change the connection string to point to a correct db
mdbClient = pymongo.MongoClient("mongodb+srv://pentaho:pentaho@winvargo.6ngvd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&readPreference=secondary")
coll = mdbClient.sample_airbnb.listingsAndReviews

class MetricsLocust(User):
    # Set the wait time to be long enough so the Locust user can actually finish any of the operations, e.g. don't make Locust go too fast else it'll start to queue up too many gevent operations and will eventually cause the CPU to hit 100% and crash.
    wait_time = between(1, 1)

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
