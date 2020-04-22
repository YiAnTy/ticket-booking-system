#!/bin/bash

# Check if rabbit and redis are up and running before starting the service.


nameko run --config config.yml paymentservice.service --backdoor 3000