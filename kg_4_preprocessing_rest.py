# -*- coding: utf-8 -*-
#MEGの前処理をするためのスクリプト
#ECG,EOGがを用いたSSP,ICAによる処理、ECG,EOGなしでのICAによる処理、notch filterが行うことが出来る

#処理の手順は一番下を参照。

#自動読み込み##############################################
#PARAMETER_DIR='/Volumes/Promise_Pegasus/Dropbox/MEG_current/kougakubu/parameter'
#PARAMETER_DIR='/Volumes/ssdraid/Dropbox (MEG)/seirisyuki_rest/parameter'
#設定################################################################################
#PCを選択。mainとculの二つの設定値を持てる


n_jobs=16 #並列処理の数
t_n_jobs=16
PARAMETER_DIR='/Users/takeiyuuichi/Dropbox (MEG)/CP/parameter'
#PARAMETER_DIR='/home/takeiyuuichi/Dropbox (MEG)/CP/parameter'

set_environment='main'
base_rawname='SAF_seq1_square'
#



#set_environment='SAF_seq2_square2'
#base_rawname='SAF_seq2_square2'
#
#set_environment='SAF_seq3_circle'
#base_rawname='SAF_seq3_circle'
##
#set_environment='SAF_seq3_circle2'
#base_rawname='SAF_seq3_circle2'
###
#set_environment='SAF_seq4_circle2'
#base_rawname='SAF_seq4_circle2'



#PARAMETER_DIR='D:/Dropbox (MEG)/seirisyuki_rest/parameter'
#set_environment='pc_main'
#n_jobs=40
#t_n_jobs='cuda'
#t_n_jobs=40

set_environment='SAF_seq2_circle'
base_rawname='SAF_seq2_circle'
PARAMETER_DIR='/Volumes/ssdraid/Dropbox (MEG)/CP/parameter/'
set_environment='cul'
n_jobs=24 #並列処理の数
t_n_jobs=12 #並列処理の数

#PARAMETER_DIR='/Volumes/ssdraid/Dropbox (MEG)/seirisyuki_rest/parameter/'
#set_environment='sub'
#n_jobs=12
#t_n_jobs=12


#base_rawname='room'
set_ref_ecg_ch=[] #ECGのref channel
set_ref_eog_ch=[]#EOGのref channel
set_notch_filter=[50,100,150] #notch filterをかける周波数
#set_notch_filter=[]
#############SSP apply index##########
import sys
import os  
sys.path.append(PARAMETER_DIR)
os.chdir(PARAMETER_DIR)
if set_environment=='main':
    import python_setting_main as cfg
elif set_environment=='pc_main':
    import python_setting_pc_main as cfg
elif set_environment=='cul':
    import python_setting_cul as cfg
elif set_environment=='SAF_seq2_square2':
    import python_setting_SAF_seq2_square2 as cfg
elif set_environment=='SAF_seq3_circle':
    import python_setting_SAF_seq3_circle as cfg
elif set_environment=='SAF_seq3_circle2':
    import python_setting_SAF_seq3_circle2 as cfg
elif set_environment=='SAF_seq4_circle2':
    import python_setting_SAF_seq4_circle2 as cfg
else:
    import python_setting_cul as cfg

sys.path.append(cfg.SET_SCRIPT_PATH)
os.chdir(cfg.SET_SCRIPT_PATH)
import kg_sub_preprocessing_191227 as preprocessing
#######################################################################################

if __name__ == '__main__':
#############import module and settings#####################
#
#    
    
    if set_notch_filter ==[]:
        print( 'notch filter not applyed')
    else:
        if 'notch' in cfg.SET_FILENAME:
            print( 'already applyed notch filter')
        else:
            preprocessing.notch_filter(base_rawname,set_notch_filter,n_jobs,cfg,set_environment)
##    preprocessing.preprocessing_SSP1(base_rawname,set_ref_ecg_ch,set_ref_eog_ch,n_jobs,cfg,set_environment)
##    preprocessing.preprocessing_SSP2(base_rawname,set_ref_ecg_ch,set_ref_eog_ch,cfg,set_environment)
    preprocessing.oversampled_temporal_projection(base_rawname,cfg,set_environment)
    preprocessing.maxfilter(base_rawname,n_jobs,cfg,set_environment)
#    preprocessing.preprocessing_SSP2(base_rawname,set_ref_ecg_ch,set_ref_eog_ch,cfg,set_environment)
    preprocessing.preprocessing_ICA1(base_rawname,set_ref_eog_ch,n_jobs,t_n_jobs,cfg,set_environment)

