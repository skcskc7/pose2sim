:: Avoid printing all the comments in the Windows cmd
@echo off

echo ------------------------- BODY, FOOT, FACE, AND HAND MODELS -------------------------
echo ----- Downloading body pose (COCO and MPI), face and hand models -----
SET WGET_EXE=..\3rdparty\windows\wget\wget.exe
SET OPENPOSE_URL=http://posefs1.perception.cs.cmu.edu/OpenPose/models/
SET POSE_FOLDER=pose/

echo:
echo ------------------------- POSE (BODY+FOOT) MODELS -------------------------
echo Body (BODY_25b)
set BODY_25_FOLDER=%POSE_FOLDER%1_25BSuperModel11FullVGG/body_25b/
set BODY_25_MODEL=%BODY_25_FOLDER%pose_iter_XXXXXX.caffemodel
%WGET_EXE% -c %OPENPOSE_URL%%BODY_25_MODEL% -P %BODY_25_FOLDER%
echo ----------------------- POSE DOWNLOADED -----------------------
