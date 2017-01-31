#!/bin/bash

envsubst </rawfiles/index-media.py >/bin/index-media.py
chmod +x /bin/index-media.py
envsubst </rawfiles/crontab > /rawfiles/crontab.subst
crontab /rawfiles/crontab.subst

exec "$@"
