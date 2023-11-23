#!/bin/bash

# 1. Modify the probability in app.py.

# 2. Rebuild the docker image.
docker build -t kingdo/eva5:latest .

# 3. Start services by docker-compose.
docker-compose up -d

# 4.use hey to test the service.
hey -c 1 -n 100  -m GET  http://127.0.0.1:20080