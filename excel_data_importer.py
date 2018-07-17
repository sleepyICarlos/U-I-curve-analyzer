# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:03:11 2018

@author: hartz
"""
<<<<<<< HEAD
import excel_lib as ex
=======
import pyexcel
import pyexcel.ext.xlsx
import numpy as  np
import os
#%% 
"""convert xls to xlsx and write txt files
        !!!user imput required!!!
        precision is now set to 5 digits"""
sample_folder = ("Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\" +
            "IHT_probe_station\\M12-0143\\143-1(Ar+H20)\\bonded Areas")
book = sample_folder + "\\data\\25-5-18_143-1_Areas.xls"
date="25-5-18"
sample_name = "143-2"
area_pad_labels=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
#area_pad_labels=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
area_pad_labels.reverse() #optional
precision= 5 #digits
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
>>>>>>> origin/master

"""read xls and write txt files
        !!!user input required!!!
        precision is now preset to 5 digits"""

# adjustable parameters:
sample_path = "M12-0143\\U-I data\\143-2 Mg+Ar mill + H2O etch\\bonded Areas"
data_date = "22-5-18"
sample_name = "143-1"
# area_pad_labels = ["6-6", "5-5", "4-4"]  #
area_pad_labels=["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
# area_pad_labels.reverse()  # optional
office = True

my_sample_folder = ex.set_sample_folder(sample_path, office=False)
my_book = my_sample_folder + "\\data\\23-5-18_143-3_Areas_highres.xls"      # xls in file_name required
print("Read file:\n%s in dir:\n%s" % (my_book, my_sample_folder))

#%%
"""define work_station and data sets"""

TLM_data_set = ex.DataSet(structure=sample_name, xls_name=my_book, sample_folder=my_sample_folder, date=data_date)
Area_data_set = ex.DataSet(structure=sample_name, xls_name=my_book, sample_folder=my_sample_folder, date=data_date,
                           pad_labels=area_pad_labels, contact_type="Areas")

ex.all_sheets_txt_export(TLM_data_set, light=True)
# ex.alt_export_all(Area_data_set)
# ex.export_light_dark(Area_data_set)
# ex.export_light_dark(TLM_data_set)
# test github pushing
