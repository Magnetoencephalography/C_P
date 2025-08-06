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
SET_EVENTNAME=['square','circle']
SET_MEG=True
REJECT = dict(grad=4000e-13,mag=4e-12)

##############################################

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

      
def main():
    for line in open(cfg.SET_PARAMETER, 'r'):
        itemList = line[:-1].split('@')
        SUBJECT=itemList[0]
        DATE=itemList[1]
        if not os.path.exists(cfg.SET_RESULT_DIR + '/' + SUBJECT):
            os.makedirs(cfg.SET_RESULT_DIR + '/' + SUBJECT)
        if not os.path.exists(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked'):
            os.makedirs(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked')
        
        raw_fname = cfg.SET_MAIN_DIR  + '/MEG' + '/' + SUBJECT + '/' + DATE + '/'+cfg.SET_FILENAME #raw data
        raw = mne.io.Raw(raw_fname, preload=True)
        picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=False, stim=False)
        raw.filter(2,28,n_jobs=n_jobs)
        events=mne.find_events(raw,stim_channel='STI 001')
        
        evokeds=[]
        for e_i in range(len(SET_EVENTID)):          
            epochs = mne.Epochs(raw, events, SET_EVENTID[e_i], -0.1, 0.5, picks=picks,baseline=(-0.1, 0),reject=REJECT, preload=True)
            evoked=epochs.average()
            epochs.save(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/'+SET_EVENTNAME[e_i]+'-epo.fif', overwrite=True)
            evoked.save(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/'+SET_EVENTNAME[e_i]+'-ave.fif')
            evokeds.append(evoked)
            pick=['grad','mag']
            for i in range(2):
                fig=evoked.plot_joint(picks='mag')
                fig.savefig(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/plot_joint_'+ SET_EVENTNAME[e_i] +'_'+pick[i]+'.png')
                plt.close()
            
            fig=evoked.plot_topomap(times=[0., 0.50, 0.1, 0.15, 0.2,0.25,0.3], ch_type='mag')
            fig.savefig(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/plot_topomap_'+ SET_EVENTNAME[e_i] +'.png')
            plt.close()

            fig=evoked.pick_types('mag').plot_topo(color='r', legend=False)
            fig.savefig(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/plot_topo_'+ SET_EVENTNAME[e_i] +'.png')
            plt.close()
            
        fig=mne.viz.plot_compare_evokeds(dict(square=evokeds[0], circle=evokeds[1]),
                         legend='upper left', show_sensors='upper right')
        fig[0].savefig(cfg.SET_RESULT_DIR + '/' + SUBJECT+'/evoked/plot_compare_evokeds.png')
        plt.close()    
                
if __name__ == '__main__':
    main()
    