# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:22:11 2018

@author: hartz
"""
import os
import numpy as np
import pyexcel


class Office:
    def __init__(self, user, work_station, folder):
        self.user = user
        self.PC = work_station
        self.folder = folder

class DataSet:
    def __init__(self, structure="", pad_labels=[], contact_type="TLM",
                 xls_name="", sample_folder="", comment="", date=""):
        self.xls_name = xls_name
        self.contact_type = contact_type
        self.structure = structure
        self.pad_labels = pad_labels             # labels for identifying different contact pads
        self.comment = comment
        self.sample_folder = sample_folder
        self.data_folder = sample_folder + "\\data"
        self.date = date


# fixed parameters:
path_office = "Z:\\sciebo\\promotion\\6_LogsDataAnalysis\\1_data\\" + "IHT_probe_station\\"
path_home = "D:\\documents\\sciebo\\ZnSe\\wafer\\"
data_precision = 5           # number of digits

home_office = Office("FH", "Felix-PC", path_home)
uni_office = Office("FH", "ag-bluhm-16", path_office)


def set_path(work_station, sub_folder):
    path = work_station.folder + sub_folder
    print(path)
    return path


def set_sample_folder(sub_path, office=True):
    if office:
        work_station= uni_office
    else:
        work_station = home_office
    my_sample_folder = set_path(work_station, sub_path)
    return my_sample_folder


def export_sheet_to_txt(xls_name, sheet_index, save_name, precision=data_precision):
    sheet_array = pyexcel.get_array(file_name=xls_name,
                                    sheet_index=sheet_index)
    precision -= 1
    my_format = '%.' + str(int(precision)) + 'e'  # set header
    rows = sheet_array[0][0] + "\t" + sheet_array[0][1]
    np.savetxt(save_name, sheet_array[1:], fmt=my_format,
               header=rows, comments="", delimiter="\t")


"""read single xls containing only light/dark data, save sheets to txt-file"""


def all_sheets_txt_export(data, light=False):
    xls_name = data.xls_name  # structure: TLM, Areas, (STRIPES: todo)
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets = book.number_of_sheets()
    if light:
        export_folder = data.sample_folder + "\\data with light"
    else:
        export_folder = data.sample_folder + "\\data without light"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    for sheet_index in range(number_of_sheets):
        if 0 < sheet_index < 3:
            continue
        else:
            print("handle sheet %d" % sheet_index)
            if sheet_index == 0:
                write_param = sheet_index + 1
            else:
                write_param = sheet_index - 1

            # select the right formatter depending on the measured structure:
            structure_type = data.contact_type
            if structure_type == "TLM":
                write_param *= 30
                save_name = "%s_%s_TLM_%d_um.txt" % (data.date, data.structure, write_param)

            elif structure_type == "Areas":
                print("Areas", write_param);
                write_param = data.pad_labels[write_param - 1]
                save_name = "%s_%s_Areas_%s.txt" % (data.date, data.structure, write_param)
            else:
                continue

            export_name = "%s\\%s" % (export_folder, save_name)
            export_sheet_to_txt(xls_name, sheet_index, export_name)


#%%
"""read single xls containing alternatingly light/ dark data
    save sheets to txt-file"""


def alt_sheet_export(data, light=False):
    xls_name = data.xls_name  # structure: TLM, Areas, Stripes, ...
    book = pyexcel.get_book(file_name=xls_name)
    number_of_sheets = book.number_of_sheets()

    # set export folder
    if light:
        export_folder = data.sample_folder + "\\data with light"
    else:
        export_folder = data.sample_folder + "\\data without light"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
        print("folder created: %s" % export_folder)

    # select right sheet and assign it to correct data field
    sets = int(number_of_sheets / 2)
    print("amount of measured pad sizes: %s" % (str(sets - 1)))
    for index in range(sets):
        if index == 1:
            print("skip, index = %s" % index)
            continue
        else:
            # write param determines pad
            if index == 0:
                sheet_index, write_param = 0, 0
                if not light:
                    sheet_index = 3
            else:
                sheet_index, write_param = index * 2, index - 1
                if not light:
                    sheet_index += 1

            print("handle sheet %d" % sheet_index)

            # select the right formatter depending on the measured structure:
            structure_type = data.contact_type
            if structure_type == "TLM":
                write_param *= 30
                save_name = "%s_%s_TLM_%d_um.txt" % (data.date, data.structure, write_param)

            elif structure_type == "Areas":
                print("Areas", write_param)
                write_param = data.pad_labels[write_param]
                save_name = "%s_%s_Areas_%s.txt" % (data.date, data.structure, write_param)

            print("save to folder %s: %s" % (export_folder, save_name))
            save_name = "%s\\%s" % (export_folder, save_name)
            export_sheet_to_txt(xls_name, sheet_index, save_name)


def alt_export_all(data_set):
    alt_sheet_export(data_set, light=True)
    alt_sheet_export(data_set, light=False)


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
    # select the right sheet and create data folder
    if light:
        sheet_index = 0
        data_folder = folder + "\\data with light"
    elif not light:
        sheet_index = 3
        data_folder = folder + "\\data without light"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    write_param = str(contents[-2])
    if structure_type == "TLM":
        save_name = "%s_%s_TLM_%s_um.txt" % (data_set.date, data_set.structure, write_param)
    elif structure_type == "Areas":
        save_name = "%s_%s_Areas_%f_Areas_%s.txt" % (data_set.date, data_set.structure, write_param)

    save_name = "%s\\%s_high_res" % (data_folder, save_name)
    export_sheet_to_txt(xls_name, sheet_index, save_name)


"""read all xls files in \data
   + extract sheet0/ sheet3 to light/dark data folders
   + use name of xls file"""


def export_light_dark_single_files(data_set, light=True):
    files = []
    data_folder = data_set.data_folder
    print(data_folder)
    for file in os.listdir(data_folder):
        print(file)
        files.append(file)
        data_set.xls_name = data_folder + "\\" + file
        light_dark_single_txt_files_export(data_set, light)
    return files


def export_light_dark(data_set):
    export_light_dark_single_files(data_set, light=False)
    export_light_dark_single_files(data_set, light=True)
