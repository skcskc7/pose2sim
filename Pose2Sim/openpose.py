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
        model_pose = cfg_dict['model_pose']
    
    else:
        cfg = toml.load(cfg_path)
        
        openpose_path = cfg.get('openpose').get('openpose_path')
        ext = cfg.get('openpose').get('vid_extension')
        project_dir = cfg.get('project').get('project_dir')
        
        rawImg_folder_dir = os.path.join(project_dir, cfg.get('project').get('rawImg_folder_name'))
        video_dir = os.path.join(rawImg_folder_dir, cfg.get('project').get('motion_name'))
        
        pose_folder_dir = os.path.join(project_dir, cfg.get('project').get('pose_folder_name'))
        json_dir = os.path.join(pose_folder_dir, cfg.get('project').get('motion_name'))
        
        model_pose = cfg.get('openpose').get('model_pose')
        
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
        os.system(f"bin\OpenPoseDemo.exe --model_pose {model_pose} --video {vidname} --write_json {json_subdir}")
        os.chdir(cwd)


if __name__ == '__main__':
    cfg_path = './Config.toml'
    cfg_dict = {'openpose_path': 'C:/Code/openpose', 
                'video_dir': 'C:/Code/pose2sim/Pose2Sim/230511_swing_0deg_opps18/raw-2d/swing1',
                'json_dir' : 'C:/Code/pose2sim/Pose2Sim/230511_swing_0deg_opps18/pose-2d/swing1',
                'model_pose' : 'COCO', # BODY_25B, COCO
                'ext': 'avi'}
    
    run_openpose(cfg_path=cfg_path, cfg_dict=None)