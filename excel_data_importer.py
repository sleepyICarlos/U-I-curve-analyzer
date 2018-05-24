# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:03:11 2018

@author: hartz
"""
import pyexcel
import pyexcel.ext.xlsx
import numpy as  np
import os
#%% 
"""convert xls to xlsx and write txt files
        !!!user imput required!!!"""
sample_folder = ("Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\" +
            "IHT_probe_station\\M12-0143\\143-1(Ar+H20)\\Areas")
book = sample_folder + "\\data\\23-5-18_143-1_Areas_light_dark.xls"
date="23-5-18"
sample_name = "143-1"
#%%
"""define experiment and data set"""
class experiment():
    def __init__(self, structure=[], pad_labels=[], contact_type="TLM", 
                 xls_name=[], sample_folder=[], comment=[], date=[]):
        self.xls_name= xls_name
        self.contact_type = contact_type
        self.structure = structure
        self.pad_labels= pad_labels             #contact pads
        self.comment =comment
        self.sample_folder= sample_folder
        self.data_folder= sample_folder +"\\data"
        self.date=date

#area_pad_labels=["6-6", "5-5"]      
area_pad_labels=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
area_pad_labels.reverse() #optional
TLM_data_set = experiment(structure=sample_name, xls_name=book, 
                          sample_folder = sample_folder, date=date)

Area_data_set = experiment(structure=sample_name, xls_name=book,
                           pad_labels=area_pad_labels,
                           contact_type="Areas", sample_folder = sample_folder,
                           date=date)
#%%
def export_sheet_to_txt(xls_name, sheet_index, save_name):  
    sheet_array = pyexcel.get_array(file_name = xls_name,
                                    sheet_index=sheet_index)
    #set header:
    rows = sheet_array[0][0]+"\t"+ sheet_array[0][1]
    np.savetxt(save_name,sheet_array[1:],fmt='%.4e',
               header=rows,comments="",delimiter="\t")
#%% 
"""read single xls containing only light/dark data, save sheets to txt-file"""
def all_sheet_txt_export(experiment, light=False): 
    xls_name=experiment.xls_name           #structure: TLM, Areas, Stripes, ...
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets=book.number_of_sheets()
    if light:
        export_folder=sample_folder + "\\data with light"
    else:
        export_folder=sample_folder + "\\data without light"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
        
    for sheet_index in range(number_of_sheets):
        if 0 < sheet_index < 3:
            continue
        else:
            print("handle sheet %d" %sheet_index)
            if sheet_index ==0:
                write_param = sheet_index+1
            else:
                write_param = sheet_index-1
                
            #select the right formatter depending on the measured structure:
            structure_type= experiment.contact_type
            if structure_type =="TLM":
                    write_param *= 30
                    save_name= "%s_%s_TLM_%d_um.txt" %(date, 
                                                       experiment.structure,
                                                       write_param)
            elif structure_type =="Areas":
                    print("TLM", write_param)
                    write_param = experiment.pad_labels[write_param-1];
                    save_name= "%s_%s_Areas_%s.txt" % (date, 
                                                       experiment.structure,
                                                       write_param)
                    
            save_name= "%s\\%s" %(export_folder, save_name)
            export_sheet_to_txt(xls_name, sheet_index, save_name)
#%%
Area_data_set = experiment(structure=sample_name, xls_name=book, 
                          sample_folder = sample_folder, date=date)
all_sheet_txt_export(Area_data_set, light=False)
#%% 
"""read single xls containing alternatingly light/ dark data
    save sheets to txt-file"""
def selcted_sheet_txt_export(experiment, light=False): 
    xls_name=experiment.xls_name           #structure: TLM, Areas, Stripes, ...
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets=book.number_of_sheets()
    
    #set export folder
    if light:
        export_folder=sample_folder + "\\data with light"
    else:
        export_folder=sample_folder + "\\data without light"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
     
    sets=int(number_of_sheets/2)
    for sheet_index in range(sets):
        if 0 < sheet_index < 3:
            continue
        else:
            write_param = sheet_index           #write param determines pad
            if sheet_index == 0:
                if not light:
                    sheet_index+=3
            else:
                sheet_index=(sheet_index+1)*2
                if not light:
                    sheet_index+=1
                print("handle sheet %d" %sheet_index)
                
                #select the right formatter depending on the measured structure:
                structure_type= experiment.contact_type
                if structure_type =="TLM":
                        write_param *= 30
                        save_name= "%s_%s_TLM_%d_um.txt" %(date, 
                                                           experiment.structure,
                                                           write_param)
                elif structure_type =="Areas":
                        print("TLM", write_param)
                        write_param = experiment.pad_labels[write_param-1];
                        save_name= "%s_%s_Areas_%s.txt" % (date, 
                                                           experiment.structure,
                                                           write_param)
                        
                save_name= "%s\\%s" %(export_folder, save_name)
                export_sheet_to_txt(xls_name, sheet_index, save_name)
                
    
#%%
Area_data_set = experiment(structure=sample_name, xls_name=book, 
                          sample_folder = sample_folder, date=date)
all_sheet_txt_export(Area_data_set, light=False)
#%%
"""for different books with the following structure: light + dark data:
    (only sheet0 and sheet3 contain relevant data)
    read xls-books and write txt.files to separate subfolders
    Takes as argument the corresponding folder like
    folder = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\
    IHT_probe_station\\M12-0143\\143-1(Ar+H20)\\TLM 2" """
def light_dark_single_txt_files_export(data_set, light):
    xls_name = data_set.xls_name
    folder = data_set.sample_folder
    structure_type = data_set.contact_type
    contents = xls_name.split("_")
    write_param=int(contents[-2])
    
    #select the right sheet and create data folder
    if light==True:
        sheet_index=0
        data_folder= folder + "\\data with light"
    elif light==False:
        sheet_index = 3
        data_folder = folder + "\\data without light"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    if structure_type == "TLM":
        save_name= "%s_%s_TLM_%d_um.txt" %(data_set.date, data_set.structure,
                                           write_param)
    elif structure_type =="Areas":
        write_param = data_set.pads[write_param-1];
        save_name= "%s_%s_Areas_%f_Areas_%s.txt" % (data_set.date, data_set.structure,
                                                    write_param)
    
    save_name= "%s\\%s" %(data_folder, save_name)
    export_sheet_to_txt(xls_name, sheet_index, save_name)

"""read all xls files in \data
   + extract sheet0/ sheet3 to light/dark data folders
   + use name of xls file"""
def export_light_dark_single_files(data_set, light=True):
    files = []
    data_folder= data_set.data_folder
    print(data_folder)
    for file in os.listdir(data_folder):
        print(file)
        files.append(file)
        data_set.xls_name = data_folder+"\\"+file
        light_dark_single_txt_files_export(data_set, light)
    return files

def export_light_dark(data_set):
    export_light_dark_single_files(data_set, light=False)
    export_light_dark_single_files(data_set, light=True)
#%%
"""sheets 1 and 2 have to be skipped, continue only when data sheet selected"""
def light_sheet_assigner(sheet):
    if sheet==0:
        return True, 1
    elif 0 < sheet < 3:
        return False, 0
    else:
        return True, sheet-1
    
def dark_sheet_assigner(sheet):
    if sheet==0:
        return True, 1
    elif 0 < sheet < 3:
        return False, 0
    else:
        return True, sheet-1
#%%
TLM_data_set = experiment(structure=sample_name, xls_name=book, 
                          sample_folder = sample_folder, date=date)
export_light_dark(TLM_data_set)
