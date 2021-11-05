import os
import subprocess
from glob import glob
from shutil import copyfile

# vegetation monitor video frame maps are exported using: https://code.earthengine.google.com?scriptPath=users/cindyvdvries/vegetatiemonitor:2019-testing/export-satellite-maps-for-video

# use the following parameters when exporting tiles from EE:
#    Export.map.toCloudStorage({
#      image: image,
#      description: description,
#      bucket: 'deltares-video-tiles',
#      fileFormat: 'png',
#      path: 'test-timelapse/' + year.toString(),
#      minZoom: 5,
#      maxZoom: 14,
#      region: reigon,
#      skipEmptyTiles: true
#    })



# download from storage example:
# gsutil cp -r gs://vegetatiemonitor/classificatie D:/video-map/vegetatiemonitor/

def run(cmd):
    print(cmd)
    subprocess.run(cmd)
# folders = ['classificatie', 'ndvi', 'satellite-false', 'satellite-natural']
bucket_name = os.path.abspath("map_tiles")
folder = "classificatie-vs-legger"
temp_dir = "temp1"
video_folder = folder+"-video"

steps = glob(f'{bucket_name}/{folder}/*')
print('steps', steps)

zoom_levels = range(5, 15)

print('zoom_levels', zoom_levels)

if not os.path.exists(r'{0}/{1}'.format(bucket_name, temp_dir)):
    os.mkdir(r'{0}/{1}'.format(bucket_name, temp_dir))

new_file_list = []
for i, step in enumerate(steps):
    print(i, step)
    print("Converting step: {}".format(step))
    for zoom in zoom_levels:
        zoom_dir =  r'{2}/{3}'.format(bucket_name, folder, step, zoom)
        tile_x_list = os.listdir(zoom_dir)
        for tile_x in tile_x_list:
            tile_x_dir = r'{0}/{1}'.format(zoom_dir, tile_x)
            tile_y_list = os.listdir(tile_x_dir)
            # copy to
            for tile_y in tile_y_list:
                tile_y_no_ext = os.path.splitext(tile_y)[0]
                tile_y_dir = r'{0}/{1}'.format(tile_x_dir, tile_y)
                new_path = r'{0}/{1}/{2}/{3}/{4}'.format(bucket_name, temp_dir, zoom, tile_x, tile_y_no_ext)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_file = r'/{:03d}.png'.format(i+1)
                # os.rename(tile_y_dir, new_path+new_file)
                copyfile(tile_y_dir, new_path + new_file)

for zoom in zoom_levels:
    zoom_dir = r'{0}/{1}/{2}'.format(bucket_name, temp_dir, zoom)
    tile_x_list = os.listdir(zoom_dir)
    for tile_x in tile_x_list:
        tile_x_dir = r'{0}/{1}'.format(zoom_dir, tile_x)
        tile_y_list = os.listdir(tile_x_dir)
        os.chdir(tile_x_dir)
        # move to
        for tile_y in tile_y_list:
            new_path = r'{0}/{1}/{2}/{3}'.format(bucket_name, video_folder, zoom, tile_x)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            # make sure we get keyframe every frame
            # see https://stackoverflow.com/questions/24152810/encoding-ffmpeg-to-mpeg-dash-or-webm-with-keyframe-clusters-for-mediasource/37776212
            cmd = 'ffmpeg -framerate 10 -i "{0}/{1}/%03d.png" -c:v libvpx -keyint_min 1 -cluster_size_limit 10M -cluster_time_limit 2100 -g 1 -an -qmin 0 -qmax 30 -crf 5 -auto-alt-ref 0 {2}/{1}.webm -y'.format(tile_x_dir, tile_y, new_path)
            cmd = cmd.split(' ')
            run(cmd)

# upload to storage example:
# run("gsutil cp -r D:/video-map/vegetatiemonitor/classificatie-video gs://vegetatiemonitor")
