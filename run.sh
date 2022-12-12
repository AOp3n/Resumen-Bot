#!/bin/sh
#/etc/init.d/apache2 start
python3 -m http.server 10000 &
python3 -m main
