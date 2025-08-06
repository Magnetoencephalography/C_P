#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 05:56:04 2020

@author: takeiyuuichi
"""


#setting##############################################
n_jobs=16 #並列処理の数
t_n_jobs=16
PARAMETER_DIR='/Volumes/Siena/CP/parameter'
#n_jobs=40 #並列処理の数
#t_n_jobs='cuda'
#PARAMETER_DIR='/home/takeiyuuichi/Dropbox (MEG)/CP/parameter'

set_environment='main'

SET_EVENTID=[2,3]
event_id = dict(control=2,arousal=3)
#square=non-face,circle=face
SET_EVENTNAME=['square','circle']
SET_MEG=True
REJECT = dict(grad=4000e-13,mag=4e-12)
#################解析時間の指定################
tmin=-0.1
tmax=0.3
#################ここにROIの名前を入れる################
pick_list=['L_Occ','R_Occ','L_fusiform','R_fusiform','L_midTemp','R_midTemp','L_Temptip','R_Temptip']

#################ROIのチャンネル選択################
R_Occ_list=[
'MEG 2111', 'MEG 2112', 'MEG 2113',
'MEG 2331', 'MEG 2332', 'MEG 2333',
'MEG 2341', 'MEG 2342', 'MEG 2343',
'MEG 2031', 'MEG 2032', 'MEG 2033']

L_Occ_list=[
'MEG 2121', 'MEG 2122', 'MEG 2123',
'MEG 1931', 'MEG 1932', 'MEG 1933',
'MEG 1921', 'MEG 1922', 'MEG 1923',
'MEG 2041', 'MEG 2042', 'MEG 2043']

#['MEG 1312',
#                  'MEG 1333',
#                 'MEG 1342',
#                  'MEG 2322',
#                  'MEG 2412',
#                  'MEG 2423',
#                 'MEG 2432','MEG 2433',
#  'MEG 2513',
#  'MEG 2523' ]

#R_fusiform_list=[
#'MEG 2431', 'MEG 2432', 'MEG 2433',
#'MEG 2521', 'MEG 2522', 'MEG 2523',
#'MEG 2321', 'MEG 2322', 'MEG 2323',
#'MEG 2511', 'MEG 2512', 'MEG 2513']
R_fusiform_list=[
'MEG 2411', 'MEG 2412', 'MEG 2413',
'MEG 2431', 'MEG 2432', 'MEG 2433',
'MEG 2521', 'MEG 2522', 'MEG 2523',
'MEG 2511', 'MEG 2512', 'MEG 2513']
# 'MEG 2423',
# 'MEG 2412',
# 'MEG 2322',
# 'MEG 1342',
# 'MEG 1333',
# 'MEG 1312'
# 
 
#L_fusiform_list=[
#'MEG 1721', 'MEG 1722', 'MEG 1723',
#'MEG 1641', 'MEG 1642', 'MEG 1643',
#'MEG 1941', 'MEG 1942', 'MEG 1943',
#'MEG 1731', 'MEG 1732', 'MEG 1733']
L_fusiform_list=[
'MEG 1731', 'MEG 1732', 'MEG 1733',
'MEG 1721', 'MEG 1722', 'MEG 1723',
'MEG 1641', 'MEG 1642', 'MEG 1643',
'MEG 1621', 'MEG 1622', 'MEG 1623']

R_midTemp_list=[
'MEG 1331', 'MEG 1332', 'MEG 1333',
'MEG 1341', 'MEG 1342', 'MEG 1343',
'MEG 2641', 'MEG 2642', 'MEG 2643',
'MEG 2421', 'MEG 2422', 'MEG 2423']

L_midTemp_list=[
'MEG 0233', 'MEG 0233', 'MEG 0232',
'MEG 0241', 'MEG 0242', 'MEG 0243',
'MEG 1611', 'MEG 1612', 'MEG 1613',
'MEG 1521', 'MEG 1522', 'MEG 1523']

R_Temptip_list=[
'MEG 1421', 'MEG 1422', 'MEG 1423',
'MEG 1443', 'MEG 1443', 'MEG 1442',
'MEG 1431', 'MEG 1432', 'MEG 1433',
'MEG 1321', 'MEG 1322', 'MEG 1323']

L_Temptip_list=[
'MEG 0111', 'MEG 0112', 'MEG 0113',
'MEG 0211', 'MEG 0212', 'MEG 0213',
'MEG 0131', 'MEG 0132', 'MEG 0133',
'MEG 0141', 'MEG 0142', 'MEG 0143']









##############################################
from PIL import Image

import numpy as np
import sys
import os  
import mne
from scipy import stats
import matplotlib.pyplot as plt
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

sys.path.append(cfg.SET_SCRIPT_PATH)
os.chdir(cfg.SET_SCRIPT_PATH)

result_dir=cfg.SET_LARGERESULT_DIR+'/' + 'evoked'

def custom_func(x):
    return x.max(axis=1)      
def main():
    all_subject=[]
    for line in open(cfg.SET_PARAMETER, 'rU'):
        itemList = line[:-1].split('@')
        all_subject.append(itemList)
        
#################ROIのセンサーポジションのプロット################        
    all_ROIlist=[L_Occ_list,R_Occ_list,L_fusiform_list,R_fusiform_list,L_midTemp_list,R_midTemp_list,L_Temptip_list,R_Temptip_list]
    for i in range(len(all_ROIlist)):
        raw_fname = cfg.SET_MAIN_DIR  + '/MEG' + '/' + all_subject[0][0] + '/' + all_subject[0][1] + '/'+cfg.SET_FILENAME #raw data
        raw = mne.io.Raw(raw_fname, preload=True)
        raw.info['bads']=all_ROIlist[i]
        fig=raw.plot_sensors(ch_type='grad')
        fig.savefig('/Users/takeiyuuichi/Dropbox (MEG)/CP/results/grandaverage/ROI/'+pick_list[i])
        plt.close()

#################evoked dataの読み出し################          
    square_list=[]
    circle_list=[]
    for line in all_subject:
        SUBJECT=line[0]
#        DATE=line[1]     
        square_list.append(mne.read_evokeds(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/'+SET_EVENTNAME[0]+'-ave.fif')[0].crop(tmin,tmax))
        circle_list.append(mne.read_evokeds(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/'+SET_EVENTNAME[1]+'-ave.fif')[0].crop(tmin,tmax))

#################NC、CPのデータを取得################                  
    NC_square_list=square_list[0:-3]
    NC_circle_list=circle_list[0:-3]
    CP_square_list=square_list[-3::]
    CP_circle_list=circle_list[-3::]
    
################ROIのデータを取得################              
    square_ROI_data_mag=[]
    circle_ROI_data_mag=[]
    square_ROI_data_grad=[]
    circle_ROI_data_grad=[]
    for i in range(len(all_ROIlist)):
        square_data_mag=[]
        circle_data_mag=[]
        square_data_grad=[]
        circle_data_grad=[]
        for j in range(len(square_list)):
            square_data_mag.append(square_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data)
            circle_data_mag.append(circle_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data)
            square_data_grad.append(square_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data)
            circle_data_grad.append(circle_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data)
        square_ROI_data_mag.append(np.array(square_data_mag))
        circle_ROI_data_mag.append(np.array(circle_data_mag))
        square_ROI_data_grad.append(np.array(square_data_grad))
        circle_ROI_data_grad.append(np.array(circle_data_grad))

#################GFPの計算################          
        
    GFP_square_ROI_data_mag=np.array([np.sqrt(np.sum(np.square(square_ROI_data_mag[i]),axis=1)/square_ROI_data_mag[i].shape[1]) for i in range(len(square_ROI_data_mag))])
    GFP_circle_ROI_data_mag=np.array([np.sqrt(np.sum(np.square(circle_ROI_data_mag[i]),axis=1)/circle_ROI_data_mag[i].shape[1]) for i in range(len(circle_ROI_data_mag))] )
    GFP_sub_ROI_data_mag=np.array([np.sqrt(np.sum(np.square(circle_ROI_data_mag[i]-square_ROI_data_mag[i]),axis=1)/circle_ROI_data_mag[i].shape[1]) for i in range(len(circle_ROI_data_mag))] )
    
    GFP_square_ROI_data_grad=np.array([np.sqrt(np.sum(np.square(square_ROI_data_grad[i]),axis=1)/square_ROI_data_grad[i].shape[1]) for i in range(len(square_ROI_data_grad))])
    GFP_circle_ROI_data_grad=np.array([np.sqrt(np.sum(np.square(circle_ROI_data_grad[i]),axis=1)/circle_ROI_data_grad[i].shape[1]) for i in range(len(circle_ROI_data_grad))] )
    GFP_sub_ROI_data_grad=np.array([np.sqrt(np.sum(np.square(circle_ROI_data_grad[i]-square_ROI_data_grad[i]),axis=1)/circle_ROI_data_grad[i].shape[1]) for i in range(len(circle_ROI_data_grad))] )
      
#################evoked dataのgrandaverageとplot################            
    grandaverage_square_list=   mne.grand_average(square_list, interpolate_bads=True, drop_bads=True)
    grandaverage_circle_list=   mne.grand_average(circle_list, interpolate_bads=True, drop_bads=True)
    grandaverage_list =[grandaverage_square_list,grandaverage_circle_list]
    sub_grandaverage_list= mne.combine_evoked([grandaverage_square_list,-grandaverage_circle_list], 'equal')
    NC_grandaverage_square_list=   mne.grand_average(NC_square_list, interpolate_bads=True, drop_bads=True)
    NC_grandaverage_circle_list=   mne.grand_average(NC_circle_list, interpolate_bads=True, drop_bads=True)
    NC_grandaverage_list =[NC_grandaverage_square_list,NC_grandaverage_circle_list]
    NC_sub_grandaverage_list= mne.combine_evoked([NC_grandaverage_square_list,-NC_grandaverage_circle_list], 'equal')
    CP_grandaverage_square_list=   mne.grand_average(CP_square_list, interpolate_bads=True, drop_bads=True)
    CP_grandaverage_circle_list=   mne.grand_average(CP_circle_list, interpolate_bads=True, drop_bads=True)
    CP_grandaverage_list =[CP_grandaverage_square_list,CP_grandaverage_circle_list]
    CP_sub_grandaverage_list= mne.combine_evoked([CP_grandaverage_square_list,-CP_grandaverage_circle_list], 'equal')
          
    conds = ('square','circle', 'subtract')
    evks_all = dict(zip(conds, [grandaverage_square_list,grandaverage_circle_list,sub_grandaverage_list]))
    
    fig=mne.viz.plot_compare_evokeds(evks_all, colors=dict(square='b', circle='g',subtract='orangered'), picks='grad', axes='topo')
    fig[0].savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/plot_compare_evokeds_grad.png')
    plt.close()

    fig=mne.viz.plot_compare_evokeds(evks_all, colors=dict(square='b', circle='g',subtract='orangered'), picks='mag', axes='topo')
    fig[0].savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/plot_compare_evokeds_mag.png')
    plt.close()
    
#################magnetomatorのROIごとのGFPのPlot################          
    
    
    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,8))
    v_max=np.max(GFP_square_ROI_data_mag[i,:,:])*0.7
    for i,ax in enumerate(axes.flat):
        if i <GFP_square_ROI_data_mag.shape[0]:           
            ax.set_ylim([0,v_max])  
            ax.set_xlim([tmin,tmax])  
            ave_data=np.mean(GFP_square_ROI_data_mag[i,:,:],axis=0)
            ste_data=stats.sem(GFP_square_ROI_data_mag[i,:,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='b',linewidth = 0.5,label='square')       
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
            ave_data=np.mean(GFP_circle_ROI_data_mag[i,:,:],axis=0)
            ste_data=stats.sem(GFP_circle_ROI_data_mag[i,:,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='g',linewidth = 0.5,label='circle')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ave_data=np.mean(GFP_sub_ROI_data_mag[i,:,:],axis=0)
            ste_data=stats.sem(GFP_sub_ROI_data_mag[i,:,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='r',linewidth = 0.5,label='subtract')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)            
            ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')
#        ax.set_ylim=[0,v_max]
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/Ch_average_mag.png')
    plt.close()
#################gradiomatorのROIごとのGFPのPlot################          

    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,8))
    v_max=np.max(GFP_square_ROI_data_grad[i,:,:])*0.9
    for i,ax in enumerate(axes.flat):
        if i <GFP_square_ROI_data_grad.shape[0]:            
            ax.set_ylim([0,v_max])  
            ax.set_xlim([tmin,tmax])  
            ave_data=np.mean(GFP_square_ROI_data_grad[i,:,:],axis=0)
            ste_data=stats.sem(GFP_square_ROI_data_grad[i,:,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='b',linewidth = 0.5,label='square')       
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
            ave_data=np.mean(GFP_circle_ROI_data_grad[i,:,:],axis=0)
            ste_data=stats.sem(GFP_circle_ROI_data_grad[i,:,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='g',linewidth = 0.5,label='circle')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ave_data=np.mean(GFP_sub_ROI_data_grad[i,:,:],axis=0)
            ste_data=stats.sem(GFP_sub_ROI_data_grad[i,:,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='r',linewidth = 0.5,label='subtract')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)            
            ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')
#        ax.set_ylim=[0,v_max]
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/Ch_average_grad.png')
    plt.close()
#################magnetomatorのROIごとのNCのGFPのPlot################    
    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,8))
    v_max=np.max(GFP_square_ROI_data_mag[i,0:-3,:])*0.9
    for i,ax in enumerate(axes.flat):
        if i <GFP_square_ROI_data_mag.shape[0]:            
            ax.set_ylim([0,v_max])  
            ax.set_xlim([tmin,tmax])  
            ave_data=np.mean(GFP_square_ROI_data_mag[i,0:-3,:],axis=0)
            ste_data=stats.sem(GFP_square_ROI_data_mag[i,0:-3,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='b',linewidth = 0.5,label='square')       
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
            ave_data=np.mean(GFP_circle_ROI_data_mag[i,0:-3,:],axis=0)
            ste_data=stats.sem(GFP_circle_ROI_data_mag[i,0:-3,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='g',linewidth = 0.5,label='circle')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ave_data=np.mean(GFP_sub_ROI_data_mag[i,0:-3,:],axis=0)
            ste_data=stats.sem(GFP_sub_ROI_data_mag[i,0:-3,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='r',linewidth = 0.5,label='subtract')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)            
            ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')
#        ax.set_ylim=[0,v_max]
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/NC_Ch_average_mag.png')
    plt.close()
#################gradiomatorのROIごとのNCのGFPのPlot################      
    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,8))
    v_max=np.max(GFP_square_ROI_data_grad[i,0:-3,:])*0.9
    for i,ax in enumerate(axes.flat):
        if i <GFP_square_ROI_data_grad.shape[0]:            
            ax.set_ylim([0,v_max])  
            ax.set_xlim([tmin,tmax])  
            ave_data=np.mean(GFP_square_ROI_data_grad[i,0:-3,:],axis=0)
            ste_data=stats.sem(GFP_square_ROI_data_grad[i,0:-3,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='b',linewidth = 0.5,label='square')       
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
            ave_data=np.mean(GFP_circle_ROI_data_grad[i,0:-3,:],axis=0)
            ste_data=stats.sem(GFP_circle_ROI_data_grad[i,0:-3,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='g',linewidth = 0.5,label='circle')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ave_data=np.mean(GFP_sub_ROI_data_grad[i,0:-3,:],axis=0)
            ste_data=stats.sem(GFP_sub_ROI_data_grad[i,0:-3,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='r',linewidth = 0.5,label='subtract')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)            
            ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')
#        ax.set_ylim=[0,v_max]
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/NC_Ch_average_grad.png')
    plt.close()
#################magnetomatorのROIごとのCPのGFPのPlot################        
    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,8))
    v_max=np.max(GFP_square_ROI_data_mag[i,-3::,:])*0.9
    for i,ax in enumerate(axes.flat):
        if i <GFP_square_ROI_data_mag.shape[0]:            
            ax.set_ylim([0,v_max])  
            ax.set_xlim([tmin,tmax])  
            ave_data=np.mean(GFP_square_ROI_data_mag[i,-3::,:],axis=0)
            ste_data=stats.sem(GFP_square_ROI_data_mag[i,-3::,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='b',linewidth = 0.5,label='square')       
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
            ave_data=np.mean(GFP_circle_ROI_data_mag[i,-3::,:],axis=0)
            ste_data=stats.sem(GFP_circle_ROI_data_mag[i,-3::,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='g',linewidth = 0.5,label='circle')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ave_data=np.mean(GFP_sub_ROI_data_mag[i,-3::,:],axis=0)
            ste_data=stats.sem(GFP_sub_ROI_data_mag[i,-3::,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='r',linewidth = 0.5,label='subtract')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)            
            ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')
#        ax.set_ylim=[0,v_max]
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/CP_Ch_average_mag.png')
    plt.close()
#################gradiomatorのROIごとのCPのGFPのPlot################        
    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,8))
    v_max=np.max(GFP_square_ROI_data_grad[i,-3::,:])*0.9
    for i,ax in enumerate(axes.flat):
        if i <GFP_square_ROI_data_grad.shape[0]:            
            ax.set_ylim([0,v_max])  
            ax.set_xlim([tmin,tmax])  
            ave_data=np.mean(GFP_square_ROI_data_grad[i,-3::,:],axis=0)
            ste_data=stats.sem(GFP_square_ROI_data_grad[i,-3::,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='b',linewidth = 0.5,label='square')       
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
            ave_data=np.mean(GFP_circle_ROI_data_grad[i,-3::,:],axis=0)
            ste_data=stats.sem(GFP_circle_ROI_data_grad[i,-3::,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='g',linewidth = 0.5,label='circle')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ave_data=np.mean(GFP_sub_ROI_data_grad[i,-3::,:],axis=0)
            ste_data=stats.sem(GFP_sub_ROI_data_grad[i,-3::,:],axis=0)
            ax.plot(grandaverage_list[0].times,ave_data, color='r',linewidth = 0.5,label='subtract')
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(grandaverage_list[0].times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)            
            ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')
#        ax.set_ylim=[0,v_max]
    plt.subplots_adjust(wspace=0.4, hspace=0.6)
    plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/CP_Ch_average_grad.png')
    plt.close()    
    
    
################全チャンネルの重ねがき波形################# 
    pick=['grad','mag']        
    for e_i in range(len(SET_EVENTID)):            
        for i in range(2):
            fig=grandaverage_list[e_i].plot_joint(picks=pick[i])
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/plot_joint_'+ SET_EVENTNAME[e_i] +'_'+pick[i]+'.png')
            plt.close()
    for i in range(2):
        fig=sub_grandaverage_list.plot_joint(picks=pick[i])
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/plot_joint_subtract_'+pick[i]+'.png')
        plt.close()    

    pick=['grad','mag']        
    for e_i in range(len(SET_EVENTID)):            
        for i in range(2):
            fig=NC_grandaverage_list[e_i].plot_joint(picks=pick[i])
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/NC_plot_joint_'+ SET_EVENTNAME[e_i] +'_'+pick[i]+'.png')
            plt.close()
    for i in range(2):
        fig=NC_sub_grandaverage_list.plot_joint(picks=pick[i])
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/NC_plot_joint_subtract_'+pick[i]+'.png')
        plt.close()  
        
    pick=['grad','mag']        
    for e_i in range(len(SET_EVENTID)):            
        for i in range(2):
            fig=CP_grandaverage_list[e_i].plot_joint(picks=pick[i])
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/CP_plot_joint_'+ SET_EVENTNAME[e_i] +'_'+pick[i]+'.png')
            plt.close()
    for i in range(2):
        fig=CP_sub_grandaverage_list.plot_joint(picks=pick[i])
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/CP_plot_joint_subtract_'+pick[i]+'.png')
        plt.close()          
        
        

##### まとめてプロット       
    col=3
    row=6/col
    cols=col*2.5
    rows=row*2
    dpis = 300
    fig = plt.figure(figsize=(cols,rows),dpi=dpis)            
    pi=1        
    for i in range(2):
        for e_i in range(len(SET_EVENTID)): 
            plot_num = pi
            ax=fig.add_subplot(row, col, plot_num)
            ax.set_title(SET_EVENTNAME[e_i] +'_'+pick[i])
            img = Image.open(cfg.SET_RESULT_DIR + '/grandaverage/evoked/plot_joint_'+ SET_EVENTNAME[e_i] +'_'+pick[i]+'.png')
            plt.imshow(img, cmap='gray')       
            plt.axis("off")
            pi = pi+1              
        plot_num = pi
        ax=fig.add_subplot(row, col, plot_num)
        ax.set_title('subtract_'+pick[i])
        img = Image.open(cfg.SET_RESULT_DIR + '/grandaverage/evoked/plot_joint_subtract_'+pick[i]+'.png')
        plt.imshow(img, cmap='gray')   
        plt.axis("off")
        pi = pi+1  
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/plot_joint_all.png')
    plt.close()
    
##### まとめてプロット       
    col=3
    row=6/col
    cols=col*2.5
    rows=row*2
    dpis = 300
    fig = plt.figure(figsize=(cols,rows),dpi=dpis)            
    pi=1        
    for i in range(2):
        for e_i in range(len(SET_EVENTID)): 
            plot_num = pi
            ax=fig.add_subplot(row, col, plot_num)
            ax.set_title(SET_EVENTNAME[e_i] +'_'+pick[i])
            img = Image.open(cfg.SET_RESULT_DIR + '/grandaverage/evoked/NC_plot_joint_'+ SET_EVENTNAME[e_i] +'_'+pick[i]+'.png')
            plt.imshow(img, cmap='gray')       
            plt.axis("off")
            pi = pi+1              
        plot_num = pi
        ax=fig.add_subplot(row, col, plot_num)
        ax.set_title('subtract_'+pick[i])
        img = Image.open(cfg.SET_RESULT_DIR + '/grandaverage/evoked/NC_plot_joint_subtract_'+pick[i]+'.png')
        plt.imshow(img, cmap='gray')   
        plt.axis("off")
        pi = pi+1  
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/NC_plot_joint_all.png')
    plt.close()
                
##### まとめてプロット       
    col=3
    row=6/col
    cols=col*2.5
    rows=row*2
    dpis = 300
    fig = plt.figure(figsize=(cols,rows),dpi=dpis)            
    pi=1        
    for i in range(2):
        for e_i in range(len(SET_EVENTID)): 
            plot_num = pi
            ax=fig.add_subplot(row, col, plot_num)
            ax.set_title(SET_EVENTNAME[e_i] +'_'+pick[i])
            img = Image.open(cfg.SET_RESULT_DIR + '/grandaverage/evoked/CP_plot_joint_'+ SET_EVENTNAME[e_i] +'_'+pick[i]+'.png')
            plt.imshow(img, cmap='gray')       
            plt.axis("off")
            pi = pi+1              
        plot_num = pi
        ax=fig.add_subplot(row, col, plot_num)
        ax.set_title('subtract_'+pick[i])
        img = Image.open(cfg.SET_RESULT_DIR + '/grandaverage/evoked/CP_plot_joint_subtract_'+pick[i]+'.png')
        plt.imshow(img, cmap='gray')   
        plt.axis("off")
        pi = pi+1  
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/evoked/CP_plot_joint_all.png')
    plt.close()
                
    
    
    