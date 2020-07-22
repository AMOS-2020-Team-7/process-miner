#!/bin/sh
# this sets the production environments backend access data from environment variables
sed -i 's/###BACKEND_HOST###/'$BACKEND_HOST'/g' src/environments/environment.prod.ts
sed -i 's/###BACKEND_PORT###/'$BACKEND_PORT'/g' src/environments/environment.prod.ts
