#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
    ##################################################
    ## Plot TRC files                               ##
    ##################################################
    
    Display each point of a TRC file in a different matplotlib tab.
    
    Usage: 
        from Pose2Sim.Utilities import trc_plot; trc_plot.trc_plot_func(r'<input_trc_file>')
        OR python -m trc_plot -i "<input_trc_file>"
'''


## INIT
import pandas as pd
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('qt5agg')
mpl.rc('figure', max_open_warning=0)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout
from scipy import signal
from scipy.ndimage import gaussian_filter1d
from statsmodels.nonparametric.smoothers_lowess import lowess
import argparse
import numpy as np


## AUTHORSHIP INFORMATION
__author__ = "David Pagnon"
__copyright__ = "Copyright 2021, Pose2Sim"
__credits__ = ["David Pagnon"]
__license__ = "BSD 3-Clause License"
__version__ = "0.1"
__maintainer__ = "David Pagnon"
__email__ = "contact@david-pagnon.com"
__status__ = "Development"


## CLASSES
class plotWindow():
    '''
    Display several figures in tabs
    Taken from https://github.com/superjax/plotWindow/blob/master/plotWindow.py

    USAGE:
    pw = plotWindow()
    f = plt.figure()
    plt.plot(x1, y1)
    pw.addPlot("1", f)
    f = plt.figure()
    plt.plot(x2, y2)
    pw.addPlot("2", f)
    '''

    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.MainWindow.__init__()
        self.MainWindow.setWindowTitle("Multitabs figure")
        self.canvases = []
        self.figure_handles = []
        self.toolbar_handles = []
        self.tab_handles = []
        self.current_window = -1
        self.tabs = QTabWidget()
        self.MainWindow.setCentralWidget(self.tabs)
        self.MainWindow.resize(1280, 720)
        self.MainWindow.show()

    def addPlot(self, title, figure):
        new_tab = QWidget()
        layout = QVBoxLayout()
        new_tab.setLayout(layout)

        figure.subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.91, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_toolbar = NavigationToolbar(new_canvas, new_tab)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        self.tabs.addTab(new_tab, title)

        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        self.tab_handles.append(new_tab)

    def show(self):
        self.app.exec_() 


## FUNCTIONS
def display_figures_fun(Q, time_col, keypoints_names):
    '''
    Displays filtered and unfiltered data for comparison

    INPUTS:
    - Q: pandas dataframe of 3D coordinates
    - time_col: pandas column
    - keypoints_names: list of strings

    OUTPUT:
    - matplotlib window with tabbed figures for each keypoint
    '''
    
    pw = plotWindow()
    for id, keypoint in enumerate(keypoints_names):
        f = plt.figure()
        
        axX = plt.subplot(311)
        plt.plot(time_col, Q.iloc[:,id*3])
        plt.setp(axX.get_xticklabels(), visible=False)
        axX.set_ylabel(keypoint+' X')

        axY = plt.subplot(312)
        plt.plot(time_col, Q.iloc[:,id*3+1])
        plt.setp(axY.get_xticklabels(), visible=False)
        axY.set_ylabel(keypoint+' Y')

        axZ = plt.subplot(313)
        plt.plot(time_col, Q.iloc[:,id*3+2])
        axZ.set_ylabel(keypoint+' Z')
        axZ.set_xlabel('Time')

        pw.addPlot(keypoint, f)
    
    pw.show()

def yup2zup(Q):
    '''
    Turns Y-up system coordinates into Z-up coordinates

    INPUT:
    - Q: pandas dataframe
    N 3D points as columns, ie 3*N columns in Y-up system coordinates
    and frame number as rows

    OUTPUT:
    - Q: pandas dataframe with N 3D points in Y-up system coordinates
    '''
    
    # Y->X, Z->Y, X->Z (=Y축이 X축으로, Z축이 Y축으로, X축이 Z축으로)
    cols = list(Q.columns)
    cols = np.array([[cols[i*3+2],cols[i*3],cols[i*3+1]] for i in range(int(len(cols)/3))]).flatten()
    Q = Q[cols]

    return Q

def draw_limbs_3d(Q, keypoints_names, joint_parents):
    joints_nb = len(keypoints_names)
    
    # yup2zup (convert to Z-up system = opensim coord to matplotlib coord)
    # Q = yup2zup(Q)
    
    joints_3d = Q.to_numpy()
    joints_3d = joints_3d.reshape(-1, joints_nb, 3) # (frames, joints, xyz)
    
    # transform to hip center of first frame
    hip_center = (joints_3d[0,0,:] + joints_3d[0,6,:]) / 2 # center of R/L hip
    joints_3d = joints_3d - hip_center
        
    # init plot
    plt.ion()
    fig = plt.figure()
    ax_3d = plt.axes(projection='3d')
    # ax_3d.view_init(elev=-90, azim=-90)
    # ax_3d.view_init(-90, -90)
    ax_3d.set_xlim(-1, 1)
    ax_3d.set_ylim(-1, 1)
    ax_3d.set_zlim(-1, 1)
    plt.show()
    
    # plot 3d skeleton
    for frame_id, j3d in enumerate(joints_3d):
        ax_3d.clear()
        ax_3d.view_init(0, 0)
        ax_3d.set_xlim(-1, 1)
        ax_3d.set_ylim(-1, 1)
        ax_3d.set_zlim(-1, 1)
        ax_3d.set_xlabel('x')
        ax_3d.set_ylabel('y')
        ax_3d.set_zlabel('z')
            
        for j_id in range(j3d.shape[0]):        
            x_pair = [j3d[j_id, 0], j3d[joint_parents[j_id], 0]]
            y_pair = [j3d[j_id, 1], j3d[joint_parents[j_id], 1]]
            z_pair = [j3d[j_id, 2], j3d[joint_parents[j_id], 2]]
            ax_3d.plot(x_pair, y_pair, zs=z_pair, linewidth=3)
            # ax_3d.scatter(j3d[j_id, :, 0], j3d[j_id, :, 1], j3d[j_id, :, 2], s=10, c='b', marker='o')
        
        plt.pause(0.0001)
        plt.show(block=True)
        

def trc_plot_func(*args, joint_parents=None):
    '''
    Plot trc files.
    
    Usage: 
        import trc_plot; trc_plot.trc_plot_func(r'<input_trc_file>')
        OR trc_plot -i "<input_trc_file>"
    '''
    
    try:
        trc_path = args[0].get('input_file') # invoked with argparse
    except:
        trc_path = args[0] # invoked as a function

    # Read trc coordinates values
    trc_df = pd.read_csv(trc_path, sep="\t", skiprows=4)
    time_col =trc_df.iloc[:,1]
    Q_coord = trc_df.drop(trc_df.columns[[0, 1]], axis=1)

    # Display figures
    keypoints_names = pd.read_csv(trc_path, sep="\t", skiprows=3, nrows=0).columns[2::3].tolist()
    draw_limbs_3d(Q_coord, keypoints_names, joint_parents)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required = True, help='trc input file')
    args = vars(parser.parse_args())
    joint_parents = [12, 0, 1, 2, 2, 2,    
                    12, 6, 7, 8, 8, 8, 
                    0, 14, 12, 
                    12, 15, 16,
                    12, 18, 19] # modified openpose body25b (except for r/l eyes and ears)
    trc_plot_func(args, joint_parents=joint_parents)
    
