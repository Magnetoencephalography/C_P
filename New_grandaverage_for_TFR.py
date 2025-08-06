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
#n_jobs=16 #並列処理の数
t_n_jobs=16
PARAMETER_DIR='/Volumes/Siena/CP/parameter'
set_environment='main'
#
#n_jobs=16 #並列処理の数
t_n_jobs=16
#PARAMETER_DIR='/Users/takeiyuuichi/Dropbox (MEG)/CP/parameter'
#n_jobs=40 #並列処理の数


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
'MEG 2311', 'MEG 2312', 'MEG 2313',
'MEG 2331', 'MEG 2332', 'MEG 2333',
'MEG 2341', 'MEG 2342', 'MEG 2343',
'MEG 2321', 'MEG 2322', 'MEG 2323',
'MEG 2511', 'MEG 2512', 'MEG 2513',
'MEG 2531', 'MEG 2532', 'MEG 2533',
'MEG 2541', 'MEG 2542', 'MEG 2543',
'MEG 2031', 'MEG 2032', 'MEG 2033',
'MEG 2021', 'MEG 2022', 'MEG 2023',
'MEG 2131', 'MEG 2132', 'MEG 2133',
'MEG 2241', 'MEG 2242', 'MEG 2243']


L_Occ_list=[
'MEG 1931', 'MEG 1932', 'MEG 1933',
'MEG 1921', 'MEG 1922', 'MEG 1923',
'MEG 1941', 'MEG 1942', 'MEG 1943',
'MEG 1731', 'MEG 1732', 'MEG 1733',
'MEG 1741', 'MEG 1742', 'MEG 1743',
'MEG 1711', 'MEG 1712', 'MEG 1713',
'MEG 1911', 'MEG 1912', 'MEG 1913',
'MEG 2011', 'MEG 2012', 'MEG 2013',
'MEG 2041', 'MEG 2042', 'MEG 2043',
'MEG 2141', 'MEG 2142', 'MEG 2143',
'MEG 1831', 'MEG 1832', 'MEG 1833']


R_fusiform_list=[
'MEG 2411', 'MEG 2412', 'MEG 2413',
'MEG 2421', 'MEG 2422', 'MEG 2423',
'MEG 2441', 'MEG 2442', 'MEG 2443',
'MEG 2641', 'MEG 2642', 'MEG 2643',
'MEG 2521', 'MEG 2522', 'MEG 2523',
'MEG 2431', 'MEG 2432', 'MEG 2433',
'MEG 2631', 'MEG 2632', 'MEG 2633',
'MEG 2221', 'MEG 2222', 'MEG 2223',
'MEG 2621', 'MEG 2622', 'MEG 2623',
'MEG 2231', 'MEG 2232', 'MEG 2233',
'MEG 2211', 'MEG 2212', 'MEG 2213']

L_fusiform_list=[
'MEG 1641', 'MEG 1642', 'MEG 1643',
'MEG 1721', 'MEG 1722', 'MEG 1723',
'MEG 1521', 'MEG 1522', 'MEG 1523',
'MEG 1611', 'MEG 1612', 'MEG 1613',
'MEG 1621', 'MEG 1622', 'MEG 1623',
'MEG 1531', 'MEG 1532', 'MEG 1533',
'MEG 1631', 'MEG 1632', 'MEG 1633',
'MEG 1811', 'MEG 1812', 'MEG 1813',
'MEG 1541', 'MEG 1542', 'MEG 1543',
'MEG 1841', 'MEG 1842', 'MEG 1843',
'MEG 1821', 'MEG 1822', 'MEG 1823']

R_midTemp_list=[
'MEG 1321', 'MEG 1322', 'MEG 1323',
'MEG 1331', 'MEG 1332', 'MEG 1333',
'MEG 1341', 'MEG 1342', 'MEG 1343',
'MEG 1441', 'MEG 1442', 'MEG 1443',
'MEG 1311', 'MEG 1312', 'MEG 1313',
'MEG 1431', 'MEG 1432', 'MEG 1433',
'MEG 1131', 'MEG 1132', 'MEG 1133',
'MEG 1121', 'MEG 1122', 'MEG 1123',
'MEG 1111', 'MEG 1112', 'MEG 1113',
'MEG 2611', 'MEG 2612', 'MEG 2613',
'MEG 1141', 'MEG 1142', 'MEG 1143']

L_midTemp_list=[
'MEG 1511', 'MEG 1512', 'MEG 1513',
'MEG 0241', 'MEG 0242', 'MEG 0243',
'MEG 0141', 'MEG 0142', 'MEG 0143',
'MEG 0131', 'MEG 0132', 'MEG 0133',
'MEG 0211', 'MEG 0212', 'MEG 0213',
'MEG 0221', 'MEG 0222', 'MEG 0223',
'MEG 0441', 'MEG 0442', 'MEG 0443',
'MEG 0431', 'MEG 0432', 'MEG 0433',
'MEG 0411', 'MEG 0412', 'MEG 0413',
'MEG 0421', 'MEG 0422', 'MEG 0423',
'MEG 0231', 'MEG 0232', 'MEG 0233']


R_Temptip_list=[
'MEG 2611', 'MEG 2612', 'MEG 2613',
'MEG 1331', 'MEG 1332', 'MEG 1333',
'MEG 1341', 'MEG 1342', 'MEG 1343',
'MEG 1131', 'MEG 1132', 'MEG 1133',
'MEG 1321', 'MEG 1322', 'MEG 1323',
'MEG 1311', 'MEG 1312', 'MEG 1313',
'MEG 1221', 'MEG 1222', 'MEG 1223',
'MEG 1441', 'MEG 1442', 'MEG 1443',
'MEG 1411', 'MEG 1412', 'MEG 1413',
'MEG 1421', 'MEG 1422', 'MEG 1423',
'MEG 1431', 'MEG 1432', 'MEG 1433',]

L_Temptip_list=[
'MEG 0121', 'MEG 0122', 'MEG 0123',
'MEG 0111', 'MEG 0112', 'MEG 0113',
'MEG 0221', 'MEG 0222', 'MEG 0223',
'MEG 0341', 'MEG 0342', 'MEG 0343',
'MEG 0211', 'MEG 0212', 'MEG 0213',
'MEG 0131', 'MEG 0132', 'MEG 0133',
'MEG 1511', 'MEG 1512', 'MEG 1513',
'MEG 0241', 'MEG 0242', 'MEG 0243',
'MEG 0231', 'MEG 0232', 'MEG 0233',
'MEG 0441', 'MEG 0442', 'MEG 0443',
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
def baseline_correction(data,times,baseline):
    data=np.mean(data,axis=0)
    time_index=(times>baseline[0])*(times<baseline[1])
    data=np.array([(data[i,:]-np.mean(data[i,time_index]))/np.std(data[i,time_index]) for i in range(data.shape[0])])
    return data

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
        power_square_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/'+SET_EVENTNAME[0]+'_power')[0].crop(tmin=-0.1, tmax=0.5))
        power_circle_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/'+SET_EVENTNAME[1]+'_power')[0].crop(tmin=-0.1, tmax=0.5))
        itc_square_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/'+SET_EVENTNAME[0]+'_itc')[0].crop(tmin=-0.1, tmax=0.5))
        itc_circle_list.append(mne.time_frequency.read_tfrs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/'+SET_EVENTNAME[1]+'_itc')[0].crop(tmin=-0.1, tmax=0.5))

#################NC、CPのデータを取得################    
    ch_list=[power_circle_list[i].info['ch_names'] for i in range(len(power_square_list))]
    picks=ch_list[0]
    for i in range(len(ch_list)-1):
        picks=set(picks) & set(ch_list[i+1])
    
    
    power_square_list=[power_square_list[i].pick_channels(picks) for i in range(len(power_square_list))]
    power_circle_list=[power_circle_list[i].pick_channels(picks) for i in range(len(power_circle_list))]
    itc_square_list=[itc_square_list[i].pick_channels(picks) for i in range(len(itc_square_list))]
    itc_circle_list=[itc_circle_list[i].pick_channels(picks) for i in range(len(itc_circle_list))]
    sub_power_list=[power_circle_list[i]-power_square_list[i] for i in range(len(power_circle_list))] 
    sub_itc_list=[itc_circle_list[i]-itc_square_list[i] for i in range(len(itc_circle_list))] 




           
    NC_power_square_list=power_square_list[0:-3]
    NC_power_circle_list=power_circle_list[0:-3]
    CP_power_square_list=power_square_list[-3::]
    CP_power_circle_list=power_circle_list[-3::]      
    sub_NC_power_list=[NC_power_circle_list[i]-NC_power_square_list[i] for i in range(len(NC_power_circle_list))]
    sub_CP_power_list=[CP_power_circle_list[i]-CP_power_square_list[i] for i in range(len(CP_power_circle_list))]
    NC_itc_square_list=itc_square_list[0:-3]
    NC_itc_circle_list=itc_circle_list[0:-3]
    CP_itc_square_list=itc_square_list[-3::]
    CP_itc_circle_list=itc_circle_list[-3::]        
    sub_NC_itc_list=[NC_itc_circle_list[i]-NC_itc_square_list[i] for i in range(len(NC_itc_circle_list))]
    sub_CP_itc_list=[CP_itc_circle_list[i]-CP_itc_square_list[i] for i in range(len(CP_itc_circle_list))]

#################それぞれのデータのgrandaverage################    
    NC_power_data=np.array([sub_NC_power_list[i].data for i in range(len(NC_power_circle_list))])
    NC_power_mean=np.mean(NC_power_data,axis=0)
    NC_power_std=np.std(NC_power_data,axis=0)
    z_CP_power_sub=np.zeros([len(CP_power_square_list),NC_power_mean.shape[0],NC_power_mean.shape[1],NC_power_mean.shape[2]])
    NC_itc_data=np.array([sub_NC_itc_list[i].data for i in range(len(NC_itc_circle_list))])
    NC_itc_mean=np.mean(NC_itc_data,axis=0)
    NC_itc_std=np.std(NC_itc_data,axis=0)
    z_CP_itc_sub=np.zeros([len(CP_itc_square_list),NC_itc_mean.shape[0],NC_itc_mean.shape[1],NC_itc_mean.shape[2]])
    for s_i in range(len(CP_power_square_list)):
        for f_i in range(CP_power_square_list[s_i].data.shape[1]):
            for t_i in range(CP_power_square_list[s_i].data.shape[2]):
                z_CP_power_sub[s_i,:,f_i,t_i]=(sub_CP_power_list[s_i].data[:,f_i,t_i]-NC_power_mean[:,f_i,t_i])/NC_power_std[:,f_i,t_i]
                z_CP_itc_sub[s_i,:,f_i,t_i]=(sub_CP_itc_list[s_i].data[:,f_i,t_i]-NC_itc_mean[:,f_i,t_i])/NC_itc_std[:,f_i,t_i]
    
    
    
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

    sub_NC_grandaverage_power_list= mne.grand_average(sub_NC_power_list, interpolate_bads=True, drop_bads=True)
    sub_CP_grandaverage_power_list= mne.grand_average(sub_CP_power_list, interpolate_bads=True, drop_bads=True)
    sub_NC_grandaverage_itc_list= mne.grand_average(sub_NC_itc_list, interpolate_bads=True, drop_bads=True)
    sub_CP_grandaverage_itc_list= mne.grand_average(sub_CP_itc_list, interpolate_bads=True, drop_bads=True)

    grand_z_CP_power_sub=grandaverage_power_square_list.copy()
    grand_z_CP_power_sub.data=np.mean(z_CP_power_sub,axis=0)
    grand_z_CP_itc_sub=grandaverage_itc_square_list.copy()
    grand_z_CP_itc_sub.data=np.mean(z_CP_itc_sub,axis=0)
    
#################grandaverageの全chのplot################    
    mean=np.mean(grandaverage_power_square_list.data)
    std=np.std(grandaverage_power_square_list.data)
    fig=grandaverage_power_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grandaverage_power_square_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(grandaverage_power_circle_list.data)
    std=np.std(grandaverage_power_circle_list.data)
    fig=grandaverage_power_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grandaverage_power_circle_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(sub_grandaverage_power_list.data)
    std=np.std(sub_grandaverage_power_list.data)
    fig=sub_grandaverage_power_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/sub_grandaverage_power_list.pdf',dpi=1000)
    plt.close()        
 
    mean=np.mean(NC_grandaverage_power_square_list.data)
    std=np.std(NC_grandaverage_power_square_list.data)
    fig=NC_grandaverage_power_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_grandaverage_power_square_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(NC_grandaverage_power_circle_list.data)
    std=np.std(NC_grandaverage_power_circle_list.data)
    fig=NC_grandaverage_power_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_grandaverage_power_circle_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(sub_NC_grandaverage_power_list.data)
    std=np.std(sub_NC_grandaverage_power_list.data)
    fig=sub_NC_grandaverage_power_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/sub_NC_grandaverage_power_list.pdf',dpi=1000)
    plt.close()        

    mean=np.mean(CP_grandaverage_power_square_list.data)
    std=np.std(CP_grandaverage_power_square_list.data)
    fig=CP_grandaverage_power_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/CP_grandaverage_power_square_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(CP_grandaverage_power_circle_list.data)
    std=np.std(CP_grandaverage_power_circle_list.data)
    fig=CP_grandaverage_power_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/CP_grandaverage_power_circle_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(sub_CP_grandaverage_power_list.data)
    std=np.std(sub_CP_grandaverage_power_list.data)
    fig=sub_CP_grandaverage_power_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/sub_CP_grandaverage_power_list.pdf',dpi=1000)
    plt.close()      
    
    
    mean=np.mean(grandaverage_itc_square_list.data)
    std=np.std(grandaverage_itc_square_list.data)
    fig=grandaverage_itc_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grandaverage_itc_square_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(grandaverage_itc_circle_list.data)
    std=np.std(grandaverage_itc_circle_list.data)
    fig=grandaverage_itc_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grandaverage_itc_circle_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(sub_grandaverage_itc_list.data)
    std=np.std(sub_grandaverage_itc_list.data)
    fig=sub_grandaverage_itc_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/sub_grandaverage_itc_list.pdf',dpi=1000)
    plt.close()        
       
 
    mean=np.mean(NC_grandaverage_itc_square_list.data)
    std=np.std(NC_grandaverage_itc_square_list.data)
    fig=NC_grandaverage_itc_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_grandaverage_itc_square_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(NC_grandaverage_itc_circle_list.data)
    std=np.std(NC_grandaverage_itc_circle_list.data)
    fig=NC_grandaverage_itc_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_grandaverage_itc_circle_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(sub_NC_grandaverage_itc_list.data)
    std=np.std(sub_NC_grandaverage_itc_list.data)
    fig=sub_NC_grandaverage_itc_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/sub_NC_grandaverage_itc_list.pdf',dpi=1000)
    plt.close()     
    
    mean=np.mean(CP_grandaverage_itc_square_list.data)
    std=np.std(CP_grandaverage_itc_square_list.data)
    fig=CP_grandaverage_itc_square_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/CP_grandaverage_itc_square_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(CP_grandaverage_itc_circle_list.data)
    std=np.std(CP_grandaverage_itc_circle_list.data)
    fig=CP_grandaverage_itc_circle_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/CP_grandaverage_itc_circle_list.pdf',dpi=1000)
    plt.close()    
    mean=np.mean(sub_CP_grandaverage_itc_list.data)
    std=np.std(sub_CP_grandaverage_itc_list.data)
    fig=sub_CP_grandaverage_itc_list.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*2,vmax=mean+std*2,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/sub_CP_grandaverage_itc_list.pdf',dpi=1000)
    plt.close()     

    mean=np.mean(grand_z_CP_power_sub.data)
    std=np.std(grand_z_CP_power_sub.data)
    fig=grand_z_CP_power_sub.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average power',
                                                 vmin=mean-std*3,vmax=mean+std*3,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grand_z_CP_power_sub.pdf',dpi=1000)
    plt.close()   


    mean=np.mean(grand_z_CP_itc_sub.data)
    std=np.std(grand_z_CP_itc_sub.data)
    fig=grand_z_CP_itc_sub.plot_topo(baseline=(-0.1, 0), mode='zscore', title='Average itc',
                                                 vmin=mean-std*3,vmax=mean+std*3,fig_facecolor='w',font_color='k')
    fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grand_z_CP_itc_sub.pdf',dpi=1000)
    plt.close()     
################ROIのデータを取得################ 
    all_ROIlist=[R_Occ_list,L_Occ_list,R_fusiform_list,L_fusiform_list,R_midTemp_list,L_midTemp_list,R_Temptip_list,L_Temptip_list]

    times=power_square_list[0].times
    freqs=power_square_list[0].freqs
    baseline=[-0.1,0]
    
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
    
    sub_power_ROI_list_mag=[]
    sub_power_ROI_list_grad=[]
    sub_power_ROI_list_all=[]
    sub_itc_ROI_list_mag=[]
    sub_itc_ROI_list_grad=[]
    sub_itc_ROI_list_all=[] 
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
        sub_power_list_mag=[]
        sub_power_list_grad=[]
        sub_power_list_all=[]
        sub_itc_list_mag=[]
        sub_itc_list_grad=[]
        sub_itc_list_all=[]    
        for j in range(len(power_square_list)):
            power_square_list_mag.append(baseline_correction(power_square_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data,times,baseline))
            power_square_list_grad.append(baseline_correction(power_square_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data,times,baseline))
            power_circle_list_mag.append(baseline_correction(power_circle_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data,times,baseline))
            power_circle_list_grad.append(baseline_correction(power_circle_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data,times,baseline))
            itc_square_list_mag.append(baseline_correction(itc_square_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data,times,baseline))
            itc_square_list_grad.append(baseline_correction(itc_square_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data,times,baseline))
            itc_circle_list_mag.append(baseline_correction(itc_circle_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data,times,baseline))
            itc_circle_list_grad.append(baseline_correction(itc_circle_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data,times,baseline))
            power_square_list_all.append(baseline_correction(power_square_list[j].copy().pick_channels(all_ROIlist[i]).data,times,baseline))
            power_circle_list_all.append(baseline_correction(power_circle_list[j].copy().pick_channels(all_ROIlist[i]).data,times,baseline))
            itc_square_list_all.append(baseline_correction(itc_square_list[j].copy().pick_channels(all_ROIlist[i]).data,times,baseline))
            itc_circle_list_all.append(baseline_correction(itc_circle_list[j].copy().pick_channels(all_ROIlist[i]).data,times,baseline))
            sub_power_list_mag.append(baseline_correction(sub_power_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data,times,baseline))
            sub_power_list_grad.append(baseline_correction(sub_power_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data,times,baseline))
            sub_power_list_all.append(baseline_correction(sub_power_list[j].copy().pick_channels(all_ROIlist[i]).data,times,baseline))
            sub_itc_list_mag.append(baseline_correction(sub_itc_list[j].copy().pick_types('mag').pick_channels(all_ROIlist[i]).data,times,baseline))
            sub_itc_list_grad.append(baseline_correction(sub_itc_list[j].copy().pick_types('grad').pick_channels(all_ROIlist[i]).data,times,baseline))
            sub_itc_list_all.append(baseline_correction(sub_itc_list[j].copy().pick_channels(all_ROIlist[i]).data,times,baseline))
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
        sub_power_ROI_list_mag.append(np.array(sub_power_list_mag))
        sub_power_ROI_list_grad.append(np.array(sub_power_list_grad))
        sub_power_ROI_list_all.append(np.array(sub_power_list_all))
        sub_itc_ROI_list_mag.append(np.array(sub_itc_list_mag))
        sub_itc_ROI_list_grad.append(np.array(sub_itc_list_grad))
        sub_itc_ROI_list_all.append(np.array(sub_itc_list_all))        
        
        
        
  
    power_z_CP_sub_list_all=[]
    itc_z_CP_sub_list_all=[]
    for i in range(len(all_ROIlist)):
        power_z_CP_sub_list=[]
        itc_z_CP_sub_list=[]
        for s_i in range(z_CP_itc_sub.shape[0]):
            picks = mne.pick_channels(NC_power_circle_list[0].info["ch_names"],all_ROIlist[i])
            power_z_CP_sub_list.append(np.mean(z_CP_power_sub[s_i,picks,:,:],axis=0))
            itc_z_CP_sub_list.append(np.mean(z_CP_itc_sub[s_i,picks,:,:],axis=0))
        power_z_CP_sub_list_all.append(power_z_CP_sub_list)
        itc_z_CP_sub_list_all.append(itc_z_CP_sub_list)
    power_z_CP_sub_list_all=np.array(power_z_CP_sub_list_all)      
    itc_z_CP_sub_list_all=np.array(itc_z_CP_sub_list_all)      
    
    
    
    
    
      
################全chのplot###############         

    
    
    
    
    
    
    
    freqs_range=[4,95]
    freqs_range=[8,25]
    freq_index=(freqs>freqs_range[0])*(freqs<freqs_range[1])

    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
    for i,ax in enumerate(axes.flat):
        ave_data=np.mean(np.array(power_z_CP_sub_list_all[i,:]),axis=0)
        mean=np.mean(np.array(power_z_CP_sub_list_all))
        std=np.std(np.array(power_z_CP_sub_list_all))
        fig2=ax.imshow( ave_data[freq_index,:],
                   extent=[times[0], times[-1], freqs_range[0], freqs_range[-1]],
                   aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title(pick_list[i])
        fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/power_z_CP_sub_list_all.pdf',dpi=1000)
        plt.close()  
        

    fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
    for i,ax in enumerate(axes.flat):
        ave_data=np.mean(np.array(itc_z_CP_sub_list_all[i,:]),axis=0)
        mean=np.mean(itc_z_CP_sub_list_all)
        std=np.std(itc_z_CP_sub_list_all)
        fig2=ax.imshow( ave_data[freq_index,:],
                   extent=[times[0], times[-1], freqs_range[0], freqs_range[-1]],
                   aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title(pick_list[i])
        fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/itc_z_CP_sub_list_all.pdf',dpi=1000)
        plt.close()          
        
        
    power_list=[power_ROI_square_list_mag,power_ROI_circle_list_mag,power_ROI_square_list_grad,power_ROI_circle_list_grad,
                power_ROI_square_list_all,power_ROI_circle_list_all,sub_power_ROI_list_mag,sub_power_ROI_list_grad,sub_power_ROI_list_all]
    power_list_names=['power_ROI_square_list_mag','power_ROI_circle_list_mag','power_ROI_square_list_grad','power_ROI_circle_list_grad',
                      'power_ROI_square_list_all','power_ROI_circle_list_all','sub_power_ROI_list_mag','sub_power_ROI_list_grad','sub_power_ROI_list_all']
    
    for j in range(len(power_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        if j<6:
            mean=np.mean(np.array(power_list[0][0]))
            std=np.std(np.array(power_list[0][0]))
        else:
            mean=np.mean(np.array(power_list[6][0]))
            std=np.std(np.array(power_list[6][0]))
            
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.array(power_list[j][i]),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grandaverage_'+power_list_names[j]+'.pdf',dpi=1000)
        plt.close()  
        
    itc_list=[itc_ROI_square_list_mag,itc_ROI_circle_list_mag,itc_ROI_square_list_grad,itc_ROI_circle_list_grad,
                itc_ROI_square_list_all,itc_ROI_circle_list_all,sub_itc_ROI_list_mag,sub_itc_ROI_list_grad,sub_itc_ROI_list_all]
    itc_list_names=['itc_ROI_square_list_mag','itc_ROI_circle_list_mag','itc_ROI_square_list_grad','itc_ROI_circle_list_grad',
                      'itc_ROI_square_list_all','itc_ROI_circle_list_all','sub_itc_ROI_list_mag','sub_itc_ROI_list_grad','sub_itc_ROI_list_all']
    
    for j in range(len(itc_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        if j<6:
            mean=np.mean(np.array(itc_list[0][0]))
            std=np.std(np.array(itc_list[0][0]))
        else:
            mean=np.mean(np.array(itc_list[6][0]))
            std=np.std(np.array(itc_list[6][0]))
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.array(itc_list[j][i]),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/grandaverage_'+itc_list_names[j]+'.pdf',dpi=1000)
        plt.close()  
        
    for j in range(len(power_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        mean=np.mean(np.array(power_list[0][0][0:-3,:,:]))
        std=np.std(np.array(power_list[0][0][0:-3,:,:]))
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.array(power_list[j][i][0:-3,:,:]),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/CP_grandaverage_'+power_list_names[j]+'.pdf',dpi=1000)
        plt.close()  

    for j in range(len(itc_list)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,12))
        mean=np.mean(np.array(itc_list[0][0][0:-3,:,:]))
        std=np.std(np.array(itc_list[0][0][0:-3,:,:]))
        for i,ax in enumerate(axes.flat):
            ave_data=np.mean(np.array(itc_list[j][i][0:-3,:,:]),axis=0)
            fig2=ax.imshow( ave_data,
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', vmin=mean-2*std, vmax=mean+2*std, cmap='RdBu_r')
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title(pick_list[i])
            fig.colorbar(fig2, ax=ax)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)
        fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/CP_grandaverage_'+itc_list_names[j]+'.pdf',dpi=1000)
        plt.close()  
      
        
        
    
    from scipy import stats
################各周波数帯域の各ROIのmag、gradの同時plot############### 
     
    
    freq_range=[[4,7],[8,13],[14,38],[40,98]]
    freq_name=['theta','alpha','beta','gamma']
    sub_list=['all','NC','CP']
    legend_list=['square mag','circle mag','square grad','circle grad']
    
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for f_i in range(len(freq_range)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
        for i,ax in enumerate(axes.flat):     
            data=np.mean(power_z_CP_sub_list_all[i,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=0)
            
            ave_data=np.mean(data,axis=0)
            ste_data=stats.sem(data,axis=0)
            ax.plot(times,ave_data, color='g',linewidth = 0.5)
            ax.set_ylim([-0.6,1.5])
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ax.set_title(pick_list[i])
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/z_CP_sub_'+freq_name[f_i]+'_power.pdf',dpi=1000)

    for f_i in range(len(freq_range)):
        fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
        for i,ax in enumerate(axes.flat):     
            data=np.mean(itc_z_CP_sub_list_all[i,:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=0)
            ave_data=np.mean(data,axis=0)
            ste_data=stats.sem(data,axis=0)
            ax.plot(times,ave_data, color='g',linewidth = 0.5)
            hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
            ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
            ax.set_title(pick_list[i])
            ax.set_ylim([-0.6,1.5])
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/z_CP_sub_'+freq_name[f_i]+'_itc.pdf',dpi=1000)


################各周波数帯域の各ROIのmag、gradの平均のplot############### 
    sub_list=['all','NC','CP']
    legend_list=['square mag','circle mag','square grad','circle grad']
    
    legend_list=['square all','circle all']
    sub_list=['all','NC','CP']
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for s_i in range(len(sub_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat):     
                data=np.mean(power_ROI_square_list_all[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='g',linewidth = 0.5,label=legend_list[0])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
              
                data=np.mean(power_ROI_circle_list_all[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='r',linewidth = 0.5,label=legend_list[1])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)  
               
                
                ax.set_title(pick_list[i])
                
    #        plt.legend(loc='upper left')
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/all_'+sub_list[s_i]+'_'+freq_name[f_i]+'_power.pdf',dpi=1000)

################各周波数帯域の各ROIのmag、gradの同時plot############### 
    legend_list=['square mag','circle mag','square grad','circle grad']
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for s_i in range(len(sub_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat):     
                data=np.mean(itc_ROI_square_list_mag[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='g',linewidth = 0.5,label=legend_list[0])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
              
                data=np.mean(itc_ROI_circle_list_mag[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='r',linewidth = 0.5,label=legend_list[1])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)  
               
                data=np.mean(itc_ROI_square_list_grad[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='b',linewidth = 0.5,label=legend_list[2])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='b', alpha=0.1)
             
                data=np.mean(itc_ROI_circle_list_grad[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='y',linewidth = 0.5,label=legend_list[3])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='y', alpha=0.1)  
                
                ax.set_title(pick_list[i])
                
    #        plt.legend(loc='upper left')
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/mag_grad_'+sub_list[s_i]+'_'+freq_name[f_i]+'_itc.pdf',dpi=1000)

################各周波数帯域の各ROIのmag、gradの平均のplot############### 
    legend_list=['square all','circle all']
    sub_index=[np.arange(0,20,1),np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    for s_i in range(len(sub_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat):     
                data=np.mean(itc_ROI_square_list_all[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='g',linewidth = 0.5,label=legend_list[0])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='g', alpha=0.1)
               
                data=np.mean(itc_ROI_circle_list_all[i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color='r',linewidth = 0.5,label=legend_list[1])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color='r', alpha=0.1)  
               
                
                ax.set_title(pick_list[i])
                
    #        plt.legend(loc='upper left')
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
#            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/all_'+sub_list[s_i]+'_'+freq_name[f_i]+'_itc.pdf',dpi=1000)

        
################各周波数帯域の各ROIのNCとCPの平均値のplot###############         
    power_list=[power_ROI_square_list_mag,power_ROI_circle_list_mag,power_ROI_square_list_grad,power_ROI_circle_list_grad,
                power_ROI_square_list_all,power_ROI_circle_list_all,sub_power_ROI_list_mag,sub_power_ROI_list_grad,sub_power_ROI_list_all]
    power_list_names=['power_ROI_square_list_mag','power_ROI_circle_list_mag','power_ROI_square_list_grad','power_ROI_circle_list_grad',
                      'power_ROI_square_list_all','power_ROI_circle_list_all','sub_power_ROI_list_mag','sub_power_ROI_list_grad','sub_power_ROI_list_all']
#
#
#    power_list=[power_ROI_square_list_mag,power_ROI_circle_list_mag,power_ROI_square_list_grad,power_ROI_circle_list_grad,power_ROI_square_list_all,power_ROI_circle_list_all]
#    power_list_names=['power_ROI_square_list_mag','power_ROI_circle_list_mag','power_ROI_square_list_grad','power_ROI_circle_list_grad','power_ROI_square_list_all','power_ROI_circle_list_all']

    sub_list=['NC','CP']
    sub_index=[np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    color_list=['g','r']
    legend_list=['square mag','circle mag','square grad','circle grad','square all','circle all','sub mag','sub grad','sub all']
    for d_i in range(len(power_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                for s_i in range(len(sub_list)):
                    data=np.mean(power_list[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                    
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_CP_'+power_list_names[d_i]+'_'+freq_name[f_i]+'_power.pdf',dpi=1000)





    itc_list=[itc_ROI_square_list_mag,itc_ROI_circle_list_mag,itc_ROI_square_list_grad,itc_ROI_circle_list_grad,itc_ROI_square_list_all,itc_ROI_circle_list_all]
    itc_list_names=['itc_ROI_square_list_mag','itc_ROI_circle_list_mag','itc_ROI_square_list_grad','itc_ROI_circle_list_grad','itc_ROI_square_list_all','itc_ROI_circle_list_all']
            
    for d_i in range(len(itc_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                for s_i in range(len(sub_list)):
                    data=np.mean(itc_list[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                    
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_CP_'+itc_list_names[d_i]+'_'+freq_name[f_i]+'_itc.pdf',dpi=1000)
     
        
     
        
################各周波数帯域の各ROIのNCとCPの個別波形のplot###############     
    sub_list=['NC','CP']
    sub_index=[np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    color_list=['g','r']
    
    for d_i in range(len(power_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                s_i=0
                data=np.mean(power_list[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                s_i=1
                data=np.mean(power_list[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                for h_i in range(len(sub_index[1])):
                    ax.plot(times,data[h_i,:], color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_all_CP_'+power_list_names[d_i]+'_'+freq_name[f_i]+'_power.pdf',dpi=1000)
            
            
    for d_i in range(len(itc_list)):
        for f_i in range(len(freq_range)):
            fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
            for i,ax in enumerate(axes.flat): 
                s_i=0
                data=np.mean(itc_list[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                ave_data=np.mean(data,axis=0)
                ste_data=stats.sem(data,axis=0)
                ax.plot(times,ave_data, color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[s_i][0], alpha=0.1)
                s_i=1
                data=np.mean(itc_list[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                
                for h_i in range(len(sub_index[1])):
                    ax.plot(times,data[h_i,:], color=color_list[s_i][0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list[d_i])
                
                ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')       
            plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
            plt.subplots_adjust(wspace=0.4, hspace=0.6)
            fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/NC_all_CP_'+itc_list_names[d_i]+'_'+freq_name[f_i]+'_itc.pdf',dpi=1000)
            
        
################各被験者条件間比較############### 
    sub_list=['NC','CP']
    sub_index=[np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    color_list=['g','r']
    power_list_square=[power_ROI_square_list_mag,power_ROI_square_list_grad,power_ROI_square_list_all]
    power_list_circle=[power_ROI_circle_list_mag,power_ROI_circle_list_grad,power_ROI_circle_list_all]
    power_list_names=['power_ROI_list_mag','power_ROI_list_grad','power_ROI_list_all']

    legend_list1=['square mag','square grad','square all']
    legend_list2=['circle mag','circle grad','circle all']
    sub_index=[np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    s_i=0
    for s_i in range(len(sub_list)):
        for d_i in range(len(power_list_circle)):
            for f_i in range(len(freq_range)):
                fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
                for i,ax in enumerate(axes.flat): 
                    data=np.mean(power_list_square[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                    
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list1[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[0], alpha=0.1)                
                    ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')  
                    data=np.mean(power_list_circle[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                    
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[1],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list2[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[1], alpha=0.1)                
                    ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')  
                plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
                plt.subplots_adjust(wspace=0.4, hspace=0.6)
                fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/'+sub_list[s_i]+'_square_circle_'+power_list_names[d_i]+'_'+freq_name[f_i]+'_power.pdf',dpi=1000)

    
    itc_list_square=[itc_ROI_square_list_mag,itc_ROI_square_list_grad,itc_ROI_square_list_all]
    itc_list_circle=[itc_ROI_circle_list_mag,itc_ROI_circle_list_grad,itc_ROI_circle_list_all]
    itc_list_names=['itc_ROI_list_mag','itc_ROI_list_grad','itc_ROI_list_all']

    legend_list1=['square mag','square grad','square all']
    legend_list2=['circle mag','circle grad','circle all']
    sub_index=[np.arange(0,20,1)[0:-3],np.arange(0,20,1)[-3::]]    
    s_i=0
    for s_i in range(len(sub_list)):
        for d_i in range(len(itc_list_circle)):
            for f_i in range(len(freq_range)):
                fig, axes = plt.subplots(nrows=4, ncols=2,figsize=(8,16))
                for i,ax in enumerate(axes.flat): 
                    data=np.mean(itc_list_square[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                    
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[0],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list1[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[0], alpha=0.1)                
                    ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')  
                    data=np.mean(itc_list_circle[d_i][i][sub_index[s_i],:,:][:,(freqs>=freq_range[f_i][0])*(freqs<=freq_range[f_i][1]),:],axis=1)
                    
                    ave_data=np.mean(data,axis=0)
                    ste_data=stats.sem(data,axis=0)
                    ax.plot(times,ave_data, color=color_list[1],linewidth = 0.5,label=sub_list[s_i]+' '+legend_list2[d_i])
                    hyp_limits0 = (ave_data- ste_data, ave_data + ste_data)
                    ax.fill_between(times,hyp_limits0[0], y2=hyp_limits0[1], color=color_list[1], alpha=0.1)                
                    ax.set_title(pick_list[i], fontsize=12, fontname='Times New Roman')  
                plt.legend(loc='upper right',bbox_to_anchor=(.5, -.15), ncol=3)
                plt.subplots_adjust(wspace=0.4, hspace=0.6)
                fig.savefig(cfg.SET_RESULT_DIR + '/grandaverage/stockwell/'+sub_list[s_i]+'_square_circle_'+itc_list_names[d_i]+'_'+freq_name[f_i]+'_itc.pdf',dpi=1000)

         
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
        
        
        