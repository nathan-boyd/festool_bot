#!/bin/bash

env >> /etc/environment

cron && tail -f /var/log/cron.log
