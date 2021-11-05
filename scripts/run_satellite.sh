#!/bin/sh
gsutil -m cp -R gs://vegetatiemonitor/satellite-natural ./map_tiles
python3 ./video_satellite-natural.py
gsutil -m cp -R ./map_tiles/satellite-natural-video gs://vegetatiemonitor
