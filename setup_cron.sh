#!/bin/bash

# 0 3 * * * docker-compose up -d parser
(crontab -l 2>/dev/null; echo "0 3 * * * docker-compose up -d parser") | crontab -