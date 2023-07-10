#!/bin/bash

rm -rf output
rm -rf storage

python3 yt-sum.py "$@"
