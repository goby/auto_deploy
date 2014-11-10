#!/bin/bash

nohup uwsgi -s 127.0.0.1:9999 --module deploy --callable app --enable-threads --py-autoreload 1 --catch-exceptions &

