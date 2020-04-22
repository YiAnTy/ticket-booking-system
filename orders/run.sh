#!/bin/bash
#docker run --name=order-service --network=host nameko/nameko-orderservice:1.0.0
# Run Service

nameko run --config config.yml orderservice.service --backdoor 3000
