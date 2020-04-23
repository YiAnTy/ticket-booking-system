#!/bin/bash

#docker build -t nameko/nameko-ticketservice:1.0.0 .
#docker run --name=ticket-service --network=host nameko/nameko-ticketservice:1.0.0
# Check if rabbit and redis are up and running before starting the service.


nameko run --config config.yml ticketservice.service --backdoor 3000