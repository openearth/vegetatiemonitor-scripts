#!/bin/sh
gsutil -m cp -R gs://vegetatiemonitor/classificatie_v2 ./map_tiles
python3 ./video_classificatie_v2-test.py
gsutil -m cp -R ./map_tiles/classificatie_v2-video gs://vegetatiemonitor
