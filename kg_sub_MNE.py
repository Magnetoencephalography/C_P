# -*- coding: utf-8 -*-
from glob import glob
from os.path import join, relpath

def argwrapper(args):
    return args[0](*args[1:])

def work(cmd,env):
    import subprocess
    return subprocess.call(cmd,  env=env)

def create_job_sequence(total_process,n_jobs):
    import numpy as np
    job_sequence=np.arange(0,(int(total_process/n_jobs)+1)*n_jobs)
    job_sequence[total_process:]=-1
    job_sequence=job_sequence.reshape(int(total_process/n_jobs)+1,n_jobs)
    return job_sequence

def file_serch(path,base_name,search_word):
    
    raw_files = [relpath(x, path) for x in glob(join(path, '*'))]
    temp_raw_files=[]
    for temp_name in raw_files:
        if base_name in temp_name:
            temp_raw_files.append(temp_name)
    flag=True
    for temp_name in temp_raw_files:
        if search_word in temp_name:
            flag=False
    return flag


def edit_python_setting(new_filename,setting,PARAMETER_DIR,set_environment): #python_settingの書き換え
    f=open(PARAMETER_DIR + '/python_setting_' + set_environment + '.py')
    lines = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    f.close()
    f=open(PARAMETER_DIR + '/python_setting_' + set_environment + '.py','w')
    flag=False
    for line in lines:
        if  line[0:len(setting)] == setting:
            f.write(setting + "='" + new_filename + "'\n")
            print( 'defalut ' + setting +  ' name is converted to ' + new_filename)
            flag=True
        else:
            f.write(line)
        print( line)
    if flag==False:
        f.write("global " + setting + "\n")
        f.write(setting + "='" + new_filename + "'\n")
    f.close()
    
def orig_free_surfer_reconall(SUBJECT,n_jobs,cfg,set_environment):
    import os
    from nipype.interfaces.freesurfer import ReconAll
    slice_list=os.listdir(cfg.SET_MAIN_DIR + '/MRI/' + SUBJECT + '/slices')
    if slice_list[0]=='.DS_Store':
        os.remove(cfg.SET_MAIN_DIR + '/MRI/' + SUBJECT + '/slices/.DS_Store')
        MRI_TOP = slice_list[1]
    else:
        MRI_TOP = slice_list[0]

    if os.path.exists(cfg.SET_SUBJECTS_DIR + '/' + SUBJECT):
        print( 'If you want to recon all, please delete the directories ' + cfg.SET_SUBJECTS_DIR + '/' + SUBJECT + ')')
    reconall = ReconAll()
    reconall.inputs.subject_id = SUBJECT
    reconall.inputs.directive = 'all'
    reconall.inputs.subjects_dir = cfg.SET_SUBJECTS_DIR
    reconall.inputs.T1_files = cfg.SET_MAIN_DIR + '/MRI/' + SUBJECT +'/slices/' + MRI_TOP
    reconall.terminal_output='stream'
    reconall.cmdline
    reconall.run()
                 
def freesurfer_process(all_subject,sttime,n_jobs,cfg,set_environment):
    from multiprocessing import Process
    import numpy as np
    import time
    processes=[]
    job_sequence=np.arange(0,(int(len(all_subject)/n_jobs)+1)*n_jobs)
    job_sequence[len(all_subject):]=-1
    job_sequence=job_sequence.reshape(int(len(all_subject)/n_jobs)+1,n_jobs)
    for i,si in enumerate(job_sequence):
        if not i ==job_sequence.shape[0]+1:
            si=np.delete(si,np.where(si==-1))
        processes=[]
        processes = [Process(target=orig_free_surfer_reconall, args=(all_subject[en],n_jobs,cfg)) for en in si]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    print( 'Processing time is ' + str((time.time()-sttime)/60) + '.')

#def mne_watershed_bem(SUBJECT,SET_OVERWRITE,cfg):
#
#    from mne import bem
#    bem.make_watershed_bem(SUBJECT, subjects_dir=cfg.SET_SUBJECTS_DIR, overwrite=SET_OVERWRITE)
#
#    conductivity = (0.3,)  # for single layer
## conductivity = (0.3, 0.006, 0.3)  # for three layers
#    model = mne.make_bem_model(subject=SUBJECT, ico=4,
#                               conductivity=conductivity,
#                               subjects_dir=cfg.SET_SUBJECTS_DIR)
#    bem = mne.make_bem_solution(model)

#def multi_mne_watershed_bem(all_subject,sttime,SET_OVERWRITE,n_jobs,cfg,set_environment):
#    import time
#    from mne import bem
#    for en in range(len(all_subject)):
#        bem.make_watershed_bem(all_subject[en], subjects_dir=cfg.SET_SUBJECTS_DIR, overwrite=SET_OVERWRITE)
#
#
#    print( 'Processing time is' + str((time.time()-sttime)/60) + '.')


def mne_watershed_bem(SET_OVERWRITE,all_subject,sttime,n_jobs,cfg):
    from multiprocessing import Process
    import time
    from mne.bem import make_watershed_bem
    import numpy as np
    job_sequence=create_job_sequence(len(all_subject),n_jobs)
    for i,si in enumerate(job_sequence):
        if not i ==job_sequence.shape[0]+1:
            si=np.delete(si,np.where(si==-1))
        processes=[]
        processes = [Process(target=make_watershed_bem, args=(line[0], cfg.SET_SUBJECTS_DIR, SET_OVERWRITE))  for line in all_subject]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        print( 'Processing time is' + str((time.time()-sttime)/60) + '.')

def mne_setup_mri(SET_OVERWRITE,all_subject,sttime,n_jobs,env):
    import multiprocessing
    import time
    p = multiprocessing.Pool(n_jobs)
    func_args = []
    #    en=0
    #    for line in all_subject:
    #        func_args.append((work,['mne_make_cor_set','--dir', cfg.SET_SUBJECTS_DIR + '/' + all_subject[en]+'/mri/orig'],env))
    #
    #        en+=1
    #    p.map(argwrapper, func_args)
    #    func_args=[]
    
    en=0
    for line in all_subject:
        if SET_OVERWRITE==True:
            func_args.append((work,['mne_setup_mri','--subject', all_subject[en],'--overwrite'],env))
        else:
            func_args.append((work,['mne_setup_mri','--subject', all_subject[en]],env))
        en+=1
    p.map(argwrapper, func_args)
    func_args=[]

    print( 'Processing time is' + str((time.time()-sttime)/60) + '.')

def mne_setup_forward_model(SET_MEG_SPACING,SET_OVERWRITE,all_subject,sttime,n_jobs,SET_OUTPUT_DIR,env):
    import shutil
    import multiprocessing
    import time
    import os
    import mne
    conductivity = (0.3,)
    for line in all_subject:
        line=line[0]
        if os.path.isfile(SET_OUTPUT_DIR + '/' + line + '/bem/watershed/' + line + '_brain_surface'):
            if not os.path.isfile(SET_OUTPUT_DIR + '/' + line + '/bem/brain.surf'):
                shutil.copyfile(SET_OUTPUT_DIR + '/' + line + '/bem/watershed/' + line + '_brain_surface', SET_OUTPUT_DIR + '/' + line + '/bem/brain.surf')
                shutil.copyfile(SET_OUTPUT_DIR + '/' + line + '/bem/watershed/' + line + '_inner_skull_surface', SET_OUTPUT_DIR + '/' + line + '/bem/inner_skull.surf')
                shutil.copyfile(SET_OUTPUT_DIR + '/' + line + '/bem/watershed/' + line + '_outer_skin_surface', SET_OUTPUT_DIR + '/' + line + '/bem/outer_skin.surf')
                shutil.copyfile(SET_OUTPUT_DIR + '/' + line + '/bem/watershed/' + line + '_outer_skull_surface', SET_OUTPUT_DIR + '/' + line + '/bem/outer_skull.surf')
#    p = multiprocessing.Pool(n_jobs)
#    func_args = []
#    en=0
    p = multiprocessing.Pool(n_jobs)
    func_args = []
    en=0
    for line in all_subject:
        if SET_OVERWRITE==True:
            func_args.append((work,['mne_setup_forward_model','--overwrite','--subject',all_subject[en][0],'--homog','--surf','--ico', SET_MEG_SPACING[len(SET_MEG_SPACING)-1]],env))
        else:
            func_args.append((work,['mne_setup_forward_model','--subject',all_subject[en][0],'--homog','--surf','--ico', SET_MEG_SPACING[len(SET_MEG_SPACING)-1]],env))
        en+=1
    p.map(argwrapper, func_args)
    func_args=[]
    
    print('Processing time is' + str((time.time()-sttime)/60) + '.')
    

def make_noise_cov(NOISE_COV_FNAME,CREATE_FROM_RAW,SUBJECT,DATE,BAD_CH,n_jobs,cfg):
    import matplotlib.pyplot as plt
    import os
    import mne
    from mne.io import Raw
    from mne import pick_types,compute_raw_covariance
    from mne.cov import compute_covariance
    from mne.viz import plot_cov
    from mne.preprocessing import maxwell_filter
    plt.ioff()
    raw_fname = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/' + NOISE_COV_FNAME #raw data
   # path = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE
    #if  file_serch(path,NOISE_COV_FNAME.split('_')[0],'-cov.fif'):
   
    
        
    raw = Raw(raw_fname)
    include = []
    raw.info['bads'] += BAD_CH
    if CREATE_FROM_RAW==True:
        picks = pick_types(raw.info, meg=True, eeg=False, stim=False, eog=False,
                        include=include, exclude='bads')
        cov = compute_raw_covariance(raw, picks=picks)
        cov.save(raw_fname[0:len(raw_fname)-4] + '-cov.fif')
        fig_cov, fig_svd = plot_cov(cov, raw.info, colorbar=True, proj=True,show=False)
        
        if not os.path.exists(cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/preprocess/COV'):
            os.makedirs(cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/preprocess/COV')
        fig_cov.savefig(cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/preprocess/COV/noise_cov_fig')
        fig_svd.savefig(cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/preprocess/COV/noise_cov_svd')
    else:
        events = mne.find_events(raw, stim_channel='STI 001')
        event_id, tmin, tmax = 5, -0.2, 0.5
        reject = dict(mag=4e-12, grad=4000e-13)
        epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=('meg'),
                    baseline=None, reject=reject, preload=True)
        
        method_params = dict(diagonal_fixed=dict(mag=0.01, grad=0.01))
        noise_covs = compute_covariance(epochs, tmin=None, tmax=0, method='auto',
                                        return_estimators=True, verbose=True, n_jobs=n_jobs,
                                        projs=None, rank=None,
                                        method_params=method_params)        
        noise_covs[0].save(raw_fname[0:len(raw_fname)-4] + '-cov.fif')

        print( 'Create from epochs is under constraction.')
def multi_make_noise_cov(NOISE_COV_FNAME,CREATE_FROM_RAW,all_subject,sttime,n_jobs,PARAMETER_DIR,cfg,set_environment):
    import numpy as np
    from multiprocessing import Process
    import time
#    processes=[]
#    job_sequence=np.arange(0,(int(len(all_subject)/n_jobs)+1)*n_jobs)
#    job_sequence[len(all_subject):]=-1
#    job_sequence=job_sequence.reshape(int(len(all_subject)/n_jobs)+1,n_jobs)
#    for i,si in enumerate(job_sequence):
#        if not i ==job_sequence.shape[0]+1:
#            si=np.delete(si,np.where(si==-1))
#        processes=[]
#        processes = [Process(target=make_noise_cov, args=([NOISE_COV_FNAME,CREATE_FROM_RAW,all_subject[en][0],all_subject[en][1],all_subject[en][2],cfg])) for en in si]
#        for p in processes:
#            p.start()
#        for p in processes:
#            p.join()
    for en in range(len(all_subject)):
        make_noise_cov(NOISE_COV_FNAME,CREATE_FROM_RAW,all_subject[en][0],all_subject[en][1],all_subject[en][2],n_jobs,cfg)
        
    new_filename=NOISE_COV_FNAME[0:len(NOISE_COV_FNAME)-4]+ '-cov.fif'
    setting='SET_COVNAME'
    edit_python_setting(new_filename,setting,PARAMETER_DIR,set_environment)
    cfg.SET_COVNAME=new_filename
    print( 'Processing time is' + str((time.time()-sttime)/60) + '.')

def make_event_from_raw(SUBJECT,DATE,BAD_CH,cfg,set_environment):
    import mne
    path = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE
    if  file_serch(path,NOISE_COV_FNAME.split('_')[0],'-eve.fif'):
        raw_fname = cfg.SET_MEG_DIR + '/' + SUBJECT + '/' + DATE + '/' + cfg.SET_FILENAME #raw data
        # Reading events
        raw = mne.io.Raw(raw_fname)
        events = mne.find_events(raw, stim_channel='STI 014')
        # Writing events
        mne.write_events(raw_fname[0:len(raw_fname)-4] + '-eve.fif', events)

def multi_make_event_from_raw(all_subject,sttime,n_jobs,PARAMETER_DIR,cfg,set_environment):
    import numpy as np
    from multiprocessing import Process
    import time
    processes=[]
    job_sequence=np.arange(0,(int(len(all_subject)/n_jobs)+1)*n_jobs)
    job_sequence[len(all_subject):]=-1
    job_sequence=job_sequence.reshape(int(len(all_subject)/n_jobs)+1,n_jobs)
    for i,si in enumerate(job_sequence):
        if not i ==job_sequence.shape[0]+1:
            si=np.delete(si,np.where(si==-1))
        processes=[]
        processes = [Process(target=make_event_from_raw, args=([all_subject[en],all_subject[en][1],all_subject[en][2],cfg])) for en in si]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    print( 'Processing time is' + str((time.time()-sttime)/60) + '.')
    new_filename=cfg.SET_FILENAME[0:len(cfg.SET_FILENAME)-4] + '-eve.fif'
    setting='SET_EVENAME'
    edit_python_setting(new_filename,setting,PARAMETER_DIR,set_environment)
    print( 'Processing time is' + str((time.time()-sttime)/60) + '.')
    
def plot_BEM(all_subject,cfg,set_environment):
    import os
    from mne.viz import plot_bem
    for line in all_subject:
        SAVE_DIR=cfg.SET_MEG_DIR + '/' + line[0] + '/' + line[1] + '/preprocess/BEM'
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        plot_bem(subject=line[0], subjects_dir=cfg.SET_SUBJECTS_DIR, orientation='axial', show=False).savefig(SAVE_DIR + '/BEM_axial',dpi=150)
        plot_bem(subject=line[0], subjects_dir=cfg.SET_SUBJECTS_DIR, orientation='sagittal', show=False).savefig(SAVE_DIR + '/BEM_sagittal',dpi=150)
        plot_bem(subject=line[0], subjects_dir=cfg.SET_SUBJECTS_DIR, orientation='coronal', show=False).savefig(SAVE_DIR + '/BEM_coronal',dpi=150)
        print(line)

def multi_setup_source_space(SET_Volume_SPACING, SET_SURFACE, SET_OVERWRITE,all_subject,sttime,n_jobs,cfg,set_environment):
    from mne import setup_source_space
    import time
    for subject in all_subject:
        setup_source_space(subject[0], spacing=SET_Volume_SPACING, surface='white', subjects_dir=cfg.SET_SUBJECTS_DIR, add_dist=True, n_jobs=n_jobs)
    print( 'Processing time is' + str((time.time()-sttime)/60) + '.')

