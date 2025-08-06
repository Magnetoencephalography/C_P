#-*- coding: utf-8 -*-

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
#squareはばらばら、sircleは顔
SET_EVENTNAME=['square','circle']
SET_MEG=True
REJECT = dict(grad=4000e-13,mag=4e-12)

##############################################
from numba.decorators import jit
import numpy as np
import sys
import os  
import mne
import pylab as plt
import itertools
from multiprocessing import Process , Array 
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

pick_list=['L_Occ','R_Occ','L_fusiform','R_fusiform','L_midTemp','R_midTemp','L_Temptip','R_Temptip']
all_ROIlist=[R_Occ_list,L_Occ_list,R_fusiform_list,L_fusiform_list,R_midTemp_list,L_midTemp_list,R_Temptip_list,L_Temptip_list]

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

def create_job_sequence(total_process,n_jobs):
    job_sequence=np.arange(0,(int(total_process/n_jobs)+1)*n_jobs)
    job_sequence[total_process:]=-1
    job_sequence=job_sequence.reshape(int(total_process/n_jobs)+1,n_jobs)
    return job_sequence  

def multi_hirbert(filtered_data,sfreq,n_jobs):
    filtered_data=filtered_data.reshape((filtered_data.shape[0],filtered_data.shape[1]))
    ch_types = ['mag' for i in range(filtered_data.shape[0])]
    ch_names = list(np.array(np.arange(0,filtered_data.shape[0],1),dtype='str'))
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    raw = mne.io.RawArray(filtered_data, info)
    raw.apply_hilbert( envelope=False, n_jobs=n_jobs, n_fft='auto')
    filtered_data=raw.get_data()
    return filtered_data


@jit
def MI_core(phase, amp, position):
    import numpy as np
    nbin=len(position)
    winsize = 2*np.pi/nbin    
    amp_angle=[]
    MeanAmp=np.zeros(nbin)
    StdAmp=np.zeros(nbin)
    allarray=np.zeros([3,nbin])
    for j in range(0,nbin):
        I=  np.where((phase <  position[j]+winsize) & (phase>=  position[j]))[0]
        if len(I)> 0:
            MeanAmp[j]=np.mean(amp[I])
            StdAmp[j]=np.std(amp[I])
            amp_angle.append(amp[I])
            allarray[0,j]=np.mean(amp[I])
            allarray[1,j]=np.std(amp[I])
    MI=(np.abs(nbin)-(-np.sum((MeanAmp/np.sum(MeanAmp))*np.log((MeanAmp/np.sum(MeanAmp)).clip(min=0.0000000001)))))/np.log(nbin)
    allarray[2,0]=MI
    return allarray

def MI_tort(Phase, Amp, position):    
    nbin=len(position) #we are breaking 0-360o in 18 bins, ie, each bin has 20o
    n_sources=Phase.shape[0]
    winsize = 2*np.pi/nbin    
    # now we compute the mean amplitude in each phase:    
    MI=np.zeros(n_sources)
    MeanAmp_array=np.zeros([n_sources,nbin])    
    for s_i in range(n_sources):    
        amp_angle=[]
        MeanAmp=np.zeros(nbin)
        StdAmp=np.zeros(nbin)
        for j in range(0,nbin):
            I=  np.where((Phase[s_i,:] <  position[j]+winsize) & (Phase[s_i,:] >=  position[j]))[0]
            if len(I)> 0:
                MeanAmp[j]=np.mean(Amp[s_i,:][I])
                StdAmp[j]=np.std(Amp[s_i,:][I])
                amp_angle.append(Amp[s_i,:][I])
        MeanAmp_array[s_i,:]=MeanAmp
        MI[s_i]=(np.abs(nbin)-(-np.sum((MeanAmp/np.sum(MeanAmp))*np.log((MeanAmp/np.sum(MeanAmp)).clip(min=0.0000000001)))))/np.log(nbin)
    return MI,MeanAmp_array ,StdAmp
 
    
def MI_orig(MI_array_tort,MeanAmp_tort,StdAmp_tort,Phase, Amp, position,ap_index,s_i):
    MI_array_tort[:,ap_index[0],ap_index[1]],MeanAmp_tort[:,:,ap_index[0],ap_index[1]],StdAmp_tort[:,:,ap_index[0],ap_index[1]]=MI_tort(Phase, Amp, position)
 
def create_permutate_phase(Phase,surrogate_num):
    n_sources=Phase.shape[0]
    n_points=Phase.shape[1]
    permutate_phase_array=np.zeros([n_sources,n_points])
    for s_i in range(n_sources):
        permutate_phase_array[s_i,:]=np.hstack((Phase[s_i,surrogate_num::],Phase[s_i,0:surrogate_num]))
    return permutate_phase_array   

def PAC_Surrogate(PAC_tort,parmutate_MI_tort,orig_MI_tort,phase, envelope, position,surrogate_runs,comb_index):
    n_sources=phase.shape[0]
    n_points=phase.shape[1]
    surrogate_MI_tort=np.zeros([n_sources,surrogate_runs])
    surrogate_num=np.random.permutation(n_points)[0:surrogate_runs]
    for i in range(surrogate_runs):
        permutate_phase=create_permutate_phase(phase,surrogate_num[i]) 
        surrogate_MI_tort[:,i],_,_=MI_tort(permutate_phase,envelope, position)
    mu_sur_tort = np.mean(surrogate_MI_tort,axis=1)
    sd_sur_tort = np.std(surrogate_MI_tort,axis=1)
    PAC_tort[:,comb_index[0],comb_index[1]]=(orig_MI_tort-mu_sur_tort)/sd_sur_tort
    parmutate_MI_tort[:,:,comb_index[0],comb_index[1]]=surrogate_MI_tort       
def PAC_ch(output_dir_name,SUBJECT,DATE,data,sfreq,file_name):
    from mne.filter import filter_data as mne_band_pass_filter
    AmpFreqVector=np.arange(20,100,5)
    Amp_bandwidths=10
    PhaseFreqVector=np.arange(4,20,1)
    Phase_bandwidths=0.5 
    surrogate_runs=200
    nbin = 18
    global counta
    
    if not os.path.exists(cfg.SET_RESULT_DIR + '/' +  SUBJECT+ '/' + output_dir_name  ):
        os.makedirs(cfg.SET_RESULT_DIR + '/' +  SUBJECT+ '/' + output_dir_name   )
    if not os.path.exists(cfg.SET_RESULT_DIR + '/' +  SUBJECT+ '/' + output_dir_name    + '/data'):
        os.makedirs(cfg.SET_RESULT_DIR + '/' +  SUBJECT+ '/' + output_dir_name    + '/data')

                
     #PAC##########################################################################################################################
    n_epochs=data.shape[0]
    n_channels=data.shape[1]
    n_points=data.shape[2]
    data=data.reshape([n_epochs*n_channels,n_points])
#######################create vector###########################################
    position=np.zeros([nbin]) # this variable will get the beginning (not the center) of each phase bin (in rads)
    winsize = 2*np.pi/nbin
    for j in range(0,nbin): 
        position[j] = -np.pi+j*winsize 
#######################caluculate envelope and phase#####################################################
    Envelope_array=np.array(np.zeros([len(AmpFreqVector),n_epochs*n_channels,n_points]),dtype='float32')
    Phase_array  =np.array(np.zeros([len(PhaseFreqVector),n_epochs*n_channels,n_points]),dtype='float32')

    
    for f_i in range(0,len(AmpFreqVector)):
        filtered_data=np.array(mne_band_pass_filter(data, sfreq, AmpFreqVector[f_i]-Amp_bandwidths, 
                                                    AmpFreqVector[f_i]+Amp_bandwidths,l_trans_bandwidth=0.5,
                                                    h_trans_bandwidth=0.5,method='fft',n_jobs=t_n_jobs),dtype='float32')
        hilbert_array=multi_hirbert(filtered_data,sfreq,n_jobs)
        filtered_data=0
        Envelope_array[f_i,:,:]=np.abs(hilbert_array)
        hilbert_array=0
        print('Filter AmpFreqVector ' + str(f_i) + '/' + str(len(AmpFreqVector)))
    for f_i in range(0,len(PhaseFreqVector)):
        filtered_data=np.array(mne_band_pass_filter(data, sfreq, PhaseFreqVector[f_i]-Phase_bandwidths, 
                                                    PhaseFreqVector[f_i]+Phase_bandwidths,
                                                    l_trans_bandwidth=0.5,
                                                    h_trans_bandwidth=0.5,method='fft', n_jobs=t_n_jobs),dtype='float32')
        hilbert_array=multi_hirbert(filtered_data,sfreq,n_jobs)
        filtered_data=0
        Phase_array[f_i,:,:]=np.angle(hilbert_array)
        hilbert_array=0
        print('Filter PhaseFreqVector ' + str(f_i) + '/' + str(len(PhaseFreqVector)))
    filtered_data=[]
    Envelope_array=np.array(Envelope_array,dtype='float32')
    Phase_array=np.array(Phase_array,dtype='float32')

#    f_i=5
#    f_i=6
#    a=np.array(mne_band_pass_filter(data, sfreq, PhaseFreqVector[f_i]-Phase_bandwidths, PhaseFreqVector[f_i]+Phase_bandwidths,filter_length='10s',l_trans_bandwidth=0.5,h_trans_bandwidth=0.5,method='fft',n_jobs=n_jobs),dtype='float32')
#    hilbert_array=multi_hirbert(a,sfreq,n_jobs)
#    Phase_array[f_i,:,:]=np.angle(hilbert_array)
#
#    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(9,3))
#    ax1.plot(a[0,0,0:721],label ='X', color='b', linewidth=0.5,alpha=0.5)
#    ax1.plot(Envelope_array[0,0,0,0:721],label ='X', color='b', linewidth=1)
#    ax2.plot(a[0,0,0:721],label ='X', color='r', linewidth=0.5,alpha=0.5)
#    ax2.plot(Phase_array[0,0,0,0:721]*0.25,label ='X', color='r', linewidth=1)
#    ax1.get_xaxis().set_visible(False)
#    ax1.get_yaxis().set_visible(False)     
#    ax2.get_xaxis().set_visible(False)
#    ax2.get_yaxis().set_visible(False)      
#    plt.subplots_adjust(0.1, 0.08, 0.96, 0.94, 0.2, 0.43)
#    plt.tight_layout()  
#    plt.savefig('/Users/takeiyuichi/Dropbox/sync_folder/On_Work/hilbert.pdf',dpi=300)
#    plt.close()     
#    
#    
 #######################caluculate original MI using tort method#####################################################        
  
#        comb_index=list(itertools.product(range(0,stcs_shape[0]), range(stcs_shape[0]+stcs_shape[1],stcs_shape[0]+stcs_shape[1]+stcs_shape[2])))
#        comb_index.append(list(itertools.product(range(stcs_shape[0],stcs_shape[0]+stcs_shape[1]), range(stcs_shape[0]+stcs_shape[1],stcs_shape[0]+stcs_shape[1]+stcs_shape[2]))))
#        n_comb=len(comb_index)
    n_comb=data.shape[0]
   
    MI_array_tort=Array('d',n_comb*len(PhaseFreqVector)*len(AmpFreqVector))
    MI_array_tort = np.frombuffer(MI_array_tort.get_obj())
    MI_array_tort=MI_array_tort.reshape((n_comb,len(PhaseFreqVector),len(AmpFreqVector)))    
    MeanAmp_tort=Array('d',n_comb*nbin*len(PhaseFreqVector)*len(AmpFreqVector))
    MeanAmp_tort = np.frombuffer(MeanAmp_tort.get_obj())
    MeanAmp_tort=MeanAmp_tort.reshape((n_comb,nbin,len(PhaseFreqVector),len(AmpFreqVector)))          
    StdAmp_tort=Array('d',n_comb*nbin*len(PhaseFreqVector)*len(AmpFreqVector))
    StdAmp_tort = np.frombuffer(StdAmp_tort.get_obj())
    StdAmp_tort=StdAmp_tort.reshape((n_comb,nbin,len(PhaseFreqVector),len(AmpFreqVector)))   
    ap_index=list(itertools.product(range(0,len(PhaseFreqVector)), range(0,len(AmpFreqVector))))
    job_sequence=create_job_sequence(len(ap_index),n_jobs)        

    for i,si in enumerate(job_sequence):
        if not i ==job_sequence.shape[0]+1:
            si=np.delete(si,np.where(si==-1))
        processes=[]
        processes = [Process(target=MI_orig, args=(MI_array_tort,MeanAmp_tort,StdAmp_tort,Phase_array[ap_index[process_index][0],:,:], Envelope_array[ap_index[process_index][1],:,:],position, ap_index[process_index],process_index)) for process_index in si]
        for p in processes:
            p.start()
        for p in processes:    
            p.join() 
        print('Caluculate original MI ' + str(i+1) + '/' + str(len(job_sequence))) 
 
    file_name=cfg.SET_RESULT_DIR + '/' +  SUBJECT+ '/' + output_dir_name    + '/data/MI_tort_'+file_name
    np.save(file_name,MI_array_tort)  
    file_name=cfg.SET_RESULT_DIR + '/' +  SUBJECT  + '/' + output_dir_name  + '/data/MeanAmp_tort_'+file_name
    np.save(file_name,MeanAmp_tort) 
    file_name=cfg.SET_RESULT_DIR + '/' +  SUBJECT  + '/' + output_dir_name  + '/data/StdAmp_tort_'+file_name
    np.save(file_name,StdAmp_tort) 



#    for i in range(MI_array_tort.shape[0]):
#        save_filename=output_dir + '/fig/MI_org_tort_'+label_name[i]
#        MI_tort=MI_array_tort[i,:,:]
#        level_min,level_max=np.min(MI_tort),np.max(MI_tort)
#        savefig_PAC(np.transpose(MI_tort),PhaseFreqVector,AmpFreqVector,save_filename,level_min,level_max)
#        save_filename=output_dir + '/fig/MI_org_canolty'
#        MI_canolty=MI_array_canolty[i,:,:]
#        level_min,level_max=np.min(MI_canolty),np.max(MI_canolty)
#        savefig_PAC(np.transpose(MI_canolty),PhaseFreqVector,AmpFreqVector,save_filename,level_min,level_max)

#######################caluculate PAC using tort method#####################################################
    PAC_array_tort=Array('d',n_comb*len(PhaseFreqVector)*len(AmpFreqVector))
    PAC_array_tort = np.frombuffer(PAC_array_tort.get_obj())
    PAC_array_tort=PAC_array_tort.reshape((n_comb,len(PhaseFreqVector),len(AmpFreqVector)))    
    parmutate_MI_array_tort=Array('d',n_comb*surrogate_runs*len(PhaseFreqVector)*len(AmpFreqVector))
    parmutate_MI_array_tort = np.frombuffer(parmutate_MI_array_tort.get_obj())
    parmutate_MI_array_tort=parmutate_MI_array_tort.reshape((n_comb,surrogate_runs,len(PhaseFreqVector),len(AmpFreqVector)))    
  
    for i,si in enumerate(job_sequence):
        if not i ==job_sequence.shape[0]+1:
            si=np.delete(si,np.where(si==-1))
        processes=[]
        processes = [Process(target=PAC_Surrogate, 
                             args=(PAC_array_tort,parmutate_MI_array_tort,MI_array_tort[:,ap_index[process_index][0],ap_index[process_index][1]],Phase_array[ap_index[process_index][0],:,:], Envelope_array[ap_index[process_index][1],:,:],position,surrogate_runs, ap_index[process_index])) for process_index in si]
        for p in processes:
            p.start()
        for p in processes:
            p.join() 
        print('caluculate sarrogate PAC ' + str(i+1) + '/' + str(len(job_sequence)))

    file_name=cfg.SET_RESULT_DIR + '/' +  SUBJECT  + '/' + output_dir_name  + '/data/PAC_array_tort_'+file_name
    np.save(file_name,PAC_array_tort)  

    file_name=cfg.SET_RESULT_DIR + '/' +  SUBJECT  + '/' + output_dir_name  + '/data/parmutate_MI_array_tort_'+file_name
    np.save(file_name,parmutate_MI_array_tort)  


    
#    for i in range(MI_array_tort.shape[0]):
#        PAC_tort=PAC_array_tort[i,:,:]
#        save_filename=output_dir + '/fig/PAC_tort_'+label_name[i]
#        level_min,level_max=np.min(PAC_tort),np.max(PAC_tort)
#        savefig_PAC(np.transpose(PAC_tort),PhaseFreqVector,AmpFreqVector,save_filename,level_min,level_max)
#        PAC_canolty=PAC_array_canolty[i,:,:]
#        save_filename=output_dir + '/fig/PAC_canolty_'+label_name[i]
#        level_min,level_max=np.min(PAC_canolty),np.max(PAC_canolty)
#        savefig_PAC(np.transpose(PAC_canolty),PhaseFreqVector,AmpFreqVector,save_filename,level_min,level_max)

        
def main():
    output_dir_name='PAC'
    for line in open(cfg.SET_PARAMETER, 'r'):
        itemList = line[:-1].split('@')
        SUBJECT=itemList[0]
        DATE=itemList[1]
        if not os.path.exists(cfg.SET_RESULT_DIR + '/' + SUBJECT):
            os.makedirs(cfg.SET_RESULT_DIR + '/' + SUBJECT)
        if not os.path.exists(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/'+output_dir_name):
            os.makedirs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/'+output_dir_name)
        
        raw_fname = cfg.SET_MAIN_DIR  + '/MEG' + '/' + SUBJECT + '/' + DATE + '/'+cfg.SET_FILENAME #raw data
        raw = mne.io.Raw(raw_fname, preload=True)
        picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=False, stim=False)
        events=mne.find_events(raw,stim_channel='STI 001')
        for e_i in range(len(SET_EVENTID)):          
            epochs = mne.Epochs(raw, events, SET_EVENTID[e_i], -0.4, 0.8, picks=picks,baseline=(-0.1, 0),reject=REJECT, preload=True)
            data=[]
            for r_i in range(len(pick_list)):
                data.append(epochs.copy().pick_channels(all_ROIlist[r_i]).get_data())            
            sfreq=epochs.info['sfreq']
            for r_i in range(len(pick_list)):
                PAC_ch(output_dir_name,SUBJECT,DATE,data[r_i],sfreq,pick_list[r_i])
                
                    
if __name__ == '__main__':
    main()
    