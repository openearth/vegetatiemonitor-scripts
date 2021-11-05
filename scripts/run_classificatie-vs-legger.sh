#!/bin/sh
gsutil -m cp -R gs://vegetatiemonitor/classificatie-vs-legger ./map_tiles
python3 ./video_classificatie-vs-legger-test.py
gsutil -m cp -R ./map_tiles/classificatie-vs-legger-video gs://vegetatiemonitor
