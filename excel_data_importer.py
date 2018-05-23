# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:03:11 2018

@author: hartz
"""
import pyexcel
import pyexcel.ext.xlsx
import numpy as  np
import os

#%% Dienstag
"""convert xls to xlsx and write txt files"""
#set file path, and name
path = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\"
file_name = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data\\22-5-18_143-1_rauschen_0V_unbel-bel_retake.xls"
folder = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\143-1(Ar+H20)\\TLM 2"
date="18-5-18"
structure="143-1"
#%% structure
class experiment():
    def __init__(self, multiplicator, pads, contact_type="TLM", structure="S1", file_name=[],  comment=[], folder =[]):
        self.file_name= file_name
        self.contact_type = contact_type
        self.structure = structure
        self.multiplicator = multiplicator          #30 for TLM, 1 otherwise
        self.pads= pads             #contact pads
        self.comment =comment
        self.folder = folder
        
area_pads=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
TLM = experiment(30, [], structure="S1", file_name=file_name, folder = folder)
Areas = experiment(1, area_pads, contact_type="Areas", file_name=file_name)
#%% 
"""read xls, save sheet to txt-file"""
def export_sheet_to_txt(xls_name, sheet_index, save_name):  
    sheet_array = pyexcel.get_array(file_name = xls_name, sheet_index=sheet_index)
    #header
    rows = sheet_array[0][0]+"\t"+ sheet_array[0][1]
    #export & save, bug-fix with header to circumvent problems with different 
    #data formats
    np.savetxt(save_name,sheet_array[1:],fmt='%.4e',header=rows,comments="",delimiter="\t")
    
 
def txt_export(experiment): 
    xls_name=experiment.file_name           #structure: TLM, Areas, Stripes, ...
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets=book.number_of_sheets()
    structure_type= experiment.contact_type
    
    for sheet_index in range(number_of_sheets):
        if 0 < sheet_index < 3:
            continue
        else:
            print("handle sheet %d" %sheet_index)
            if sheet_index ==0:
                write_param = sheet_index+1
            else:
                write_param = sheet_index-1
                    
            if structure_type =="TLM":
                    write_param *= experiment.multiplicator
                    save_name= "%s_%s_TLM_%d_um.txt" %(date, experiment.structure, write_param)
            elif structure_type =="Areas":
                    write_param = experiment.pads[write_param-1];
                    save_name= "%s_%s_Areas_%f_Areas_%s.txt" % (date, experiment.structure, write_param)
                    
            export_sheet_to_txt(xls_name, sheet_index, save_name)


def light_dark_txt_export(experiment, light):   #bool True:light 1, False: dark
    xls_name=experiment.file_name           #structure: TLM, Areas, Stripes, ...
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets=book.number_of_sheets()
    structure_type= experiment.contact_type
    for sheet_index in range(number_of_sheets):
        if 0 < sheet_index < 3:
            continue
        else:
            if sheet_index == 0 and light:
                print("handle sheet %d" %sheet_index)
                write_param = sheet_index+1
            else:
                write_param = sheet_index-1
                    
            if structure_type =="TLM":
                    write_param *= experiment.multiplicator
                    save_name= "%s_%s_TLM_%d_um.txt" %(date, experiment.structure, write_param)
            elif structure_type =="Areas":
                    write_param = experiment.pads[write_param-1];
                    save_name= "%s_%s_Areas_%f_Areas_%s.txt" % (date, experiment.structure, write_param)
            
            save_name= "%s\\%s" %(folder, save_name)
            export_sheet_to_txt(xls_name, sheet_index, save_name)
            
            
#%%
def light_dark_single_txt_files_export(experiment, summary_folder, measurement_index, light):
        xls_name=experiment.file_name
        structure_type= experiment.contact_type
        contents = xls_name.split("_")
        write_param=int(contents[3])
        
        if light==True:
            sheet_index=0
            data_folder=summary_folder + "\\data with light"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
        elif light==False:
            sheet_index = 3
            data_folder=summary_folder + "\\data without light"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

        if structure_type == "TLM":
            save_name= "%s_%s_TLM_%d_um.txt" %(date, experiment.structure, write_param)
        elif structure_type =="Areas":
            write_param = experiment.pads[write_param-1];
            save_name= "%s_%s_Areas_%f_Areas_%s.txt" % (date, experiment.structure, write_param)
        
        save_name= "%s\\%s" %(data_folder, save_name)
        export_sheet_to_txt(xls_name, sheet_index, save_name)
                
def export_light_dark_single_files(folder, light=True):
    index=0
    files = []
    summary_folder = folder
    folder+="\\data"
    for file in os.listdir(folder):
        print(index)
        files.append(file)
        TLM = experiment(30, [], structure="143-1", file_name=file, folder = folder)
        light_dark_single_txt_files_export(TLM, summary_folder, index, light)
        index+=1
    return files

export_light_dark_single_files(folder, light=True)