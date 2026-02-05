#!/bin/sh
# Start Next.js in background on port 3000
PORT=3000 node server.js &
# Start Nginx in foreground on port 8080 (Cloud Run default)
nginx -g "daemon off;"
