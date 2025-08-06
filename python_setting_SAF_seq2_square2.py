#-*- coding: utf-8 -*-

##################global setting##################
global SET_MAIN_DIR
global SET_MEG_DIR
global SET_SUBJECTS_DIR
global SET_PARAMETER
global SET_SCRIPT_PATH
global SET_FILENAME
global SET_PARAMETER
global SET_REJECT_GRAD
global SET_REJECT_MAG
SET_MAIN_DIR = '/Volumes/Siena/CP'
SET_MEG_DIR =SET_MAIN_DIR+'/MEG'
SET_RESULT_DIR='/Volumes/Siena/CP/results'
SET_SUBJECTS_DIR=SET_MAIN_DIR + '/subjects'
SET_PARAMETER='/Volumes/Siena/CP/parameter/subject_setting.txt'
SET_LARGERESULT_DIR='/Volumes/Siena/CP/results'
SET_SCRIPT_PATH='/Volumes/Siena/CP/source'
SET_FILENAME='SAF_seq2_square2_notch_otp_ica_raw_tsss.fif' #Raw data filename
######################################################
global SET_COVNAME
SET_COVNAME='room_notch_otp_raw_tsss-cov.fif'
global SET_EVENAME
SET_EVENAME='SAF_seq2_circle_raw_ica_tsss-eve.fif'
global SET_FWDNAME
SET_FWDNAME='SAF_seq2_circle_raw-fwd.fif'
global SET_INVNAME
SET_INVNAME='SAF_seq2_circle_raw-inv.fif'
global SET_EVENTID
SET_EVENTID='2,3,4'
global SET_EVENTNAME
SET_EVENTNAME='fear,neutral,house'
global REJECT
REJECT='grad:1e-10,mag:4e-12'
