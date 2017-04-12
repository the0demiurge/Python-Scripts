import os
import sys
path_in, path_out = sys.argv[1:3]

for dirs in os.listdir(path_in):  # 1,2,3
    for file_in in os.listdir('{}/{}'.format(path_in, dirs)):
        os.makedirs('{}/{}'.format(path_out, dirs), exist_ok=True)
        os.system('ffmpeg -i {0}/{2}/{3}  -vcodec libx264 -preset fast -crf 25 -y -acodec libmp3lame -ab 128k {1}/{2}/{4}.mp4 -threads 4'.format(
            path_in, path_out, dirs, file_in, file_in[3: 6]))
