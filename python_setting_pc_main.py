#-*- coding: utf-8 -*-

global SET_MAIN_DIR
global SET_MEG_DIR
global SET_SUBJECTS_DIR
global SET_PARAMETER
global SET_SCRIPT_PATH
global SET_FILENAME
global SET_PARAMETER
global SET_REJECT_GRAD
global SET_REJECT_MAG
global SET_COVNAME
global SET_EVENAME

SET_MAIN_DIR = '/Volumes/Siena/CP2'
SET_MEG_DIR=SET_MAIN_DIR+ '/MEG'
SET_RESULT_DIR='/Volumes/Siena/CP2/results'
SET_LARGERESULT_DIR=SET_RESULT_DIR
SET_SUBJECTS_DIR=SET_MAIN_DIR + '/subjects'
SET_PARAMETER= '/Volumes/Siena/CP2/parameter/subject_setting.txt'
SET_SCRIPT_PATH='/Volumes/Siena/CP2/source'
SET_FILENAME='SAF_seq1_square_raw.fif' #Raw data filename
SET_COVNAME='room_notch_otp_raw_tsss-cov.fif'
SET_EVENAME='rest1_notch_otp_ica_raw_tsss-eve.fif'
######################################################
global SET_FWDNAME
SET_FWDNAME='rest1_notch_otp_ica_raw_tsss-fwd.fif'
global SET_INVNAME
SET_INVNAME='rest1_notch_otp_ica_raw_tsss-inv.fif'
global SET_EVENTID
SET_EVENTID='5,6,7'
global SET_EVENTNAME
SET_EVENTNAME='0_back,1_back,2_back'
global REJECT
REJECT='grad:4e-10,mag:4e-12'
global SET_MEG
SET_MEG='True'
