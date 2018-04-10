# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:46:37 2018

@author: hartz
"""
#%% 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy.polynomial.polynomial import polyval
#import data_import as load

#office = False
x_label="bias voltage (V)"
y_label="photocurrent (nA)"
sample_name="sample_name"
export_name = "export_name"
end_name = ".txt" #or ".dat"
plot_fit_output= False
save_name="save_name"#to do!
save= False
#%%
def plot_resistance_results(resistance_data, resistance_error_data, save=save):
    fig = plt.figure(0)
    x = resistance_data[0]
    y1, y1_err = resistance_data[1], resistance_error_data[1]
    y2, y2_err = resistance_data[2], resistance_error_data[2]
    plt.errorbar(x, y1, yerr=y1_err, label ="up-sweep", marker=".", linestyle="None")
    plt.errorbar(x, y2, yerr=y2_err, label ="down-sweep", marker=".", linestyle="None")
    plt.ylim(0, 250)
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("R (G$\Omega$)")
    plt.title(save_name+", R")

    if save:
        fig.savefig(save_name + " G.pdf", format="pdf")

#%%
def error_bar_plot(data, err, save_name="", y_limits =[0, 100], data_label=["up-sweep", "down-sweep"], axes_label=["measurement number", "$R$ (G$\Omega$)"], markersize=5, capsize=3, save=False):
    fig, ax = plt.subplots()
    x = data[0]
    y1, y1_err = data[1], err[1]
    y2, y2_err = data[2], err[2]
    ax.errorbar(x, y1, yerr=y1_err, label=data_label[0], marker=".", linestyle="None", markersize=markersize, capsize=capsize)
    ax.errorbar(x, y2, yerr=y2_err, label=data_label[1], marker=".", linestyle="None", markersize=markersize, capsize=capsize)
    ax.set_ylim(y_limits)
    plt.legend(data_label)
    plt.title(save_name)
    
    if save:
        fig.savefig(save_name + ".pdf", format="pdf")
#%%
def plot_correlation(x, y, y_err, save_name, fig, ax, data_label , axes_label=["x-label", "y-label"], markersize=5, capsize=3):#y_limits =[0, 100], x_err may be None
    #interpret error as systematic, due to sweep speed. By reciproke addition of 
    #the error is reduced, maximal beeing the better one. Average I & G by taking the mean.
    x=(x[1]+x[2])/2
    y=(y[1]+y[2])/2
    y_err=1/(1/y_err[1]+1/y_err[2])
    #plot_with_errorbars(x, y, y_err, fig, ax, save_name,  data_label=data_label, axes_label=axes_label, markersize=markersize, capsize=capsize)
    plot_with_errorbars(x, y, y_err, fig, ax, save_name, data_label=data_label, axes_label=axes_label, markersize=markersize, capsize=capsize) 
    
    # for plotting doped areas G/I correlation
    #Areas: D/UD y_limits= [0,0.08], x_limits = [0,30], y_limits= [0,0.15], x_limits = [0,80]
    #Stripes: y_limits= [0, 20], x_limits = [0, 160]
#%%
def plot_with_errorbars(x, y, y_err, fig, ax,
                        save_name, y_limits=None, x_limits= None,
                        data_label=["data-label"],
                        axes_label=["x-label", "y-label"], 
                        markersize=5, capsize=3, save=save):
    #interpret error as systematic, due to sweep speed. By reciproke addition of 
    #the error is reduced, maximal beeing the better one.    
    ax.errorbar(x, y, yerr=y_err, label=data_label[0], marker=".", linestyle="None", markersize=markersize, capsize=capsize)
    if y_limits!=None:
        ax.set_ylim(y_limits)
    if x_limits!= None:
        ax.set_xlim(x_limits)
    plt.legend(data_label)
    plt.title(save_name)
    ax.set_xlabel(axes_label[0]), ax.set_ylabel(axes_label[1])
    
    if save:
        fig.savefig(save_name + " errorbar-plot.pdf", format="pdf")
        
#%%

def process_data(data, fit_deg, fit_points, legend, fig, ax, axes_labels = ["x_param (X)", "y_param (Y)"], output = True):
    z=data.transpose()[0][1:]
    R=[]
    R_err= []
    slope=[]    #conductance here
    slope_err =[]
    for i in range(np.shape(data)[0]):
        if i>=1:
            slope_up  =  fit_with_errors(data, fit_deg, i, fit_points, 0, legend, output=output)
            slope_down = fit_with_errors(data, fit_deg, i, fit_points, 1, legend, output=output)
            R.append(np.abs(1/slope_up[0]))
            R.append(np.abs(1/slope_down[0]))
            R_err.append(np.abs(1/slope_up[0]**2*slope_up[1]))
            R_err.append(np.abs(1/slope_down[0]**2*slope_down[1]))
            slope.append(slope_up[0])
            slope.append(slope_down[0])
            slope_err.append(slope_up[1])
            slope_err.append(slope_down[1])

    #reshape variables
    R= np.reshape(R, (len(z),2))
    R_err= np.reshape(R_err, (len(z),2))
    slope = np.reshape(slope, (len(z), 2))
    slope_err= np.reshape(slope_err, (len(z),2))
    
    z=np.transpose(z)
    R=np.vstack((z, np.transpose(R)))
    R_err=np.vstack((z, np.transpose(R_err)))
    slope=np.vstack((z, np.transpose(slope)))
    slope_err=np.vstack((z, np.transpose(slope_err)))
    
    #plot resistances
    if output:
        #fig, ax = plt.subplots()       #put this in plot G-I correlation
        ax.set_xlabel(axes_labels[0])
        ax.set_ylabel(axes_labels[1])
        ax.legend(legend, loc = "lower right")
        plt.plot(R[1], ".", label="up-sweep"),plt.plot(R[2], ".", label="down-sweep")  
    
    return R , R_err, slope, slope_err

#%% data analysis
""" my fitting function for extracting the slope around 0 V,
polynomial of deg 3."""
def poly_1(x, a, b):
    result = a * x + b
    return result


def poly_3(x, a, b, c, d):
    result = a * x**3 + b*x**2 +c*x +d
    return result

def poly_5(x, a, b, c, d, e, f):
    result = a * x**5 + b*x**4 +c * x**3 + d*x**2 +e*x +f
    return result

def poly_7(x, a, b, c, d, e, f, g, h):
    result = a * x**7 + b*x**6 +c * x**5 + d*x**4 +e * x**3 + f*x**2 +g*x +h
    return result

def exp(x, a, b, c, d):
    result = a*np.exp(c*x) + b*np.exp(d*x)
    return result
    
class func():
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree
        
    def _return(self):
        return polyval(self.x, self.coeff)
    


def set_func(N):#comment: eventually I could also use polynomial from a library
    #, if implemented correctly, "exp" for exonential fit
    if N==1:
        return poly_1
    if N== 3:
        return poly_3
    if N==5:
        return poly_5
    if N==7:
        return poly_7
    if N=="exp": 
        return exp
    
#%% 
    
"""fits my fit function to the data, returns data which is called by
'compute_conductances(...)' later."""
def fit_with_errors(data, fit_deg, i_data, fit_points, sweep_direction, legend, output = plot_fit_output):        #fit_points == number of fitpoints, # sweep_direction== 0, 1 for up and downsweep, respectively
    #fitting
    fit_points=int(fit_points/2)-1
    voltages=data[0][1:]
    #identify values around 0 V
    if sweep_direction==0:
        x_length = int(len(voltages)/4+1)
        x_index_1, x_index_2= x_length-fit_points, x_length+fit_points
    else:
        x_length = int(len(voltages)*3/4)
        x_index_1, x_index_2= x_length-fit_points-1, x_length+fit_points+2
    
    x=voltages[x_index_1:x_index_2]  #define data
    y=data[i_data][x_index_1:x_index_2]
    func = set_func(fit_deg)
    popt, pcov = curve_fit(func, x, y)
    
    perr = np.sqrt(np.diag(pcov))
    if fit_deg!="exp":
        slope_index=fit_deg-1
    else: 
        slope_index=0  #hack for exponential fitting, 1 for b in e^bx
    slope, slope_error =popt[slope_index], perr[slope_index]
    #plotting
    if output:
        fig, ax = plt.subplots()
        ax.plot(x, func(x, *popt), "g-", label = "fit")
        ax.plot(x, y, "b.", label = "y-data")
        ax.legend(loc="best")
        comment= "slope "+ str(round(slope, 5)) +" nA/V \n R = " + str(round(1/slope, 0)) +" G$\Omega$"
        i_label=int(data[i_data][0])-1
        print(i_label)
        print("label_index %d"  %(i_label))
        #plt.title(save_name+", " +legend[i_label])     #ZnSeMarchMeetingHack
        plt.text(0,0, comment)
        ax.set_xlabel(x_label)
        ax.set_ylabel("current (nA)")
        plt.show()
        
        if save:
            a=[]
        #    fig.savefig(save_name + legend[i_label] + "_lin_fit.pdf", format="pdf")  #ZnSeMarchMeetingHack
            
    return slope, slope_error
#%%
def title(sample_name, structure, T_anneal, measurement = "I-G", implanted=True):
    figure_title ="sample %s %s T_anneal %d %s" %(sample_name, structure, T_anneal, measurement)
    save_title = figure_title       #could be expanded to s.o different
    if implanted:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nAl+Cl implantation at 1 keV\nafter annealing at %d °C for 3 min" %(sample_name, structure, T_anneal)
    else:
        figure_title ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nno implantation\nafter annealing at %d °C for 3 min" %(sample_name, structure, T_anneal)
    
    return figure_title, save_title, figure_comment
#%%
"""Assign current I to x, conductance G with errors to y, and send those params
 to plot_correlation"""

def plot_variable_correlations(x, y, y_err, save_name, fig, ax, data_label , axes_label=["x-label", "y-label"], markersize=5, capsize=3):#y_limits =[0, 100], x_err may be None
    #interpret error as systematic, due to sweep speed. By reciproke addition of 
    #the error is reduced, maximal beeing the better one. Average y by taking the mean.
    y=(y[1]+y[2])/2
    y_err=1/(1/y_err[1]+1/y_err[2])
    #plot_with_errorbars(x, y, y_err, fig, ax, save_name,  data_label=data_label, axes_label=axes_label, markersize=markersize, capsize=capsize)
    plot_with_errorbars(x, y, y_err, fig, ax, save_name, data_label=data_label, axes_label=axes_label, markersize=markersize, capsize=capsize) 
    
    # for plotting doped areas G/I correlation
    #Areas: D/UD y_limits= [0,0.08], x_limits = [0,30], y_limits= [0,0.15], x_limits = [0,80]
    #Stripes: y_limits= [0, 20], x_limits = [0, 160]
#%%
def plot_G_I_correlation(data_set, fit_deg, fit_points, output=plot_fit_output):         #data_set and data_labels have to be corresponding. each are multi-dimensional!!! Ideally each data set were a struct with something like sample name, data_labels, ...
    axes_label=["I at +/- 10 V (nA)", "$G$ (1/G$\Omega$)"]
    data_labels=data_set.names
    fig, ax = plt.subplots()
    for i in range(len(data_set.data)):
        x=data_set.data[i][0]
        x=x.transpose()
        x_len=int(np.shape(x)[0]/2)
        x0= x[0][1:]
        x1=-(x[1][1:]+x[-1][1:])/2
        x2=(x[x_len][1:]+x[x_len+1][1:])/2
        x=np.vstack((x0, x1, x2))
        (y, y_err)= (process_data(data_set.data[i][0], fit_deg, fit_points, data_labels[i], fig, ax, output=output))[2:4]
        data_set.G.append(y)
        data_set.G_err.append(y_err)
        save_name_i = "save_name"+" data_set %s" %str(i)#to do!!!
        plot_correlation(x, y, y_err, save_name_i, fig, ax, data_label=data_set.names, axes_label=axes_label, markersize=5, capsize=3)
        print(data_labels[i] +", "+str(i))
#%%
"""Assign current circumference to x, conductance G with errors to y, and send those params
 to plot_correlation, G_L_A stands for conductance, Length, Area, Circumference"""
 
def plot_G_L_A_circ__correlation(data_set, fit_deg, fit_points, param, output=plot_fit_output):      #data set = i.e. doped #structure takes "TLM, Areas, Homo or Stripes"   #data_set and data_labels have to be corresponding. each are multi-dimensional!!! Ideally each data set were a struct with something like sample name, data_labels, ...
    data_labels=data_set.names
    data_set.G, data_set.G_err=[], []
    fig, ax = plt.subplots()
    if param=="circ":
        axes_label=["circumference (mm)", "$G$ (1/G$\Omega$)"]
        xdata_set=data_set.circ
    if param =="L":
        axes_label=["length (um)", "$G$ (1/G$\Omega$)"]
        xdata_set=data_set.L
    if param =="A":
        axes_label=["area (mm^2)", "$G$ (1/G$\Omega$)"] #^unicode: U+02C6
        xdata_set=data_set.A
    #if param =="G":                to-do 
    for i in range(len(data_set.data)):
        x=xdata_set[i]
        (y, y_err)= (process_data(data_set.data[i][0], fit_deg, fit_points, data_labels[i], fig, ax, output=output))[2:4]
        data_set.G.append(y)
        data_set.G_err.append(y_err)
        save_name_i = "save_name"+" data_set %s" %str(i)#to do!!!
        #x_plot=data_set.circ[i]
        plot_variable_correlations(x, y, y_err, save_name_i, fig, ax, data_label=data_set.names, axes_label=axes_label, markersize=5, capsize=3)
        print(data_labels[i] +", "+str(i))
    #return x
#%%
#plot_G_I_correlation(doped, 1, 20)
#plot_G_I_correlation(undoped, 1, 20)
#my_x=plot_G_L_A_circ__correlation(doped, 1, 20, param="A")
#my_x=plot_G_L_A_circ__correlation(doped, 1, 20, param="A")
POI=["A", "L", "circ"]
def plot_all_POI(data_set, POI, fit_deg, fit_points):
    for interest in range(len(POI)):
        print(interest, len(POI))
        plot_G_L_A_circ__correlation(data_set, fit_deg, fit_points, param=POI[interest])

plot_all_POI(doped, ["A", "L", "circ"], "exp", 199)
#plot_all_POI(undoped, ["A", "L", "circ"], "exp", 5)
#fit_deg, fit_points=1, 20
#plot_G_L_A_circ__correlation(doped, fit_deg, fit_points, param="L")

#%%
def fit_N_points(data, N, labels, output= False):       #fits and plots slope at 0 V
    (x_data,
     x_error_data,
     y_data,
     y_error_data) = (process_data(data, 3, N, labels, output=output))
    
    error_bar_plot(x_data, x_error_data, save_name+" R, N_%d" %N)
