# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:03:11 2018

@author: hartz
"""
import pyexcel
import pyexcel.ext.xlsx
import numpy as  np

#%% Dienstag
"""convert xls to xlsx and write txt files"""
#set file path, and name
path = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\"
file_name = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data\\22-5-18_143-1_rauschen_0V_unbel-bel_retake.xls"
folder = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\143-1(Ar+H20)\\TLM 1"
date="22-5-18"
structure="S1"
#%% structure
class experiment():
    def __init__(self, file_name, multiplicator, pads, contact_type="TLM", structure="S1", comment=[], folder =[]):
        self.file_name= file_name
        self.contact_type = contact_type
        self.structure = structure
        self.multiplicator = multiplicator          #30 for TLM, 1 otherwise
        self.pads= pads             #contact pads
        self.comment =comment
        self.folder = folder
        
area_pads=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
TLM = experiment(file_name, 30, [], structure="S1")
Areas = experiment(file_name, 1, area_pads, contact_type="Areas")
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
            
def txt_light_dark_single_export(experiment, folder):
    for file in os.listdir(folder)
    xls_name=experiment.file_name
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
#%%
#my_array = pyexcel.get_array(file_name=file_name)
#my_dict = pyexcel.get_dict(file_name=file_name)

#pyexcel.save_book_as(file_name=file_name, dest_file_name=dest_file_name)
#my_sheet = pyexcel.get_sheet(file_name=dest_file_name, sheet_name="Settings") #choose from {"Data", "Settings", "Append1", ...}
#
#
#book = pyexcel.get_book(file_name=file_name)
#pyexcel.save_book_as(bookdict=book, dest_file_name="converted_data.xlsx")
#%%
#"""load book and save sheets to single txt files"""
#book = pyexcel.get_book(file_name=file_name)
#names=book.sheet_names()
#number_of_sheets=book.number_of_sheets()

#convert file to python dict and then save to xlxs.
#book_dict = pyexcel.get_book_dict(file_name=file_name)
#pyexcel.save_book_as(bookdict=book_dict, dest_file_name="converted_data.xlsx")
## Retrieve current working directory (`cwd`)
#cwd = os.getcwd()
#path = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data"
## Change directory 
#os.chdir(path)
## List all files and directories in current directory
#file=os.listdir('.')

#from pyexcel._compact import OrderedDict
#for commandline in anaconda in dir of xls files: convert to xlsx
#$ pyexcel transcode test.xls test-out.xlsx


##%%
#import pyexcel as p
#sheet = p.get_sheet(file_name = file_name, name_columns_by_row=1)
#sheet.save_as("me.sortable.html", display_length=10)
#from IPython.display import IFrame
#IFrame("me.sortable.html", width = 600, height = 500)
##sheet = pyexcel.get_sheet(file_name = file_name, name_columns_by_row=1)
##pyexcel.save_as(file_name= file_name, dest_file_name= path+"\\felix.xlsx")
