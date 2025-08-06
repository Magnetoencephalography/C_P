# -*- coding: utf-8 -*-

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

#自動読み込み##############################################
PARAMETER_DIR='/Volumes/Promise_Pegasus/Dropbox/seirisyuki_rest/parameter'
#PARAMETER_DIR='/Volumes/Samsung_T3/seirisyuki_rest/parameter'
#設定################################################################################
n_jobs=40 #並列処理の数
t_n_jobs='cuda'
#PARAMETER_DIR='/Users/takeiyuuichi/Dropbox (MEG)/CP/parameter'
PARAMETER_DIR='/Users/takeiyuuichi/Dropbox (MEG)/CP/parameter'
set_environment='main'
base_rawname='SAF_merge'
n_jobs=16 #並列処理の数
t_n_jobs=16 #並列処理の数
#
##
#PARAMETER_DIR='D:/Dropbox (MEG)/seirisyuki_rest/parameter/'
#set_environment='pc_main'
#n_jobs=40
#t_n_jobs='cuda'
##

import sys
import os
from glob import glob
from os.path import join, relpath
import time
import mne
import os.path as op
from mne import make_forward_solution,read_cov
from mne.minimum_norm import make_inverse_operator,write_inverse_operator
from mayavi import mlab
sys.path.append(PARAMETER_DIR)
os.chdir(PARAMETER_DIR)
if set_environment=='main':
    import python_setting_main as cfg
elif set_environment=='cul':
    import python_setting_cul as cfg
elif set_environment=='pc_main':
    import python_setting_pc_main as cfg
else:
    import python_setting_sub as cfg

sys.path.append(cfg.SET_SCRIPT_PATH)
os.chdir(cfg.SET_SCRIPT_PATH)
import kg_sub_MNE_151002 as kgMNE
#######################################設定領域##############################################################################
FREESURFER_HOME= '/Applications/freesurfer'
MATLAB_ROOT= '/Applications/MATLAB_R2015b.app'
MNE_ROOT='/Applications/MNE-2.7.4-3378-MacOSX-x86_64'
#n_jobs=24
#mne_watershed_bem##########################################
SET_VOLUME='T1'
SET_OVERWRITE=False
SET_PLOT_BEM=True
#setup_volume_source_space###################################
SET_Volume_SPACING='oct6'
#SET_Volume_SPACING='ico5'
#<number>	Sources per hemisphere	Source spacing / mm	Surface area per source / mm2
#-5	1026	9.9	97
#4	2562	6.2	39
#-6	4098	4.9	24
#5	10242	3.1	9.8
#setup_source_space##########################################
SET_MEG_SPACING='oct6'
#SET_MEG_SPACING='ico5'
SET_SURFACE='white'
#Specifying --ico 4 yields 5120 triangles per surface while --ico 3 results in 1280 triangles.
#The recommended choice is --ico 4 .
#make_noise_cov##############################################
NOISE_COV_FNAME='room_notch_otp_raw_tsss.fif'
CREATE_FROM_RAW=True
REJECT=dict(mag=4e-12, grad=4000e-13)
#make_forward_solution#######################################
SET_FWD_MINDIST=5
#convert_forward_solution,make_inverse_operator##############
#select any one of setting
SET_LOOSE,SET_DEPTH,SET_INV_FIXED,SET_FORCE_FIXED,SET_SURF_ORI=0.2,0.8,False,False,True # Loose constraint ,Depth weighted
#SET_LOOSE,SET_DEPTH,SET_INV_FIXED,SET_FORCE_FIXED,SET_SURF_ORI=0.2,None,False,False,True # Loose constraint
#SET_LOOSE,SET_DEPTH,SET_INV_FIXED,SET_FORCE_FIXED,SET_SURF_ORI=None,0.8,False,False,True #Free orientation,Depth weighted
#SET_LOOSE,SET_DEPTH,SET_INV_FIXED,SET_FORCE_FIXED,SET_SURF_ORI=None,None,False,False,True #Free orientation
#SET_LOOSE,SET_DEPTH,SET_INV_FIXED,SET_FORCE_FIXED,SET_SURF_ORI=None,0.8,True,False,True #Fixed constraint,Depth weighted
#SET_LOOSE,SET_DEPTH,SET_INV_FIXED,SET_FORCE_FIXED,SET_SURF_ORI=None,None,True,True,True #Fixed constraint 

#############################################各段階の処理############################################################################
def argwrapper(args):
    return args[0](*args[1:])

def work(cmd,env):
    import subprocess
    return subprocess.call(cmd,  env=env)

def file_serch(path,base_name,search_word):
    
    raw_files = [relpath(x, path) for x in glob(join(path, '*'))]
    temp_raw_files=[]
    for temp_name in raw_files:
        if base_name in temp_name:
            temp_raw_files.append(temp_name)
    files=[]
    for temp_name in temp_raw_files:
        if search_word in temp_name:
            files.append(temp_name)
    return files


def mne_make_scalp_surfaces(all_subject,sttime,n_jobs,env):
    import multiprocessing
    import time
    p = multiprocessing.Pool(n_jobs)
    func_args = []
    en=0
    for line in all_subject:
        func_args.append((work,['mne','make_scalp_surfaces','-s', all_subject[en][0]],env))
        en+=1
    p.map(argwrapper, func_args)
    func_args=[]
    print('Processing time is' + str((time.time()-sttime)/60) + '.')



def mne_process(all_subject,env,sttime):
    #不要な処理をコメントアウトして下さい。----------------------------------------------------
    kgMNE.multi_setup_source_space(SET_Volume_SPACING, SET_SURFACE, SET_OVERWRITE,all_subject,sttime,n_jobs,cfg,set_environment)
#    kgMNE.multi_make_noise_cov(cfg.SET_FILENAME,CREATE_FROM_RAW,all_subject,sttime,n_jobs,PARAMETER_DIR,cfg,set_environment)
    #    kgMNE.multi_make_event_from_raw(all_subject,sttime,n_jobs,PARAMETER_DIR,cfg,set_environment)
#    kgMNE.mne_watershed_bem(SET_OVERWRITE,all_subject,sttime,n_jobs,cfg)
#    kgMNE.mne_setup_forward_model(SET_MEG_SPACING,SET_OVERWRITE,all_subject,sttime,n_jobs,cfg.SET_SUBJECTS_DIR,set_environment)
#    mne_make_scalp_surfaces(all_subject,sttime,n_jobs,env)
    
    for line in all_subject:
        SUBJECT=line[0]
        DATE=line[1]  
        raw_fname = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/' + cfg.SET_FILENAME #raw data
        trans_files=file_serch(cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE,'','trans')
        if len(trans_files)>0:
            trans_file = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/' + trans_files[0]
        else:
            print(SUBJECT + ' does not have trans file!')
                
        fname_src = op.join(cfg.SET_SUBJECTS_DIR, SUBJECT, 'bem', SUBJECT+ '-' + SET_MEG_SPACING[0:3] + '-' + SET_Volume_SPACING[len(SET_Volume_SPACING)-1] + '-src.fif')        
        fwd_filename=raw_fname[0:len(raw_fname)-4] + '-fwd.fif'
        inv_filename=raw_fname[0:len(raw_fname)-4] + '-inv.fif'
        
                
        if  SET_MEG_SPACING=='ico4':
            fname_bem = op.join(cfg.SET_SUBJECTS_DIR, SUBJECT, 'bem',SUBJECT+'-5120-bem-sol.fif')   
        elif   SET_MEG_SPACING=='ico3':
            fname_bem = op.join(cfg.SET_SUBJECTS_DIR, SUBJECT, 'bem',SUBJECT+'-1280-bem-sol.fif')
        elif   SET_MEG_SPACING=='oct5':
            fname_bem = op.join(cfg.SET_SUBJECTS_DIR, SUBJECT, 'bem',SUBJECT+'-20480-bem-sol.fif')
        elif   SET_MEG_SPACING=='oct6':
        
            fname_bem = op.join(cfg.SET_SUBJECTS_DIR, SUBJECT, 'bem',SUBJECT+'-20480-bem-sol.fif')
        elif   SET_MEG_SPACING=='ico5':
        
            fname_bem = op.join(cfg.SET_SUBJECTS_DIR, SUBJECT, 'bem',SUBJECT+'-20480-bem-sol.fif')#            conductivity = (0.3,)  # for single layer
#            # conductivity = (0.3, 0.006, 0.3)  # for three layers
#            model = mne.make_bem_model(subject=SUBJECT, ico=5,conductivity=conductivity, subjects_dir=cfg.SET_SUBJECTS_DIR)
#            bem = mne.make_bem_solution(model)
#            mne.write_bem_solution(fname_bem, bem)
        raw = mne.io.Raw(raw_fname,preload=True)
#        raw.filter(0.5,None,l_trans_bandwidth=0.25,n_jobs=n_jobs)
        noise_cov=read_cov(raw_fname[0:len(raw_fname)-4] + '-cov.fif')
        #不要な処理をコメントアウトして下さい。----------------------------------------------------
#        if not os.path.isfile(fname_src):
        src = mne.setup_source_space(SUBJECT, spacing=SET_Volume_SPACING, surface='white', subjects_dir=cfg.SET_SUBJECTS_DIR,  n_jobs=n_jobs)
        mne.write_source_spaces(fname_src, src,overwrite=True)         
        fwd=make_forward_solution(raw.info, trans_file, fname_src, fname_bem, meg=True,
                                  eeg=False, mindist=SET_FWD_MINDIST, n_jobs=1)

        kgMNE.edit_python_setting(cfg.SET_FILENAME[0:len(cfg.SET_FILENAME)-4] + '-fwd.fif','SET_FWDNAME',PARAMETER_DIR,set_environment)#python_settingのSET_FWDNAMEの書き換え
        forward = mne.convert_forward_solution(fwd, surf_ori=SET_SURF_ORI,force_fixed=SET_FORCE_FIXED)
        inv = make_inverse_operator(raw.info, forward, noise_cov,loose=SET_LOOSE, depth=SET_DEPTH,fixed=SET_INV_FIXED)        
        write_inverse_operator(inv_filename,inv)
        kgMNE.edit_python_setting(cfg.SET_FILENAME[0:len(cfg.SET_FILENAME)-4] + '-inv.fif','SET_INVNAME',PARAMETER_DIR,set_environment)#python_settingのSET_INVNAMEの書き換え
        #--------------------------------------------------------------------------------------------
#        trans = mne.read_trans(cfg.SET_MAIN_DIR + '/MEG/' + SUBJECT + '/'+DATE+'/' + SUBJECT+'-trans.fif')
#        src = mne.read_source_spaces(op.join(cfg.SET_SUBJECTS_DIR, SUBJECT, 'bem',
#                                             SUBJECT+'-oct-6-src.fif'))    
#        
#        fig = mne.viz.plot_alignment(raw.info, trans=trans, subject=SUBJECT,
#                                     subjects_dir=cfg.SET_SUBJECTS_DIR, surfaces='head-dense',
#                                     show_axes=True, dig=True, eeg=[], meg='sensors',
#                                     coord_frame='meg')
#        
##        fig = mne.viz.plot_alignment(raw.info,trans=trans,surfaces=('inner_skull', 'outer_skull', 'outer_skin'),
##                       subjects_dir=cfg.SET_SUBJECTS_DIR, subject=SUBJECT,
##                                 show_axes=True, dig=True, eeg=[], meg='sensors',
##                                     coord_frame='meg')
#        
#        
#        mne.viz.set_3d_view(fig, 45, 90, distance=0.6, focalpoint=(0., 0., 0.))
#        fig.scene.save(cfg.SET_RESULT_DIR + '/head_alignmeent/' + SUBJECT + '_plot_alignment.png')
#        mlab.close()


        print('Processing time is' + str((time.time()-sttime)/60) + '.')
        print('processing finished ' + SUBJECT)
    kgMNE.plot_BEM(all_subject,cfg,set_environment)
    
 #############################################メインの処理############################################################################
def main():
    env = os.environ.copy()
    env['FREESURFER_HOME'] = FREESURFER_HOME
    env['MATLAB_ROOT'] = MATLAB_ROOT
    env['MNE_ROOT'] = MNE_ROOT
    env['SUBJECTS_DIR'] = cfg.SET_SUBJECTS_DIR   
       
    sttime = time.time()
    all_subject=[]
    for line in open(cfg.SET_PARAMETER, 'rU'):
        itemList = line[:-1].split('@')
        all_subject.append(itemList)
    mne_process(all_subject,env,sttime)
    #--------------------------------------------------------------------------------------------
    entime = time.time()
    print('Total processing time is ' + str((entime-sttime)/60) + '.')

if __name__ == '__main__':
    main()

