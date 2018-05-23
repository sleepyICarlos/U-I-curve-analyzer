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
file_name = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data\\22-5-18_143-1_rauschen_0.5V_unbel-bel.xls"
dest_file_name = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data\\22-5-18_143-1_rauschen_0.5V_unbel-bel.xlsx"

"""load book and save sheets to single txt files"""
book = pyexcel.get_book(file_name=file_name)
names=book.sheet_names()
number_of_sheets=book.number_of_sheets()

book.sheet_by_index(2)

data="22-5-18"
structure="S1"
"""writes txt files for different TLM structures"""
def TLM_txt_writer(book):
    for sheet in range(book.number_of_sheets()):
        print(sheet)
        if sheet == 0:
            sheet += 1
        if 0 < sheet < 2:
            sheet
        else:
            sheet -=2
        print(sheet)
        dist= sheet *30 #micrometer
        
        export_name = "%s_%s_TLM_%s_um" %(data, structure, dist)    
        print(export_name)
#%% structure
class experiment():
    def __init__(self, file_name, multiplicator, pads, contact_type="TLM", structure=[], comment=[]):
        self.file_name= file_name
        self.contact_type = contact_type
        self.structure = structure
        self.multiplicator = multiplicator          #30 for TLM, 1 otherwise
        self.pads= pads             #contact pads
        self.comment =comment
        
TLM = experiment(file_name, 30, [])
#["1-1", "2-2", "3-3", "4-4", "5-5", "6-6"]
#%% 
"""read xls, save sheet to txt-file"""
def export_sheet_to_txt(xls_name, sheet_index, save_name):  
    sheet_array = pyexcel.get_array(file_name = xls_name, sheet_index=sheet_index)
    #header
    rows = sheet_array[0][0]+"\t"+ sheet_array[0][1]
    #export & save, bug-fix with header to circumvent problems with different 
    #data formats
    np.savetxt(save_name,my_array[1:],fmt='%.4e',header=rows,comments="",delimiter="\t")
    
 
def txt_export(xls_name, structure):            #structure: TLM, Areas, Stripes, ...
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets=book.number_of_sheets()
    
    for sheet_index in range(book.number_of_sheets()):
        print(sheet)
        if 0 < sheet_index < 2:
            break
        else:
            if sheet_index ==0:
                write_param = sheet_index+1
            else:
                write_param = sheet_index-1
            write_param = sheet *structure.multiplicator    #micrometer in case of TLM
            export_sheet_to_txt(xls_name, sheet_index, )
#%%
    
    
    
    
sheet=book.sheet_by_index(3)
sheet.save_as("append1.csv", delimiter="\t")



#%%



#%%
my_array = pyexcel.get_array(file_name=file_name)
my_dict = pyexcel.get_dict(file_name=file_name)


#%%
import pyexcel as p
sheet = p.get_sheet(file_name = file_name, name_columns_by_row=1)
sheet.save_as("me.sortable.html", display_length=10)
from IPython.display import IFrame
IFrame("me.sortable.html", width = 600, height = 500)
#sheet = pyexcel.get_sheet(file_name = file_name, name_columns_by_row=1)
#pyexcel.save_as(file_name= file_name, dest_file_name= path+"\\felix.xlsx")





pyexcel.save_book_as(file_name=file_name, dest_file_name=dest_file_name)
my_sheet = pyexcel.get_sheet(file_name=dest_file_name, sheet_name="Settings") #choose from {"Data", "Settings", "Append1", ...}


book = pyexcel.get_book(file_name=file_name)
pyexcel.save_book_as(bookdict=book, dest_file_name="converted_data.xlsx")



#%%
#convert file to python dict and then save to xlxs.
#book_dict = pyexcel.get_book_dict(file_name=file_name)
pyexcel.save_book_as(bookdict=book_dict, dest_file_name="converted_data.xlsx")
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