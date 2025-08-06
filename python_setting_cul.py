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
SET_MAIN_DIR = '/Volumes/Siena/CP2'
SET_MEG_DIR =SET_MAIN_DIR+'/MEG'
SET_LARGERESULT_DIR=SET_MAIN_DIR+'/results'
SET_RESULT_DIR='/Volumes/Siena/CP2/results'
SET_SUBJECTS_DIR=SET_MAIN_DIR + '/subjects'
SET_PARAMETER='/Volumes/Siena/CP2/parameter/subject_setting.txt'
SET_SCRIPT_PATH='/Volumes/Siena/CP2/source'
SET_FILENAME='SAF_seq1_square_raw.fif' #Raw data filename
######################################################
global SET_COVNAME
SET_COVNAME='room_notch_otp_raw_tsss-cov.fif'
global SET_EVENAME
SET_EVENAME='SAF_seq2_circle_raw-eve.fif'
global SET_FWDNAME
SET_FWDNAME='SAF_seq2_circle_raw-fwd.fif'
global SET_INVNAME
SET_INVNAME='SAF_seq2_circle_raw-inv.fif'
global SET_EVENTID
SET_EVENTID='2,3,4'
global SET_EVENTNAME
SET_EVENTNAME='fear,neutral,house'
global REJECT
REJECT='grad:4e-10,mag:4e-12'

