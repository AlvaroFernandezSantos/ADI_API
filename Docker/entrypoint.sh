#!/bin/bash

cd /home/authService
pip install -r requirements.txt
pip install .
authService_server -a admin -p 3001 -l 172.17.0.2 -d test.db
