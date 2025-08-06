# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 09:50:15 2015

@author: takeiyuichi
"""

# -*- coding: utf-8 -*-
#mne-pythonでの解析環境を構築するためのスクリプト
#次のprocessはkg_preprocessing_141009.py

#必要なのは、MEGのraw data, MRIスライスデータもしくはfreesurfer済みデータ、
#covarianceをルームデータから計算する場合はroomデータ、被験者の一覧を記述したsubject_setting.txtファイル

#subject_setting.txtは自分で作成する
#形式は以下の通り
#被験者名¥日付¥bad channnel(カンマ区切り)
#例 
#NB_subject_1@120401@MEG 0432,MEG 0921
#NB_subject_2@120402@MEG 0432

#################################設定#############################################
SET_MAIN_DIR = '/Users/takeiyuichi/Dropbox/canonical_correlation_block' #この中に各種ディレクトリが作成される。名前は任意でOK。アルファベットのみ。

#以下は元データの場所の指定。
MEG_DATA_DIR = '/Volumes/S_128GQX/MEG_t' #MEGデータの入っているディレクトリの指定.このディレクトリ以下に/被験者ごとに入れておく
RAW_DATA_NAME='transient_raw.fif' #raw dataファイルの指定
ROOM_DATA='room_raw.fif'
#freesurfer済みの場合は、freesurferデータの入っているディレクトリを指定。
#そうでない場合は、MRIスライスの入っているディレクトリを指定。
FREESURFER_DIR= '/Users/takeiyuichi/Dropbox/transient_test' #このディレクトリ以下に/被験者名/freesurfer data(e.g. bem, label,mri,・・・)という形で入れておく。freesurferをしていない場合は、''とする
#自分で記載して作成
#subject_setting_file='/Volumes/FREECOM/MNE/subject_setting.txt'
defaut_BAD_channel=''
#被験者名@日付@bad channenlとする。
#例
#NB_subject_1@120401@MEG 0432,MEG 0921
#NB_subject_2@120402@MEG 0432
##################################################################################

import shutil
import os
import glob
def process1():
    if not os.path.exists(SET_MAIN_DIR):
        os.mkdir(SET_MAIN_DIR)
    else:
        print SET_MAIN_DIR + ' alredy exist!'
        import sys
        sys.exit()
        
    if not os.path.exists(SET_MAIN_DIR + '/subjects'):
        os.mkdir(SET_MAIN_DIR + '/subjects')
    
    if not os.path.exists(SET_MAIN_DIR + '/source'):
        os.mkdir(SET_MAIN_DIR + '/source')
    
    if not os.path.exists(SET_MAIN_DIR + '/MEG'):
        os.mkdir(SET_MAIN_DIR + '/MEG')
    
    if not os.path.exists(SET_MAIN_DIR + '/results'):
        os.mkdir(SET_MAIN_DIR + '/results')
    
    if not os.path.exists(SET_MAIN_DIR + '/parameter'):
        os.mkdir(SET_MAIN_DIR + '/parameter')
    if not os.path.exists(SET_MAIN_DIR + '/parameter/python_setting_main.py'):
        f=open(SET_MAIN_DIR + '/parameter/python_setting_main.py','w')
        f.write("#-*- coding: utf-8 -*-\n")
        f.write("\n")
        f.write("##################global setting##################\n")
        f.write("global SET_MAIN_DIR\n")
        f.write("global SET_MEG_DIR\n")
        f.write("global SET_SUBJECTS_DIR\n")
        f.write("global SET_PARAMETER\n")
        f.write("global SET_SCRIPT_PATH\n")
        f.write("global SET_FILENAME\n")
        f.write("global SET_PARAMETER\n")
        f.write("global SET_REJECT_GRAD\n")
        f.write("global SET_REJECT_MAG\n")
        f.write("SET_MAIN_DIR = '" + SET_MAIN_DIR + "'\n")
        f.write("SET_MEG_DIR=SET_MAIN_DIR + '/MEG'\n")
        f.write("SET_RESULT_DIR=SET_MAIN_DIR + '/results'\n")
        f.write("SET_SUBJECTS_DIR=SET_MAIN_DIR + '/subjects'\n")
        f.write("SET_PARAMETER=SET_MAIN_DIR + '/parameter/subject_setting.txt'\n")
        f.write("SET_SCRIPT_PATH=SET_MAIN_DIR + '/source'\n")
        f.write("SET_FILENAME='" + RAW_DATA_NAME + "' #Raw data filename\n")
        f.write("######################################################\n")
        f.close()

    all_subject=[r.split('/')[-1] for r in glob.glob(MEG_DATA_DIR + '/*')]
    date_list=[]
    filtered_subjects_list=[]
    for subject in all_subject:
        date=[r.split('/')[-1] for r in glob.glob(MEG_DATA_DIR + '/' + subject + '/*')]
        if len(date)<2:
            if not subject[-1]=='-':
                date_list.append(date[0])
                filtered_subjects_list.append(subject)
        else:
            print subject + ' has more than two dates folder !!'
    f = open(SET_MAIN_DIR + '/parameter/subject_setting.txt', 'w')
    for i in range(len(filtered_subjects_list)):
        f.write(filtered_subjects_list[i] + '@' + date_list[i] + '@' + defaut_BAD_channel + '\n')
    f.close()

def process2():
    for line in open(SET_MAIN_DIR + '/parameter/subject_setting.txt', 'r'):
        itemList = line[:-1].split('@')
        SUBJECT=itemList[0]
        DATE=itemList[1]
        BAD_CHANNEL=itemList[2]
        if not os.path.exists(SET_MAIN_DIR + '/MEG/' + SUBJECT):
            os.mkdir(SET_MAIN_DIR + '/MEG/' + SUBJECT)
        if not os.path.exists(SET_MAIN_DIR + '/MEG/' + SUBJECT + '/' + DATE):
            os.mkdir(SET_MAIN_DIR + '/MEG/' + SUBJECT + '/' + DATE)
        if not os.path.exists(SET_MAIN_DIR + '/MEG/' + SUBJECT + '/' + RAW_DATA_NAME):
            
            if  os.path.exists(MEG_DATA_DIR + '/' + SUBJECT + '/' + RAW_DATA_NAME):                
                shutil.copy(MEG_DATA_DIR + '/' + SUBJECT + '/' + RAW_DATA_NAME, SET_MAIN_DIR + '/MEG/' + SUBJECT + '/' + DATE + '/' + RAW_DATA_NAME)
            elif  os.path.exists(MEG_DATA_DIR + '/' + SUBJECT + '/' + DATE + '/' + RAW_DATA_NAME):                
                shutil.copy(MEG_DATA_DIR + '/' + SUBJECT + '/' + DATE + '/' + RAW_DATA_NAME, SET_MAIN_DIR + '/MEG/' + SUBJECT + '/' + DATE + '/' + RAW_DATA_NAME)
            else:
                print 'I cannot find raw data!'  
                
            if not ROOM_DATA == '':
                if  os.path.exists(MEG_DATA_DIR + '/' + SUBJECT + '/' + ROOM_DATA):                
                    shutil.copy(MEG_DATA_DIR + '/' + SUBJECT + '/' + ROOM_DATA, SET_MAIN_DIR + '/MEG/' + SUBJECT + '/' + DATE + '/' + ROOM_DATA)
                if  os.path.exists(MEG_DATA_DIR + '/' + SUBJECT + '/' + DATE + '/' + ROOM_DATA):                
                    shutil.copy(MEG_DATA_DIR + '/' + SUBJECT + '/' + DATE + '/' + ROOM_DATA, SET_MAIN_DIR + '/MEG/' + SUBJECT + '/' + DATE + '/' + ROOM_DATA)
                else:
                    print 'I cannot find room data!' 
                   
        if not FREESURFER_DIR=='':
            if not os.path.exists(SET_MAIN_DIR + '/subjects/' + SUBJECT):
                shutil.copytree(FREESURFER_DIR + '/' + SUBJECT, SET_MAIN_DIR + '/subjects/' + SUBJECT)
        else:
            if not os.path.exists(SET_MAIN_DIR + '/MRI/' + SUBJECT):
                shutil.copytree(MRI_SLICE_DIR + '/' + SUBJECT, SET_MAIN_DIR + '/MRI/' + SUBJECT)


def main ():
    process1()
    process2()
    print 'Preparation complete'
    print 'Next step is kg_preprocessing.py'

if __name__ == "__main__":
    main()
    
       
