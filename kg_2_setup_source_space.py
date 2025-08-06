# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:07:33 2015

@author: takeiyuichi
"""

#このスクリプトには以下のpythonパッケージが必要です。
#pydicom https://code.google.com/p/pydicom/downloads/list
# nibabel
# networkx
# nipype

#この処理を行う前に、kg_prepare(_日付).pyを行い、
#解析用ディレクトリの構成を行って下さい。

#macをお使いの場合は、ターミナル(ipythonもしくはpython)から使用して下さい。
#canopyでは動きません！

#またLinux環境では試していないので、

#このスクリプトはT1からfreesufer のrecon allを行い、source spaceのセットアップまで行います。.
#もし不要な処理がありましたら、以下のprocess1の定義の中で、不要な処理をコメントアウトして下さい。

#自動読み込み#####################################################################################################################################
#First edit .bash_profile or .profile in user directory (e.g. /Users/takeiyuichi/)

PARAMETER_DIR='/Volumes/ssdraid/Dropbox (MEG)/seirisyuki_rest/parameter'
set_environment='cul'
n_jobs=24 #並列処理の数

#PARAMETER_DIR='/Users/takeiyuuichi/Dropbox (MEG)/seirisyuki_rest/parameter'
#large_results_dir='/Users/takeiyuuichi/Dropbox (MEG)/seirisyuki_rest/results'
#n_jobs=4
#set_environment='main'
SET_MEG_SPACING='oct5'

import sys
import os
import time
sys.path.append(PARAMETER_DIR)
os.chdir(PARAMETER_DIR)
if set_environment=='main':
    import python_setting_main as cfg
else:
    import python_setting_cul as cfg

sys.path.append(cfg.SET_SCRIPT_PATH)
os.chdir(cfg.SET_SCRIPT_PATH)
import kg_sub_MNE_151002 as kgMNE
#######################################設定領域##############################################################################
FREESURFER_HOME= '/Applications/freesurfer'
MATLAB_ROOT= '/Applications/MATLAB_R2015b.app'
MNE_ROOT='/Applications/MNE-2.7.4-3378-MacOSX-x86_64'
n_jobs=24
n_jobs=4
#mne_watershed_bem##########################################
SET_VOLUME='T1'
SET_OVERWRITE=True
SET_PLOT_BEM=True
#setup_volume_source_space###################################
SET_Volume_SPACING='oct5'
#<number>	Sources per hemisphere	Source spacing / mm	Surface area per source / mm2
#-5	1026	9.9	97
#4	2562	6.2	39
#-6	4098	4.9	24
#5	10242	3.1	9.8
#setup_source_space##########################################
SET_SURFACE='white'
#Specifying --ico 4 yields 5120 triangles per surface while --ico 3 results in 1280 triangles.
#The recommended choice is --ico 4 .

def mne_process(all_subject,sttime):
    #不要な処理をコメントアウトして下さい。----------------------------------------------------
    kgMNE.mne_setup_mri(SET_OVERWRITE,all_subject,sttime,n_jobs,env)
    #kgMNE.mne_watershed_bem(SET_OVERWRITE,all_subject,sttime,n_jobs,env)
    kgMNE.multi_mne_watershed_bem(all_subject,sttime,SET_OVERWRITE,n_jobs,cfg,env)
    
    kgMNE.multi_setup_source_space(SET_Volume_SPACING, SET_SURFACE, SET_OVERWRITE,all_subject,sttime,n_jobs,cfg.SET_SUBJECTS_DIR,env)
    kgMNE.mne_setup_forward_model(SET_MEG_SPACING,SET_OVERWRITE,all_subject,sttime,n_jobs,cfg.SET_SUBJECTS_DIR,env)
    #############################################メインの処理############################################################################                     
if __name__ == '__main__':
    env = os.environ.copy()
    env['FREESURFER_HOME'] = FREESURFER_HOME
    env['MATLAB_ROOT'] = MATLAB_ROOT
    env['MNE_ROOT'] = MNE_ROOT
    env['SUBJECTS_DIR'] = cfg.SET_SUBJECTS_DIR   
       
    sttime = time.time()
    all_subject=[]
    for line in open(cfg.SET_PARAMETER, 'rU'):
        itemList = line[:-1].split('@')
        all_subject.append(itemList[0])
    mne_process(all_subject,sttime)
    #--------------------------------------------------------------------------------------------
    entime = time.time()
    print('Total processing time is ' + str((entime-sttime)/60) + '.')
