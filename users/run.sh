#!/bin/bash

#docker build -t nameko/nameko-userservice:1.0.0 .
#docker run --name=user-service --network=host nameko/nameko-userservice:1.0.0
# Check if rabbit is up and running before starting the service.

# Run Service

nameko run --config config.yml userservice.service --backdoor 3000
