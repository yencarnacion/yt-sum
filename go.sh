#!/bin/bash

rm -rf output/output.html
rm -rf storage

python3 yt-sum.py "$@"
