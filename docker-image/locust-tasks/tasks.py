#!/usr/bin/env python

import pymongo
from bson import json_util
from bson.json_util import loads
from bson import ObjectId
from locust import HttpUser, task, constant, tag
import time

class MetricsLocust(HttpUser):
    client = pymongo.MongoClient("mongodb+srv://<user>:<pwd>@demo.nndb3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&readPreference=secondary")
    coll = client.sample_airbnb.listingsAndReviews

    # def on_start(self):
    #     self._deviceid = str(uuid.uuid4())

    @task(1)
    def login(self):
        try:
            tic = time.time();
            # Get the record from the TEST collection now
            doc = self.coll.find_one({})
            self.environment.events.request_success.fire(request_type="pymongo", name="singleFetch", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'DB-CONNECTION-PROBLEM: '
                  f'{str(e)}')
            connect_problem = True

    # @task(999)
    # def post_metrics(self):
    #     self.environment.events.request_success.fire(request_type="pymongo", name="post_metrics", response_time=0, response_length=0)
        # self.client.post(
        #     "/metrics", {"deviceid": self._deviceid, "timestamp": datetime.now()})
