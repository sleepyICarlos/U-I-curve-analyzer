# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26   11:35:04 2018

@author: hartz
"""
#%%
"""Define some classes containing information on the data saving location
sample set than can carry all analysis quantities important for our photocurrent
analysis"""

import numpy as np
import os


save_folder = "Z:\sciebo\promotion\6_LogsDataAnalysis\1_data\IHT_probe_station\MA-0084\python"

office =True




#%%
def set_path(folder, office = True):
    if office:
        folder = "Z:\sciebo" + folder
    else:
        folder = "D:\documents\sciebo" + folder
    return folder

#%%
def fig_comment(sample_name, structure, T_anneal, implanted=True):
    if implanted:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nAl+Cl implantation at 1 keV\nafter annealing at %d °C for 3 min" %(sample_name, structure, T_anneal)
    else:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nno implantation\nafter annealing at %d °C for 3 min" %(sample_name, structure, T_anneal)
    return figure_comment
#%%
def data_set_fig_comment(sample_name, structure, T_anneal, implanted=True):
    if implanted:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nAl+Cl implantation at 1 keV\nafter annealing at %s for 3 min" %(sample_name, structure, T_anneal)
    else:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nno implantation\nafter annealing at %s for 3 min" %(sample_name, structure, T_anneal)
    return figure_comment


#%%
class sample_set():
    def __init__(self, folders=[], names=[], T_anneal=[], structure="Stripes", implanted= True, office = True):
        self.figure_comment = data_set_fig_comment("all", structure, "variable temperatures", implanted=implanted)
        self.folders = folders
        self.names   = names
        self.structure = structure
        self.T_anneal= T_anneal
        self.office = office
        if implanted:
            self.implanted=implanted
        else:
            self.implanted=False
        self.data =[]
        self.I_max=[]
        self.G=[]
        self.G_err=[]
        self.L=[]
        self.L_err=[]
        self.A=[]
        self.A_err=[]
        self.labels=[]
        self.circ=[]


undoped, doped = sample_set(), sample_set()

class data_set():                   #circ: circumference
    def __init__(self, folder, selector, sample_set, sample_name, T_anneal):
        folder = set_path(folder, office = office)
        structure = sample_set.structure
        implanted=sample_set.implanted
        export_name = sample_name +" " + structure
        data = import_data_selector(folder, selector = selector)
        data_import=np.transpose(data[-1])
        labels = data[1]      
        area = data_import[0]
        circ= data_import[1]
        length= data_import[2]

        figure_comment = fig_comment(sample_name, structure, T_anneal, implanted=implanted)
        self.office=sample_set.office
        self.sample_name = sample_name
        self.save_name = "sample %s %d °C anneal %s" %(sample_name, T_anneal , structure)
        self.export_name = export_name
        self.folder = folder
        self.data = data
        self.T_anneal = T_anneal
        self.sample_name = sample_set
        self.figure_comment=figure_comment
        self.labels= labels
        sample_set.folders.append(folder)
        sample_set.names.append(sample_name)
        sample_set.T_anneal.append(T_anneal)
        sample_set.data.append(data)
        sample_set.labels.append(labels)
        sample_set.A.append(area)
        sample_set.L.append(length)
        sample_set.circ.append(circ)
#%%
#name= "3-2-18_D1_Stripes_1-1_L.txt"
def filename_data_assigner(name, separator="_"):
    contents = name.split(separator)
    structure = contents[2]
    if structure == "Areas":
        length=1
        area=1
        circumference=1


    if structure == "Stripes":
        length=range(15)
        circumference, area=length, length
#        contents = name.split(separator) 
#        i = len(contents)
#        if i==5:
#            stripe_nr = int(contents[i-2].split("_")[0].split("-")[0])-1
#            width= contents[i-1].split(".")[0]
#            if width == "S":
#                width = 0.05
#            if width == "M":
#                width = 0.075
#            if width=="L":
#                width = 0.1
#            length = L[stripe_nr]
#            circumference= calc_circumference(length, width)
#            area=length*width  
#        else:
#            stripe_nr = int(contents[i-1].split("_")[0].split("-")[0])-1
#            if stripe_nr <= 8:
#                width = 0.5
#            else: width = 0.75
#            length = L[stripe_nr]
#            circumference= calc_circumference(length, width)
#            area=length*width
  
    return area, circumference, length
##%%
#filename_data_assigner("3-2-18_D1_Stripes_10-10.txt", separator="_")
#%%
def calc_circumference(L, W):
    return 2*(L+W)
#%%
def import_data(folder, end_name=".txt", separator="_"):
    data, x2_data, voltages, values, zdata, files =[], [], [], [], [], []    #pad distance: any param read from file name
    measurement_counter = 0
    measurement_description = []
    for file in os.listdir(folder):
        if file.endswith(end_name):
            contents = file.split(separator)    
            l = len(contents)
            measurement_counter += 1
            zdata_value = measurement_counter
            measurement_description.append(contents[l-2]+" "+ contents[l-1].split(".")[0])
            

            zdata.append(zdata_value)
            files.append(file)
            x2_data.append(filename_data_assigner(file, separator))
            new_value=np.genfromtxt(folder+"\\"+file,usecols=0, skip_header=1).astype(float)
            new_value*= 1e9             #convert from mA to nA
            values.append(np.concatenate((np.array([zdata_value]),new_value)))       # skip_header: skips device names, usecol: uses 2nd column (current)
    
    #values.sort(key=lambda x: x[0])
    #values=np.array(values)*1e6 #convert to nA 
    file_list = files
    print("%d files imported successfully:" %(len(files)) )
    print(files)
    voltages = np.concatenate((np.array([0]),np.genfromtxt(folder+"\\"+files[0],usecols=1, skip_header = 1))) 
    data = np.vstack((voltages,values))
    data_labels= measurement_description
    return data, file_list, data_labels, x2_data
#%%
def import_data_selector(folder, selector="with", end_name=".txt", separator="_"):
    data, x2_data, voltages, values, zdata, files =[], [], [], [], [], []    #pad distance: any param read from file name
    measurement_counter = 0
    measurement_description = []
    for file in os.listdir(folder):
        if file.endswith(end_name):
            contents = file.split(separator)
            l = len(contents)
            for i in np.arange(l):
                if contents[i] == selector:
                    measurement_counter += 1
                    zdata_value = measurement_counter
                    measurement_description.append(file)
                

                    zdata.append(zdata_value)
                    files.append(file)
                    x2_data.append(filename_data_assigner(file, separator))
                    new_value=np.genfromtxt(folder+"\\"+file,usecols=0, skip_header=1).astype(float)
                    new_value*= 1e9             #convert from mA to nA
                    values.append(np.concatenate((np.array([zdata_value]),new_value)))       # skip_header: skips device names, usecol: uses 2nd column (current)
    
    #values.sort(key=lambda x: x[0])
    #values=np.array(values)*1e6 #convert to nA 
    file_list = files
    print("%d files imported successfully:" %(len(files)) )
    print(files)
    voltages = np.concatenate((np.array([0]),np.genfromtxt(folder+"\\"+files[0],usecols=1, skip_header = 1))) 
    data = np.vstack((voltages,values))
    data_labels= measurement_description
    return data, file_list, data_labels, x2_data


#%%
"""define data location and put it in one data_struct"""
#
##def load_all(structure="Areas"):
#structure = "Areas" #"Stripes"
#D1_folder = "\ZnSe\M12-0084\IHT Probestation\D1\%s\data" %structure
#D2_folder = "\ZnSe\M12-0084\IHT Probestation\D2\%s\data" %structure
#D4_folder = "\ZnSe\M12-0084\IHT Probestation\D4\%s\data" %structure
#D6_folder = "\ZnSe\M12-0084\IHT Probestation\D6\%s\data" %structure
#
#UD1_folder = "\ZnSe\M12-0084\IHT Probestation\\UD1\%s\data" %structure
#UD2_folder ="\ZnSe\M12-0084\IHT Probestation\\UD2\%s\data" %structure
#UD3_folder = "\ZnSe\M12-0084\IHT Probestation\\UD3\%s\data" %structure
#UD4_folder = "\ZnSe\M12-0084\IHT Probestation\\UD4\%s\data" %structure
#
#undoped, doped = sample_set([], [], [], implanted=False, office = office), sample_set([], [], [], implanted=True, office= office)
#
#D1 = data_set(D1_folder, doped, "D1", 250)
#D2 = data_set(D2_folder, doped, "D2", 300)
#D4 = data_set(D4_folder, doped, "D4", 250)
#D6 = data_set(D6_folder, doped, "D6", 20)
#UD1 = data_set(UD1_folder, undoped, "UD1", 20)
#UD2 = data_set(UD2_folder, undoped, "UD2", 250)     #data for stripes 7,8,9,10 is missing
#UD3 = data_set(UD3_folder, undoped, "UD3", 350)
#UD4 = data_set(UD4_folder, undoped, "UD4", 250)
##now we have: doped.data[0]==D1.data
#print("imported doped samples successfully:\n%s \n"  
#      "imported undoped samples successfully:\n%s" %(doped.names, undoped.names))
##    return undoped, doped
##undoped, doped = load_all()
#
#data_import=np.transpose(doped.data[0][3])
#area= data_import[0]
#circumference= data_import[1]
#length= data_import[2]

#%%
structure = "Stripes" #"Stripes"
D1_folder = "\ZnSe\M12-0084\IHT Probestation\\D1\\2018-03-15_photocurrent_experiments\D1\Stripes\data" #%structure D1 covered

undoped, doped = sample_set([], [], [], implanted=False, office = office), sample_set([], [], [], implanted=True, office= office)

D1_6a_6c_covered = data_set(D1_folder, "Stripes", doped, "D1", 250)



#now we have: doped.data[0]==D1.data
print("imported doped samples successfully:\n%s \n"  
      "imported undoped samples successfully:\n%s" %(doped.names, undoped.names))
#    return undoped, doped
#undoped, doped = load_all()

data_import=np.transpose(doped.data[0][3])
area= data_import[0]
circumference= data_import[1]
length= data_import[2]
#%%
#structure = "Homo"
#UD2_folder = "\ZnSe\M12-0084\IHT Probestation\\UD2\%s\data" %structure
#undoped, doped = sample_set([], [], [], implanted=False, office = office), sample_set([], [], [], implanted=True, office= office)
#UD2 = data_set(UD2_folder, undoped, "UD2", 250)
##%%
#structure = "Stripes_orientation"
#D1_folder = "\ZnSe\M12-0084\IHT Probestation\D1\2018-03-20_D1\%s\data"
#D1 = data_set(D1_folder, doped, "D1", 250)