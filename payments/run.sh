#!/bin/bash
#docker build -t nameko/nameko-paymentservice:1.0.0 .
#docker run --name=payment-service --network=host nameko/nameko-paymentservice:1.0.0
# Check if rabbit and redis are up and running before starting the service.


nameko run --config config.yml paymentservice.service --backdoor 3000