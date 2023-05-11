import numpy as np
from aniposelib.boards import CharucoBoard, Checkerboard
from aniposelib.cameras import Camera, CameraGroup
from aniposelib.utils import load_pose2d_fnames

vidnames = [['C:/Code/pose2sim/Pose2Sim/230511_swing/calib-2d/cam0/20230511_041258_cam0.avi'],
            ['C:/Code/pose2sim/Pose2Sim/230511_swing/calib-2d/cam1/20230511_041258_cam1.avi']]

cam_names = ['cam0', 'cam1']

n_cams = len(vidnames)

board = Checkerboard(4, 5,
                     square_length=0.035, # unit: m
                     manually_verify=False)


# the videos provided are fisheye, so we need the fisheye option
cgroup = CameraGroup.from_names(cam_names, fisheye=False)


# this will take about 15 minutes (mostly due to detection)
# it will detect the charuco board in the videos,
# then calibrate the cameras based on the detections, using iterative bundle adjustment
cgroup.calibrate_videos(vidnames, board)

# if you need to save and load
# example saving and loading for later
cgroup.dump('calibration.toml')