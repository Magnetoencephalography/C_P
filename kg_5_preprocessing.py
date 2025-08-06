#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 05:37:22 2020

@author: takeiyuuichi
"""
import mne
from mne.preprocessing import create_ecg_epochs
import os        
from mne.io import Raw    
import mne                    
import matplotlib.pyplot as plt  
from mne.preprocessing import create_ecg_epochs
#PARAMETER_DIR='/Users/takeiyuuichi/Dropbox (MEG)/seirisyuki_rest/parameter'
n_jobs=12 #並列処理の数
set_environment='main'
n_jobs=12 #並列処理の数
base_rawname='rest1'

#PARAMETER_DIR='D:/Dropbox (MEG)/seirisyuki_rest/parameter'
set_environment='pc_main'
n_jobs=40
t_n_jobs='cuda'
t_n_jobs=40

n_jobs=16 #並列処理の数
#PARAMETER_DIR='/Users/takeiyuuichi/Dropbox (MEG)/CP/parameter'
PARAMETER_DIR='/home/takeiyuuichi/Dropbox (MEG)/CP/parameter'

set_environment='main'
base_rawname='SAF_seq1_square'
#
#set_environment='SAF_seq2_circle'
#base_rawname='SAF_seq2_circle'



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
elif set_environment=='SAF_seq2_circle':
    import python_setting_SAF_seq2_circle as cfg
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
    
line='NB_subject_188@180117@'
itemList = line[:-1].split('@')
SUBJECT=itemList[0]
DATE=itemList[1]

print("mne browse_raw --raw='/Users/takeiyuuichi/Dropbox (MEG)/seirisyuki_rest/MEG/"+SUBJECT+'/'+DATE+"/preprocess/ICA/'+base_rawname+'_ica_raw.fif'" + ' --n_channels=99')


#############import module and settings#####################
s_i=0
new_filename=''
if not os.path.exists(cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/preprocess'):
    os.makedirs(cfg.SET_MEG_DIR  + '/' + SUBJECT + '/' + DATE + '/preprocess')
if not os.path.exists(cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/preprocess/ICA'):
    os.makedirs(cfg.SET_MEG_DIR  + '/' + SUBJECT + '/' + DATE + '/preprocess/ICA')    
path = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE
raw_fname = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/' + base_rawname  + '_notch_otp_raw_tsss.fif' #raw data
raw = mne.io.Raw(raw_fname, preload=True)
ica=mne.preprocessing.read_ica(cfg.SET_MEG_DIR  + '/' + SUBJECT + '/' + DATE + '/preprocess/ICA/'+base_rawname+'_original-ica.fif')


f = open(cfg.SET_MEG_DIR  + '/' + SUBJECT + '/' + DATE  + '/preprocess/ICA/'+base_rawname+'_ica_setting.txt')
ICA_index = f.read() 
f.close()
if ICA_index.split('@')[0]:
    ICA_index_ECG=list(map(int, ICA_index.split('@')[0].split(',')))
else:
    ICA_index_ECG=[]
if ICA_index.split('@')[1]:
    ICA_index_EOG=list(map(int, ICA_index.split('@')[1].split(',')))
else:
    ICA_index_EOG=[]
if ICA_index.split('@')[2]:
    ICA_index_JUMP=list(map(int, ICA_index.split('@')[2].split(',')))
else:
    ICA_index_JUMP=[]

if not ICA_index_ECG==[]:
    ica.exclude += ICA_index_ECG   
# EOG
if not ICA_index_EOG==[]:
    ica.exclude += ICA_index_EOG
# JUMP
if not ICA_index_JUMP==[]:
    ica.exclude += ICA_index_JUMP 
new_filename=cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/' + base_rawname  +'_notch_otp_ica_raw_tsss.fif'            
raw2 = Raw(raw_fname, preload=True)
ica.apply(raw2)
raw2.save(new_filename, overwrite=True) 
picks = mne.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=False,
                   exclude='bads')
fig=raw2.plot_psd( fmin=0, fmax=100, show=True,picks=picks,n_jobs=n_jobs)
fig.savefig(cfg.SET_MEG_DIR  + '/' + SUBJECT + '/' + DATE+ '/preprocess/psd_' +base_rawname + '_notch_otp_ica_raw_tsss', dpi=600)
plt.close()
#
#data=ica.get_sources(raw,start=0,stop=1000)
#psd=mne.time_frequency.psd_array_multitaper(data.get_data(),sfreq=raw.info['sfreq'], fmin=0, fmax=100)
#for i in range(data.get_data().shape[0]):
#    plt.plot(psd[1],psd[0][i,:],label=str(i))
#    plt.legend(loc="lower left")
#    plt.show()
#    plt.close()
#    
#i=28
#ica.plot_properties(raw, picks=[41,15,29])
#    
    
    
    