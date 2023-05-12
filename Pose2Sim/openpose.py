import os.path as op
import os
from glob import glob
import toml

def run_openpose(cfg_path, cfg_dict=None):
    # params
    if cfg_path is None:
        openpose_path = cfg_dict['openpose_path']
        ext = cfg_dict['ext']
        video_dir = cfg_dict['video_dir']
        json_dir = cfg_dict['json_dir']
    
    else:
        cfg = toml.load(cfg_path)
        
        openpose_path = cfg.get('openpose').get('openpose_path')
        ext = cfg.get('openpose').get('vid_extension')
        project_dir = cfg.get('project').get('project_dir')
        
        rawImg_folder_dir = os.path.join(project_dir, cfg.get('project').get('rawImg_folder_name'))
        video_dir = os.path.join(rawImg_folder_dir, cfg.get('project').get('motion_name'))
        
        pose_folder_dir = os.path.join(project_dir, cfg.get('project').get('pose_folder_name'))
        json_dir = os.path.join(pose_folder_dir, cfg.get('project').get('motion_name'))
        
    cam_dir = glob(os.path.join(video_dir, 'cam*'))
    cwd = os.getcwd()
    
    # run openpose
    for cam in cam_dir:
        vidname = glob(os.path.join(cam, f'*.{ext}'))
        if len(vidname) == 0:
            print(f'No video file found in {cam}')
        else:
            print(f'Found {len(vidname)} video files in {cam}')
        vidname = os.path.realpath(vidname[0])
        
        json_subdir =  os.path.realpath(os.path.join(json_dir, os.path.basename(cam)))
        os.makedirs(json_dir, exist_ok=True)
        
        os.chdir(openpose_path)
        os.system(f"bin\OpenPoseDemo.exe --model_pose BODY_25B --video {vidname} --write_json {json_subdir}")
        os.chdir(cwd)


if __name__ == '__main__':
    cfg_path = './Config.toml'
    cfg_dict = {'openpose_path': 'C:/Code/openpose', 
                'video_dir': 'C:/Code/pose2sim/Pose2Sim/230511_swing/raw-2d/swing',
                'json_dir' : 'C:/Code/pose2sim/Pose2Sim/230511_swing/pose-2d/swing',
                'ext': 'avi'}
    
    run_openpose(cfg_path=cfg_path, cfg_dict=None)