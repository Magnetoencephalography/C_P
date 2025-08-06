#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 05:56:04 2020

@author: takeiyuuichi
"""


#setting##############################################
n_jobs=16 #並列処理の数
t_n_jobs=16
PARAMETER_DIR='/Volumes/Siena/CP/parameter/'
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

R_fusiform_list=[
'MEG 2431', 'MEG 2432', 'MEG 2433',
'MEG 2521', 'MEG 2522', 'MEG 2523',
'MEG 2321', 'MEG 2322', 'MEG 2323',
'MEG 2511', 'MEG 2512', 'MEG 2513']
# 'MEG 2423',
# 'MEG 2412',
# 'MEG 2322',
# 'MEG 1342',
# 'MEG 1333',
# 'MEG 1312'
# 

L_fusiform_list=[
'MEG 1721', 'MEG 1722', 'MEG 1723',
'MEG 1641', 'MEG 1642', 'MEG 1643',
'MEG 1941', 'MEG 1942', 'MEG 1943',
'MEG 1731', 'MEG 1732', 'MEG 1733',]

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
import numpy as np
import sys
import os  
import mne
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

#####################解析データの読み込み########################       
    power_square_list=[]
    power_circle_list=[]
    itc_square_list=[]
    itc_circle_list=[]
    for line in all_subject:
        SUBJECT=line[0]
        power_square_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/wavelet/'+SET_EVENTNAME[0]+'_power')[0].crop(tmin=-0.1, tmax=0.5))
        power_circle_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/wavelet/'+SET_EVENTNAME[1]+'_power')[0].crop(tmin=-0.1, tmax=0.5))
        itc_square_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/wavelet/'+SET_EVENTNAME[0]+'_itc')[0].crop(tmin=-0.1, tmax=0.5))
        itc_circle_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/wavelet/'+SET_EVENTNAME[1]+'_itc')[0].crop(tmin=-0.1, tmax=0.5))

#################NC、CPのデータを取得################               
    NC_power_square_list=power_square_list[0:-3]
    NC_power_circle_list=power_circle_list[0:-3]
    CP_power_square_list=power_square_list[-3::]
    CP_power_circle_list=power_circle_list[-3::]        
    NC_itc_square_list=itc_square_list[0:-3]
    NC_itc_circle_list=itc_circle_list[0:-3]
    CP_itc_square_list=itc_square_list[-3::]
    CP_itc_circle_list=itc_circle_list[-3::]        

#################それぞれのデータのgrandaverage################         
    grandaverage_power_square_list=   mne.grand_average(power_square_list, interpolate_bads=True, drop_bads=True)
    grandaverage_power_circle_list=   mne.grand_average(power_circle_list, interpolate_bads=True, drop_bads=True)
    sub_grandaverage_power_list= grandaverage_power_square_list.__sub__(grandaverage_power_circle_list)

    grandaverage_itc_square_list=   mne.grand_average(itc_square_list, interpolate_bads=True, drop_bads=True)
    grandaverage_itc_circle_list=   mne.grand_average(itc_circle_list, interpolate_bads=True, drop_bads=True)
    sub_grandaverage_itc_list= grandaverage_itc_square_list.__sub__(grandaverage_itc_circle_list)
        
    NC_grandaverage_power_square_list=   mne.grand_average(NC_power_square_list, interpolate_bads=True, drop_bads=True)
    NC_grandaverage_power_circle_list=   mne.grand_average(NC_power_circle_list, interpolate_bads=True, drop_bads=True)
    sub_NC_grandaverage_power_list= NC_grandaverage_power_square_list.__sub__(NC_grandaverage_power_circle_list)        

    CP_grandaverage_power_square_list=   mne.grand_average(CP_power_square_list, interpolate_bads=True, drop_bads=True)
    CP_grandaverage_power_circle_list=   mne.grand_average(CP_power_circle_list, interpolate_bads=True, drop_bads=True)
    sub_CP_grandaverage_power_list= CP_grandaverage_power_square_list.__sub__(CP_grandaverage_power_circle_list)        
        
    NC_grandaverage_itc_square_list=   mne.grand_average(NC_itc_square_list, interpolate_bads=True, drop_bads=True)
    NC_grandaverage_itc_circle_list=   mne.grand_average(NC_itc_circle_list, interpolate_bads=True, drop_bads=True)
    sub_NC_grandaverage_itc_list= NC_grandaverage_itc_square_list.__sub__(NC_grandaverage_itc_circle_list)        

    CP_grandaverage_itc_square_list=   mne.grand_average(CP_itc_square_list, interpolate_bads=True, drop_bads=True)
    CP_grandaverage_itc_circle_list=   mne.grand_average(CP_itc_circle_list, interpolate_bads=True, drop_bads=True)
    sub_CP_grandaverage_itc_list= CP_grandaverage_itc_square_list.__sub__(CP_grandaverage_itc_circle_list)    


#################grandaverageの全chのplot################    
    mean=np.mean(grandaverage_power_square_list.data)
    std=np.std(grandaverage_power_square_list.data)
    fig=grandaverage_power_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/grandaverage_power_square_list.png',dpi=300)
    plt.close()    
    mean=np.mean(grandaverage_power_circle_list.data)
    std=np.std(grandaverage_power_circle_list.data)
    fig=grandaverage_power_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/grandaverage_power_circle_list.png',dpi=300)
    plt.close()    
    mean=np.mean(sub_grandaverage_power_list.data)
    std=np.std(sub_grandaverage_power_list.data)
    fig=sub_grandaverage_power_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/sub_grandaverage_power_list.png',dpi=300)
    plt.close()        
 
    mean=np.mean(NC_grandaverage_power_square_list.data)
    std=np.std(NC_grandaverage_power_square_list.data)
    fig=NC_grandaverage_power_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_grandaverage_power_square_list.png',dpi=300)
    plt.close()    
    mean=np.mean(NC_grandaverage_power_circle_list.data)
    std=np.std(NC_grandaverage_power_circle_list.data)
    fig=NC_grandaverage_power_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_grandaverage_power_circle_list.png',dpi=300)
    plt.close()    
    mean=np.mean(sub_NC_grandaverage_power_list.data)
    std=np.std(sub_NC_grandaverage_power_list.data)
    fig=sub_NC_grandaverage_power_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/sub_NC_grandaverage_power_list.png',dpi=300)
    plt.close()        

    mean=np.mean(CP_grandaverage_power_square_list.data)
    std=np.std(CP_grandaverage_power_square_list.data)
    fig=CP_grandaverage_power_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/CP_grandaverage_power_square_list.png',dpi=300)
    plt.close()    
    mean=np.mean(CP_grandaverage_power_circle_list.data)
    std=np.std(CP_grandaverage_power_circle_list.data)
    fig=CP_grandaverage_power_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/CP_grandaverage_power_circle_list.png',dpi=300)
    plt.close()    
    mean=np.mean(sub_CP_grandaverage_power_list.data)
    std=np.std(sub_CP_grandaverage_power_list.data)
    fig=sub_CP_grandaverage_power_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/sub_CP_grandaverage_power_list.png',dpi=300)
    plt.close()      
    
    
    mean=np.mean(grandaverage_itc_square_list.data)
    std=np.std(grandaverage_itc_square_list.data)
    fig=grandaverage_itc_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/grandaverage_itc_square_list.png',dpi=300)
    plt.close()    
    mean=np.mean(grandaverage_itc_circle_list.data)
    std=np.std(grandaverage_itc_circle_list.data)
    fig=grandaverage_itc_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/grandaverage_itc_circle_list.png',dpi=300)
    plt.close()    
    mean=np.mean(sub_grandaverage_itc_list.data)
    std=np.std(sub_grandaverage_itc_list.data)
    fig=sub_grandaverage_itc_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/sub_grandaverage_itc_list.png',dpi=300)
    plt.close()        
       
 
    mean=np.mean(NC_grandaverage_itc_square_list.data)
    std=np.std(NC_grandaverage_itc_square_list.data)
    fig=NC_grandaverage_itc_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_grandaverage_itc_square_list.png',dpi=300)
    plt.close()    
    mean=np.mean(NC_grandaverage_itc_circle_list.data)
    std=np.std(NC_grandaverage_itc_circle_list.data)
    fig=NC_grandaverage_itc_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_grandaverage_itc_circle_list.png',dpi=300)
    plt.close()    
    mean=np.mean(sub_NC_grandaverage_itc_list.data)
    std=np.std(sub_NC_grandaverage_itc_list.data)
    fig=sub_NC_grandaverage_itc_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/sub_NC_grandaverage_itc_list.png',dpi=300)
    plt.close()     
    
    mean=np.mean(CP_grandaverage_itc_square_list.data)
    std=np.std(CP_grandaverage_itc_square_list.data)
    fig=CP_grandaverage_itc_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/CP_grandaverage_itc_square_list.png',dpi=300)
    plt.close()    
    mean=np.mean(CP_grandaverage_itc_circle_list.data)
    std=np.std(CP_grandaverage_itc_circle_list.data)
    fig=CP_grandaverage_itc_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/CP_grandaverage_itc_circle_list.png',dpi=300)
    plt.close()    
    mean=np.mean(sub_CP_grandaverage_itc_list.data)
    std=np.std(sub_CP_grandaverage_itc_list.data)
    fig=sub_CP_grandaverage_itc_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/sub_CP_grandaverage_itc_list.png',dpi=300)
    plt.close()     

################ROIのデータを取得################ 
    all_ROIlist=[R_Occ_list,L_Occ_list,R_fusiform_list,L_fusiform_list,R_midTemp_list,L_midTemp_list,R_Temptip_list,L_Temptip_list]

    power_ROI_square_list_mag=[]
    power_ROI_square_list_grad=[]
    itc_ROI_square_list_mag=[]
    itc_ROI_square_list_grad=[]
    power_ROI_circle_list_mag=[]
    power_ROI_circle_list_grad=[]
    itc_ROI_circle_list_mag=[]
    itc_ROI_circle_list_grad=[]    

    power_ROI_square_list_all=[]
    itc_ROI_square_list_all=[]
    power_ROI_circle_list_all=[]
    itc_ROI_circle_list_all=[]
    
    
#    square_ROI_data_grad=[]
#    circle_ROI_data_grad=[]
    for i in range(len(all_ROIlist)):
        power_square_list_mag=[]
        power_square_list_grad=[]
        itc_square_list_mag=[]
        itc_square_list_grad=[]
        power_circle_list_mag=[]
        power_circle_list_grad=[]
        itc_circle_list_mag=[]
        itc_circle_list_grad=[]  
        power_square_list_all=[]
        itc_square_list_all=[]
        power_circle_list_all=[]
        itc_circle_list_all=[]
        for j in range(len(power_square_list)):
            power_square_list_mag.append(power_square_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data)
            power_square_list_grad.append(power_square_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data)
            power_circle_list_mag.append(power_circle_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data)
            power_circle_list_grad.append(power_circle_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data)
            itc_square_list_mag.append(itc_square_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data)
            itc_square_list_grad.append(itc_square_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data)
            itc_circle_list_mag.append(itc_circle_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data)
            itc_circle_list_grad.append(itc_circle_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data)

            power_square_list_all.append(power_square_list[j].copy().pick_channels(all_ROIlist[i]).data)
            power_circle_list_all.append(power_circle_list[j].copy().pick_channels(all_ROIlist[i]).data)
            itc_square_list_all.append(itc_square_list[j].copy().pick_channels(all_ROIlist[i]).data)
            itc_circle_list_all.append(itc_circle_list[j].copy().pick_channels(all_ROIlist[i]).data)
            
        power_ROI_square_list_mag.append(np.array(power_square_list_mag))
        power_ROI_square_list_grad.append(np.array(power_square_list_grad))
        itc_ROI_square_list_mag.append(np.array(itc_square_list_mag))
        itc_ROI_square_list_grad.append(np.array(itc_square_list_grad))
        power_ROI_circle_list_mag.append(np.array(power_circle_list_mag))
        power_ROI_circle_list_grad.append(np.array(power_circle_list_grad))
        itc_ROI_circle_list_mag.append(np.array(itc_circle_list_mag))
        itc_ROI_circle_list_grad.append(np.array(itc_circle_list_grad))        

        power_ROI_square_list_all.append(np.array(power_square_list_all))
        itc_ROI_square_list_all.append(np.array(itc_square_list_all))
        power_ROI_circle_list_all.append(np.array(power_circle_list_all))
        itc_ROI_circle_list_all.append(np.array(itc_circle_list_all))
        
################全chのplot###############         
    times=power_square_list[0].times
    freqs=power_square_list[0].freqs
    
    power_list=[power_ROI_square_list_mag,power_ROI_circle_list_mag,power_ROI_square_list_grad,power_ROI_circle_list_grad,power_ROI_square_list_all,power_ROI_circle_list_all]
    power_list_names=['power_ROI_square_list_mag','power_ROI_circle_list_mag','power_ROI_square_list_grad','power_ROI_circle_list_grad','power_ROI_square_list_all','power_ROI_circle_list_all']
    
    for j in range(len(power_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        mean=np.mean(np.array(power_list[0][0]))
        std=np.std(np.array(power_list[0][0]))
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.mean( np.array(power_list[j][i]),axis=0),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/grandaverage_'+power_list_names[j]+'.png',dpi=300)
        plt.close()  
        
    itc_list=[itc_ROI_square_list_mag,itc_ROI_circle_list_mag,itc_ROI_square_list_grad,itc_ROI_circle_list_grad,itc_ROI_square_list_all,itc_ROI_circle_list_all]
    itc_list_names=['itc_ROI_square_list_mag','itc_ROI_circle_list_mag','itc_ROI_square_list_grad','itc_ROI_circle_list_grad','itc_ROI_square_list_all','itc_ROI_circle_list_all']
    
    for j in range(len(itc_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        mean=np.mean(np.array(itc_list[0][0]))
        std=np.std(np.array(itc_list[0][0]))
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.mean( np.array(itc_list[j][i]),axis=0),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/grandaverage_'+itc_list_names[j]+'.png',dpi=300)
        plt.close()  
        
    for j in range(len(power_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        mean=np.mean(np.array(power_list[0][0][0:-3,:,:,:]))
        std=np.std(np.array(power_list[0][0][0:-3,:,:,:]))
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.mean( np.array(power_list[j][i][0:-3,:,:,:]),axis=0),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/CP_grandaverage_'+power_list_names[j]+'.png',dpi=300)
        plt.close()  

    for j in range(len(itc_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        mean=np.mean(np.array(itc_list[0][0][0:-3,:,:,:]))
        std=np.std(np.array(itc_list[0][0][0:-3,:,:,:]))
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.mean( np.array(itc_list[j][i][0:-3,:,:,:]),axis=0),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/CP_grandaverage_'+itc_list_names[j]+'.png',dpi=300)
        plt.close()  
      
        
        
    
    from scipy import stats
################各周波数帯域の各ROIのmag、gradの同時plot############### 
    freq_range=[[4,7],[8,13],[14,38],[40,98]]
    freq_name=['theta','alpha','beta','gamma']
    sub_list=['all','NC','CP']
    legend_list=['square mag','circle mag','square grad','circle grad']
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for s_i in range(len(sub_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat):     
                data=np.mean(power_ROI_square_list_mag[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='g',linewidth = 0.5,label=legend_list[0])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
              
                data=np.mean(power_ROI_circle_list_mag[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='r',linewidth = 0.5,label=legend_list[1])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)  
               
                data=np.mean(power_ROI_square_list_grad[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='b',linewidth = 0.5,label=legend_list[2])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
             
                data=np.mean(power_ROI_circle_list_grad[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='y',linewidth = 0.5,label=legend_list[3])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='y', alpha=0.1)  
                
                ax.set_title(pick_list[i])
                
    #        plt.legend(loc='upper left')
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/mag_grad_'+sub_list[s_i]+'_'+freq_name[f_i]+'_power.png',dpi=300)

################各周波数帯域の各ROIのmag、gradの平均のplot############### 
    legend_list=['square all','circle all']
    sub_list=['all','NC','CP']
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for s_i in range(len(sub_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat):     
                data=np.mean(power_ROI_square_list_all[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='g',linewidth = 0.5,label=legend_list[0])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
              
                data=np.mean(power_ROI_circle_list_all[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='r',linewidth = 0.5,label=legend_list[1])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)  
               
                
                ax.set_title(pick_list[i])
                
    #        plt.legend(loc='upper left')
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/all_'+sub_list[s_i]+'_'+freq_name[f_i]+'_power.png',dpi=300)

################各周波数帯域の各ROIのmag、gradの同時plot############### 
    legend_list=['square mag','circle mag','square grad','circle grad']
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for s_i in range(len(sub_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat):     
                data=np.mean(itc_ROI_square_list_mag[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='g',linewidth = 0.5,label=legend_list[0])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
              
                data=np.mean(itc_ROI_circle_list_mag[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='r',linewidth = 0.5,label=legend_list[1])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)  
               
                data=np.mean(itc_ROI_square_list_grad[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='b',linewidth = 0.5,label=legend_list[2])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
             
                data=np.mean(itc_ROI_circle_list_grad[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='y',linewidth = 0.5,label=legend_list[3])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='y', alpha=0.1)  
                
                ax.set_title(pick_list[i])
                
    #        plt.legend(loc='upper left')
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/mag_grad_'+sub_list[s_i]+'_'+freq_name[f_i]+'_itc.png',dpi=300)

################各周波数帯域の各ROIのmag、gradの平均のplot############### 
    legend_list=['square all','circle all']
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for s_i in range(len(sub_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat):     
                data=np.mean(itc_ROI_square_list_all[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='g',linewidth = 0.5,label=legend_list[0])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
               
                data=np.mean(itc_ROI_circle_list_all[i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='r',linewidth = 0.5,label=legend_list[1])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)  
               
                
                ax.set_title(pick_list[i])
                
    #        plt.legend(loc='upper left')
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/all_'+sub_list[s_i]+'_'+freq_name[f_i]+'_itc.png',dpi=300)

        
################各周波数帯域の各ROIのNCとCPの平均値のplot###############         
    power_list=[power_ROI_square_list_mag,power_ROI_circle_list_mag,power_ROI_square_list_grad,power_ROI_circle_list_grad,power_ROI_square_list_all,power_ROI_circle_list_all]
    power_list_names=['power_ROI_square_list_mag','power_ROI_circle_list_mag','power_ROI_square_list_grad','power_ROI_circle_list_grad','power_ROI_square_list_all','power_ROI_circle_list_all']

    sub_list=['NC','CP']
    sub_index=[np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    color_list=['g','r']
    legend_list=['square mag','circle mag','square grad','circle grad','square all','circle all']
    for d_i in range(len(power_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                for s_i in range(len(sub_list)):
                    data=np.mean(power_list[d_i][i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                    data=np.mean(data,axis=1)
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_CP_'+power_list_names[d_i]+'_'+freq_name[f_i]+'_power.png',dpi=300)

    itc_list=[itc_ROI_square_list_mag,itc_ROI_circle_list_mag,itc_ROI_square_list_grad,itc_ROI_circle_list_grad,itc_ROI_square_list_all,itc_ROI_circle_list_all]
    itc_list_names=['itc_ROI_square_list_mag','itc_ROI_circle_list_mag','itc_ROI_square_list_grad','itc_ROI_circle_list_grad','itc_ROI_square_list_all','itc_ROI_circle_list_all']
            
    for d_i in range(len(itc_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                for s_i in range(len(sub_list)):
                    data=np.mean(itc_list[d_i][i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                    data=np.mean(data,axis=1)
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_CP_'+itc_list_names[d_i]+'_'+freq_name[f_i]+'_itc.png',dpi=300)
     
        
     
        
################各周波数帯域の各ROIのNCとCPの個別波形のplot###############     
    sub_list=['NC','CP']
    sub_index=[np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    color_list=['g','r']
    
    for d_i in range(len(power_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                s_i=0
                data=np.mean(power_list[d_i][i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                s_i=1
                data=np.mean(power_list[d_i][i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                for h_i in range(len(sub_index[1])):
                    ax.plot(times,data[h_i,:], color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_all_CP_'+power_list_names[d_i]+'_'+freq_name[f_i]+'_power.png',dpi=300)
            
            
    for d_i in range(len(itc_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                s_i=0
                data=np.mean(itc_list[d_i][i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                s_i=1
                data=np.mean(itc_list[d_i][i][sub_index[s_i],:,:,:][:,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=2)
                data=np.mean(data,axis=1)
                for h_i in range(len(sub_index[1])):
                    ax.plot(times,data[h_i,:], color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/wavelet/NC_all_CP_'+itc_list_names[d_i]+'_'+freq_name[f_i]+'_itc.png',dpi=300)
            
        
 
################各散布図の作成############### 
    NC_power_circle_list_R_fusiform=np.mean(power_circle_list_R_fusiform[0:-3,:,:,:],axis=1) 
    CP_power_circle_list_R_fusiform=np.mean(power_circle_list_R_fusiform[-3::,:,:,:],axis=1) 
    times=power_circle_list[0].times
    freqs=power_circle_list[0].freqs 
    time_index=(times>=0.1)*(times<=0.3)
    i=1
    NC_power_circle_list_R_fusiform=NC_power_circle_list_R_fusiform[:,(freqs>=freq_range[i][0])*(freqs<=freq_range[i][1]),:][:,:,time_index]
    NC_power_circle_list_R_fusiform=np.mean(np.mean(NC_power_circle_list_R_fusiform,axis=1),axis=1)
    CP_power_circle_list_R_fusiform=CP_power_circle_list_R_fusiform[:,(freqs>=freq_range[i][0])*(freqs<=freq_range[i][1]),:][:,:,time_index]
    CP_power_circle_list_R_fusiform=np.mean(np.mean(CP_power_circle_list_R_fusiform,axis=1),axis=1)
    plt.scatter(np.ones(len(NC_power_circle_list_R_fusiform)),NC_power_circle_list_R_fusiform)    
    plt.scatter(np.ones(len(CP_power_circle_list_R_fusiform))*2,CP_power_circle_list_R_fusiform) 
        
  
    NC_power_circle_list_L_temp=np.mean(power_circle_list_L_temp[0:-3,:,:,:],axis=1) 
    CP_power_circle_list_L_temp=np.mean(power_circle_list_L_temp[-3::,:,:,:],axis=1) 
    times=power_circle_list[0].times
    freqs=power_circle_list[0].freqs 
    time_index=(times>=0.2)*(times<=0.4)
    i=2
    NC_power_circle_list_L_temp=NC_power_circle_list_L_temp[:,(freqs>=freq_range[i][0])*(freqs<=freq_range[i][1]),:][:,:,time_index]
    NC_power_circle_list_L_temp=np.mean(np.mean(NC_power_circle_list_L_temp,axis=1),axis=1)
    CP_power_circle_list_L_temp=CP_power_circle_list_L_temp[:,(freqs>=freq_range[i][0])*(freqs<=freq_range[i][1]),:][:,:,time_index]
    CP_power_circle_list_L_temp=np.mean(np.mean(CP_power_circle_list_L_temp,axis=1),axis=1)
    plt.scatter(np.ones(len(NC_power_circle_list_L_temp)),NC_power_circle_list_L_temp)    
    plt.scatter(np.ones(len(CP_power_circle_list_L_temp))*2,CP_power_circle_list_L_temp)             
        
        
        