import os.path as op
import os
import sys
from glob import glob
import subprocess

# params
openpose_path = "C:/Code/openpose"
video_dir = "C:/Code/pose2sim/Pose2Sim/230511_swing/raw-2d"
ext = "avi"
display = 0

os.chdir(openpose_path)

video_files = glob(video_dir + f'/*.{ext}')
for video_path in video_files:
    json_path = op.join(video_dir, op.splitext(op.basename(video_path))[0])
    # print(f"bin/OpenPoseDemo.exe --model_pose BODY_25B --video {video_path} --write_json {json_path}")
    
    os.system(f"bin\OpenPoseDemo.exe --model_pose BODY_25B --video {video_path} --write_json {json_path}")
    