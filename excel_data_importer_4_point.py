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
        !!!user imput required!!!
        precision is now set to 5 digits"""
sample_folder = ("Z:\\data\\170 UI data\\170-2")
file_name = "2018-06-21_M12-170-2_TLM_30...180_um"
book = sample_folder +"\\"+ file_name +".xls"
date="2018-06-21"
sample_name = "170-2"
area_pad_labels=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
#area_pad_labels=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
area_pad_labels.reverse() #optional
digits= 5 #digits
UI_columns = [5, 1, 6] #valid for 4 point measurements on IHT-Probe-station

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
#%%
TLM_data_set = experiment(structure=sample_name, xls_name=book, 
                          sample_folder = sample_folder, date=date)

Area_data_set = experiment(structure=sample_name, xls_name=book,
                           pad_labels=area_pad_labels,
                           contact_type="Areas", sample_folder = sample_folder,
                           date=date)
#%%
'''columns is list of columns to be read
    (i.e. [2, 1] for x-vals in column 2 and y-vals in column 1)'''
def export_sheet_to_txt(xls_name, sheet_index, columns, save_name, precision=digits):  
    sheet_array = pyexcel.get_array(file_name = xls_name,
                                    sheet_index=sheet_index)
    precision-=1
    my_format='%.'+str(int(precision))+'e'
    #set header:
    #rows = "\t\t\t\t\t" #str(sheet_array[0][columns[0]])+"\t"+ str(sheet_array[0][columns[1]])+"\t"+ str(sheet_array[0][columns[2]])
    np.savetxt(save_name, sheet_array[1:],fmt=my_format, header = "", comments="",delimiter="\t")
    
#%% 
"""read single xls containing only light/dark data, save sheets to txt-file"""
def all_sheets_txt_export(experiment, columns= UI_columns): 
    xls_name=experiment.xls_name           #structure: TLM, Areas, Stripes, ...
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets=book.number_of_sheets()
    export_folder=sample_folder + "\\data"
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
                    print("Areas", write_param)
                    write_param = experiment.pad_labels[write_param-1];
                    save_name= "%s_%s_Areas_%s.txt" % (date, 
                                                       experiment.structure,
                                                       write_param)
                    
            save_name= "%s\\%s" %(export_folder, save_name)
            export_sheet_to_txt(xls_name, sheet_index, UI_columns, save_name)
#%%
all_sheets_txt_export(TLM_data_set)
