Instructions: https://cloud.google.com/architecture/distributed-load-testing-using-gke

Notes you should read before you go through the instructions:
Create a google cloud project and then select the project before you proceed with instructions above.
Clone my github rather than the sample repo in the instructions above because I modified locust to be 2.1.0 and python 3.8.2 and other dependencies.
You don't need to deploy the sample App Engine web application since I commented out all the logic for posting data to the app.
Keep in mind that the instructions have a hard limit for the GKE cluster max nodes. If you are testing beyond that, pick a larger max node number.
Also keep in mind that the number of worker replicas is set to 5 by default. You can update that accordingly.

Handy commands:
kubectl exec -ti <pod name> -- /bin/sh
Scale workers down to 0 and upscale to pick up new container images: kubectl scale deployment/locust-worker --replicas=0

