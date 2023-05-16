import numpy as np
import toml
import os
from glob import glob
import cv2

from aniposelib.boards import Checkerboard
from aniposelib.cameras import Camera, CameraGroup
from aniposelib.utils import load_pose2d_fnames
from Pose2Sim.common import rotate_cam

def calibrate_cams_all(cfg_path):
    cfg = toml.load(cfg_path)
    
    # get calibration folder
    project_dir = cfg.get('project').get('project_dir')
    calib_folder_name = cfg.get('project').get('calib_folder_name')
    calib_dir = os.path.join(project_dir, calib_folder_name)
    cam_dir = glob(os.path.join(calib_dir, 'cam*'))
    
    # get calibration parameters
    corners_nb = cfg.get('calibration').get('checkerboard').get('corners_nb') # [H,W]
    square_size = cfg.get('calibration').get('checkerboard').get('square_size') # unit: m
    show_corner_detection = cfg.get('calibration').get('checkerboard').get('show_corner_detection') 
    vid_extension = cfg.get('calibration').get('checkerboard').get('vid_extension')
    
    vidnames = []
    cam_names = []
    # check video files and camera names
    for cam in cam_dir:
        vidname = glob(os.path.join(cam, f'*.{vid_extension}'))
        if len(vidname) == 0:
            print(f'No video file found in {cam}')
        else:
            print(f'Found {len(vidname)} video files in {cam}')
        vidnames.append([vidname[0]])
        cam_names.append(os.path.basename(cam)) # cam name is the folder name       
    
    n_cams = len(vidnames)
    board = Checkerboard(corners_nb[0], corners_nb[1],
                        square_length=square_size, # unit: m
                        manually_verify=show_corner_detection)


    # the videos provided are fisheye, so we need the fisheye option
    cgroup = CameraGroup.from_names(cam_names, fisheye=False)

    # this will take about 15 minutes (mostly due to detection)
    # it will detect the charuco board in the videos,
    # then calibrate the cameras based on the detections, using iterative bundle adjustment
    cgroup.calibrate_videos(vidnames, board)
    
    # for cam in cgroup.cameras:
    #     rvec = cam.rvec
    #     tvec = cam.tvec
        
    #     RT = rotate_cam(rvec, tvec, ang_x=-np.pi/2, ang_y=0, ang_z=0)
    #     R = RT[0]
    #     T = RT[1]
    #     R_ = np.array(cv2.Rodrigues(R)).flatten()
    #     # R_ = [np.array(cv2.Rodrigues(r)[0]).flatten() for r in R]
    

    # if you need to save and load
    # example saving and loading for later
    save_path = os.path.join(calib_dir, 'Calib_checkerboard.toml')
    cgroup.dump(save_path)

if __name__ == '__main__':
    cfg_path = './Config.toml'
    calibrate_cams_all(cfg_path)