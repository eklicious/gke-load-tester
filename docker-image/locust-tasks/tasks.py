#!/usr/bin/env python

import gevent
print('using gevent my monkey patching')
_ = gevent.monkey.patch_all()

import pymongo
from bson import json_util
from bson.json_util import loads
from bson import ObjectId
from locust import HttpUser, events, task, constant, tag
import time

class MetricsLocust(HttpUser):
    mdbClient = pymongo.MongoClient("mongodb+srv://ek:ek@demo.nndb3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&readPreference=secondary")
    coll = mdbClient.sample_airbnb.listingsAndReviews

    # Start logic per user
    # def on_start(self):
    # self._deviceid = str(uuid.uuid4())

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        print("A new test is starting")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print("A new test is ending")

    def _async_find(self, timeout=600):
        try:
            tic = time.time();
            # Get the record from the TEST collection now
            doc = self.coll.find_one({})
            events.request_success.fire(request_type="pymongo", name="singleFetch", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            gevent.sleep(0)
        except Exception as e:
            print(f'DB-CONNECTION-PROBLEM: '
                  f'{str(e)}')
            connect_problem = True

    @task(1)
    def test(self):
        # If we don't sleep, locust tries to launch as many greenlets as possible which will crash the machine
        # Ideally, we'll sleep less than the overall avg execution time, e.g. <2ms.
        gevent.sleep(0.004)
        gevent.spawn(self._async_find)
