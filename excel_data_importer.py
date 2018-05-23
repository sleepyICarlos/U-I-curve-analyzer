# -*- coding: utf-8 -*-
"""
Created on Tue May 22 15:03:11 2018

@author: hartz
"""
import pyexcel
import pyexcel.ext.xlsx



"""convert xls to xlsx and write txt files"""
#set file path, and name
#path = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\"
#wafer = "M12-0143\\"
#file =  "22-5-18_143-1_rauschen_0.5V_unbel-bel.xls"
#file_name = path + wafer + file
file_name = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data\\22-5-18_143-1_rauschen_0.5V_unbel-bel.xls"
dest_file_name = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data\\22-5-18_143-1_rauschen_0.5V_unbel-bel.xlsx"
#convert file to python dict and then save to xlxs.
book_dict = pyexcel.get_book_dict(file_name=file_name)
pyexcel.save_book_as(bookdict=book_dict, dest_file_name="converted_data.xlsx")
#%% Dienstag
book = pyexcel.get_book(file_name=file_name)

book.sheet_by_index(2)

data="22-5-18"
structure="S1"
"""writes txt files for different TLM structures"""
def TLM_txt_writer():
    for sheet in range(book.number_of_sheets()):
        print(sheet)
        if sheet != 0:
            sheet = sheet -1
        else:
            sheet -=2
        print(sheet)
        dist= sheet *30 #micrometer
        
        export_name = "%s_%s_TLM_%s_um" %(data, structure, dist)    
        print(export_name)
#%% Mittwoch
pyexcel.save_book_as(file_name=file_name, dest_file_name=dest_file_name)
my_sheet = pyexcel.get_sheet(file_name=dest_file_name, sheet_name="Settings") #choose from {"Data", "Settings", "Append1", ...}


book = pyexcel.get_book(file_name=file_name)
pyexcel.save_book_as(bookdict=book, dest_file_name="converted_data.xlsx")
book.sheet_by_index(3)
names=book.sheet_names()
number_of_sheets=book.number_of_sheets()











#%%
my_array = pyexcel.get_array(file_name=file_name)
my_dict = pyexcel.get_dict(file_name=file_name)



import pyexcel as p
sheet = p.get_sheet(file_name = file_name, name_columns_by_row=1)
sheet.save_as("me.sortable.html", display_length=10)
from IPython.display import IFrame
IFrame("me.sortable.html", width = 600, height = 500)
#sheet = pyexcel.get_sheet(file_name = file_name, name_columns_by_row=1)
#pyexcel.save_as(file_name, dest= path+"\\felix.xlsx")



book_dict.sheet1








## Retrieve current working directory (`cwd`)
#cwd = os.getcwd()
#path = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\IHT_probe_station\\M12-0143\\data"
## Change directory 
#os.chdir(path)
## List all files and directories in current directory
#file=os.listdir('.')

#from pyexcel._compact import OrderedDict