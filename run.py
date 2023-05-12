from Pose2Sim import Pose2Sim, calibration, openpose

cfg_path = './Config.toml'
calibration.calibrate_cams_all(cfg_path)
openpose.run_openpose(cfg_path)
Pose2Sim.track2D(cfg_path)
Pose2Sim.triangulate3D(cfg_path)
Pose2Sim.filter3D(cfg_path)