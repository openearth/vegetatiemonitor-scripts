rm -rf ./map_tiles/classificatie_v2
gsutil -m cp -R gs://vegetatiemonitor/classificatie_v2 ./map_tiles/
python3 video_classificatie.py
