#-*- coding: utf-8 -*-

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
SET_EVENTNAME=['square','circle']
SET_MEG=True
REJECT = dict(grad=4000e-13,mag=4e-12)

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

occ_ch_list=[ 'MEG 2113',
 'MEG 2112',
 'MEG 2111','MEG 2122',
 'MEG 2123',
 'MEG 2121','MEG 2332',
 'MEG 2333',
 'MEG 2331','MEG 2343',
 'MEG 2342',
 'MEG 2341','MEG 2512',
 'MEG 2513',
 'MEG 2511']

temp_ch_list=[ 'MEG 1522',
 'MEG 1523',
 'MEG 1521', 'MEG 1612',
 'MEG 1611',
 'MEG 1622',
 'MEG 1623',
 'MEG 1621',
 'MEG 1632',
 'MEG 1633',
 'MEG 1631', 'MEG 1643',
 'MEG 1642',
 'MEG 1641']

def main():
    for line in open(cfg.SET_PARAMETER, 'r'):
        itemList = line[:-1].split('@')
        SUBJECT=itemList[0]
        DATE=itemList[1]
        if not os.path.exists(cfg.SET_RESULT_DIR + '/' + SUBJECT):
            os.makedirs(cfg.SET_RESULT_DIR + '/' + SUBJECT)
        if not os.path.exists(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell'):
            os.makedirs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell')
                
        
        
        raw_fname = cfg.SET_MAIN_DIR  + '/MEG' + '/' + SUBJECT + '/' + DATE + '/'+cfg.SET_FILENAME #raw data
        raw = mne.io.Raw(raw_fname, preload=True)
        picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=False, stim=False)
        events=mne.find_events(raw,stim_channel='STI 001')
        
        for e_i in range(len(SET_EVENTID)):          
            epochs = mne.Epochs(raw, events, SET_EVENTID[e_i], -0.4, 0.8, picks=picks,baseline=(-0.1, 0),reject=REJECT, preload=True)
            frequencies = np.arange(4, 95, 2)
            power,itc = mne.time_frequency.tfr_stockwell(epochs, fmin=4, fmax=95, return_itc=True, n_jobs=n_jobs,width=0.5)
            
            power.apply_baseline((-0.4, 0),mode='zscore')
            itc.apply_baseline((-0.4, 0),mode='zscore')
            
            power.save(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/'+SET_EVENTNAME[e_i]+'_power', overwrite=True)
            itc.save(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/'+SET_EVENTNAME[e_i]+'_itc', overwrite=True)
            
            fig=power.plot_topo(baseline=(-0.4, 0), mode='zscore', title='Average power',fig_facecolor='w', font_color='k', border='k')
            fig.savefig(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/power_plot_topo'+ SET_EVENTNAME[e_i] +'.png',dpi=300)
            plt.close()            

            fig=itc.plot_topo(baseline=(-0.4, 0), mode='zscore', title='Average itc',fig_facecolor='w', font_color='k', border='k')
            fig.savefig(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/itc_plot_topo'+ SET_EVENTNAME[e_i] +'.png',dpi=300)
            plt.close()    

            occ_power=power.copy().pick_channels(occ_ch_list)
            temp_power=power.copy().pick_channels(temp_ch_list)
            occ_itc=itc.copy().pick_channels(occ_ch_list)
            temp_itc=itc.copy().pick_channels(temp_ch_list)
            
            times=occ_power.times
            freqs=occ_power.freqs
            
            plt.subplots_adjust(0.1, 0.08, 0.96, 0.94, 0.2, 0.43)
            plt.subplot(2, 2, 1)
            plt.imshow(np.mean(occ_power.data,axis=0),
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', cmap='RdBu_r')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title('occ_power')
            plt.colorbar()
    
            plt.subplot(2, 2, 2)
            plt.imshow(np.mean(temp_power.data,axis=0),
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', cmap='RdBu_r')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title('temp_power')
            plt.colorbar()

            plt.subplot(2, 2, 3)
            plt.imshow(np.mean(occ_itc.data,axis=0),
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', cmap='RdBu_r')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title('occ_itc')
            plt.colorbar()

            plt.subplot(2, 2, 4)
            plt.imshow(np.mean(temp_itc.data,axis=0),
                       extent=[times[0], times[-1], freqs[0], freqs[-1]],
                       aspect='auto', origin='lower', cmap='RdBu_r')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title('temp_itc')
            plt.colorbar()
            plt.savefig(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/stockwell/power_itc_'+ SET_EVENTNAME[e_i] +'.png',dpi=300)
            plt.close()    




        
                    
if __name__ == '__main__':
    main()
    