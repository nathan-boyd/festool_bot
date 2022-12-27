# festool recon site checker

### build
```
docker build . -t festool_bot
```

### run
```
docker run -d \
    -e PUSHOVER_APP_TOKEN="" \
    -e PUSHOVER_USER_KEY="" \
    -e STATE_FILE_PATH=/festool_state.txt \
    -v /tmp/festool_state.txt:/festool_state.txt \
    --name festool_watcher \
    --restart unless-stopped \
    festool_bot:latest
```

### run
```
PUSHOVER_APP_TOKEN="" PUSHOVER_USER_KEY="" STATE_FILE_PATH=/tmp/festool_state.txt python3 check_site.py
```
