#!/bin/sh
apk --update --no-cache add curl mc dropbear

mkdir -p /tmp/archives/
tar -cpzf "/tmp/archives/backdoor.tar.gz" --exclude tmp --exclude dev --exclude sys --exclude proc /
