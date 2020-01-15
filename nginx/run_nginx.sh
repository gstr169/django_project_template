#!/bin/bash
export DOLLAR='$'
envsubst < /code/nginx.conf > /etc/nginx/conf.d/nginx.conf
nginx -g "daemon off;"