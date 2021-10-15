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

########################################################################
# Global Static Variables that can be accessed without referencing self
########################################################################
# Change the connection string to point to a correct db and double check the readpreference etc.
mdbClient = pymongo.MongoClient("mongodb+srv://<username>:<password>@<srv>/myFirstDatabase?retryWrites=true&w=majority&readPreference=secondaryPreferred")
coll = mdbClient.sample_airbnb.listingsAndReviews

class MetricsLocust(User):
    # Set the wait time to be long enough so the Locust user can actually finish any of the operations, e.g. don't make Locust go too fast else it'll start to queue up too many gevent operations and will eventually cause the CPU to hit 100% and crash.
    wait_time = between(1, 1)

    # Helper function that is not a Locust task. All Locust tasks require the @task annotation
    # Note that you have to pass the self reference for all helper functions
    def get_time(self):
        return time.time()
    
    @task(1)
    def _async_find(self):
        try:
            # Note that you don't pass in self despite the signature above
            tic = get_time();
            
            # Get the record from the TEST collection now
            coll.find_one({}, {"_id":1})
            events.request_success.fire(request_type="pymongo", name="singleFetch", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            gevent.sleep(0)
        except Exception as e:
            print(f'Exception: '
                  f'{str(e)}')
