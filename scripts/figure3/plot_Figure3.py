# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 08:51:13 2019

@author: Fub
"""
import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
import os


plt.figure(figsize=(12,18))

#######################
dty=dty = np.float32
mean_RF_CO2=1.789
std_RF_CO2=0.1*mean_RF_CO2
TMP= np.array([line for line in csv.reader(open('D:/Thomas/OSCAR-master-EXP2-3.0-baseline/data/HistClim_HadCRUT4/#DATA.HistClim_HadCRUT4.1850-2014.gst.csv','r'))], dtype=dty)
HistClim_gst_had = np.zeros([310+1],dtype=dty)
HistClim_gst_had[150:]=TMP[:-4,0]
HistClim_gst_had[150:310+1] = HistClim_gst_had[150:310+1] - np.mean(HistClim_gst_had[201:231])
mean_D_gst=np.mean(  HistClim_gst_had[-21:-1]  )
std_D_gst=0.9*mean_D_gst
weight=[]
weight1=[]
weight2=[]
RF_CO2=[]
temp=[]

for filename in os.listdir('D:/Thomas/v4/OSCAR-master-v4/results_EXP1/'):   
    if 'att' in filename:
        TMP=np.array([line for line in csv.reader(open('D:/Thomas/v4/OSCAR-master-v4/results_EXP1/'+filename,'r'))],dtype=dty)
        if np.isnan(TMP[0,-1]):
            continue
        TMP=np.array([line for line in csv.reader(open('D:/Thomas/v4/OSCAR-master-v4/results_EXP1/'+filename,'r'))],dtype=dty)
        RF_CO2.append(TMP[1,:])
        
        filename_tmp='weight'+filename[11:]
        TMP=np.array([line for line in csv.reader(open('D:/Thomas/v4/OSCAR-master-v4/results_EXP1/'+filename_tmp,'r'))],dtype=dty)
        D_gst_tmp=TMP[0,:]
        D_gst_tmp -= np.mean(D_gst_tmp[201:231])
        RF_CO2_tmp=TMP[1,-1]
        weight1.append(1 / np.sqrt(2*np.pi) / (std_D_gst) * np.exp(- 0.5 * (np.mean(D_gst_tmp[-21:-1])-mean_D_gst)**2 / std_D_gst**2))
        weight2.append(1 / np.sqrt(2*np.pi) / (std_RF_CO2) * np.exp(- 0.5 * (RF_CO2_tmp-mean_RF_CO2)**2 / std_RF_CO2**2))
RF_CO2=np.array(RF_CO2)    
weight1=np.array(weight1)
weight2=np.array(weight2)
weight=weight1*weight2
#del NAN
temp=np.where(np.isnan(weight))
weight=np.delete(weight,temp,0)
RF_CO2=np.delete(RF_CO2,temp,0)     
wmean_RF_CO2=np.array([np.sum(RF_CO2[:,0]*weight)/np.sum(weight),np.sum(RF_CO2[:,1]*weight)/np.sum(weight),np.sum(RF_CO2[:,2]*weight)/np.sum(weight)])
wstd_RF_CO2=[np.sqrt(np.sum((RF_CO2[:,0]-wmean_RF_CO2[0])**2*weight)/np.sum(weight)),np.sqrt(np.sum((RF_CO2[:,1]-wmean_RF_CO2[1])**2*weight)/np.sum(weight)),np.sqrt(np.sum((RF_CO2[:,2]-wmean_RF_CO2[2])**2*weight)/np.sum(weight))]
wmean_RF_CO2_sum=np.sum(np.sum(RF_CO2,1)*weight)/np.sum(weight)
wstd_RF_CO2_sum=np.sqrt(np.sum((np.sum(RF_CO2,1)-wmean_RF_CO2_sum)**2*weight)/np.sum(weight))
#######################
###########################################################
ax0 = plt.subplot2grid((2,1),(0,0))
#ax0=plt.subplot()
TMP=np.array([line for line in csv.reader(open('D:/Thomas/v4/OSCAR-master-v4/EXP4-clim.csv','r'))],dtype=dty)
data0=[]
for i in range(3):
    temp=TMP[:,i]
    data0.append( wmean_RF_CO2[i]*  temp/np.sum(temp) )
data0=np.array(data0).T
data_shape=np.shape(data0)

period=[100,50,25,25,10,10,10,10,1,1,4,4,2,2,2,2,2,1]
year=[0]
for i in range(len(period)):
    year.append(year[i]+period[i])

color_list=['#FF0000','#ff5a4e','#B5D04B']
label_list=['FF-CO$_2$','LUC-CO$_2$','Climate-carbon feedback']
bottom=np.zeros([data_shape[0],2])
for i in range(data_shape[0]):
    for j in [2,1,0]:
        if j!=2:
            hatch=''
        else:
            hatch='.....'
        if data0[i,j]>=0:    
            ax0.bar(1750+year[i],data0[i,j]/period[i],width=period[i],color=color_list[j],bottom=bottom[i,0],align='edge',edgecolor='k',hatch=hatch)
            bottom[i,0]+=data0[i,j]/period[i]
        else:
            ax0.bar(1750+year[i],data0[i,j]/period[i],width=period[i],color=color_list[j],align='edge',edgecolor='k',bottom=bottom[i,1],hatch=hatch)
            bottom[i,1]+=data0[i,j]/period[i]
for j in [0,1]:
    ax0.bar(0,0,width=0,color=color_list[j],bottom=bottom[i,0],align='edge',edgecolor='k',hatch='',label=label_list[j])
j+=1
ax0.bar(0,0,width=0,color=color_list[j],bottom=bottom[i,0],align='edge',edgecolor='k',hatch='.....',label=label_list[j])
ax0.set_xlim([1900,2010])
ax0.set_ylabel(r'Contribtions to $RF_{CO_2-2010}$ (mW m$^{-2}$ yr$^{-1}$)',fontsize='large')
ax0.set_xticks(np.arange(1900,2010+0.1,20))
ax0.set_yticks(np.arange(-0.01,0.1,0.01))
ax0.set_yticklabels(np.arange(-10,100,10),fontsize='large')
ax0.set_ylim([0,0.09])
ax0.set_title('a', fontweight='bold') 
ax0.legend()
ax0.set_xlabel('year of forcing',fontsize='large')
#################################################

dty = np.float32 
data=[]
for filename in os.listdir('D:/Thomas/v4/OSCAR-master-v4/results_EXP4/'):  
    TMP=np.array([line for line in csv.reader(open('D:/Thomas/v4/OSCAR-master-v4/results_EXP4/'+filename,'r'))],dtype=dty)
    data.append(TMP/np.sum(TMP)*1.81)
data=np.array(data)
data_mean=np.mean(data,0)
data_std=np.std(data,0)

data=data_mean
#EXP3
dty=dty = np.float32
mean_RF_CO2=1.789
std_RF_CO2=0.1*mean_RF_CO2
TMP= np.array([line for line in csv.reader(open('D:/Thomas/OSCAR-master-EXP3-3.0-baseline/data/HistClim_HadCRUT4/#DATA.HistClim_HadCRUT4.1850-2014.gst.csv','r'))], dtype=dty)
HistClim_gst_had = np.zeros([310+1],dtype=dty)
HistClim_gst_had[150:]=TMP[:-4,0]
HistClim_gst_had[150:310+1] = HistClim_gst_had[150:310+1] - np.mean(HistClim_gst_had[201:231])
mean_D_gst=np.mean(  HistClim_gst_had[-21:-1]  )
std_D_gst=0.9*mean_D_gst
weight=[]
weight1=[]
weight2=[]
RF_CO2=[]
D_gst=[]
for filename in os.listdir('D:/Thomas/v4/OSCAR-master-v4/results_EXP3/'):   
    if 'att' in filename:
        TMP=np.array([line for line in csv.reader(open('D:/Thomas/v4/OSCAR-master-v4/results_EXP3/'+filename,'r'))],dtype=dty)        
        if np.isnan(TMP[0,-1]):
            continue
        RF_CO2.append(TMP[0,:])
        filename_tmp='weight'+filename[11:]
        TMP=np.array([line for line in csv.reader(open('D:/Thomas/v4/OSCAR-master-v4/results_EXP3/'+filename_tmp,'r'))],dtype=dty)
        D_gst_tmp=TMP[0,:]
        D_gst_tmp -= np.mean(D_gst_tmp[201:231])
        D_gst.append(D_gst_tmp[-1])
        weight1.append(1 / np.sqrt(2*np.pi) / (std_D_gst) * np.exp(- 0.5 * (D_gst_tmp[-1]-mean_D_gst)**2 / std_D_gst**2))
        RF_CO2_tmp=TMP[1,-1]
        weight2.append(1 / np.sqrt(2*np.pi) / (std_RF_CO2) * np.exp(- 0.5 * (RF_CO2_tmp-mean_RF_CO2)**2 / std_RF_CO2**2))
weight1=np.array(weight1)
weight2=np.array(weight2)
weight=weight1*weight2
RF_CO2=np.array(RF_CO2)    
D_gst=np.array(D_gst)  
RF_CO2=np.array(RF_CO2)    
D_gst=np.array(D_gst)  
wmean_RF_CO2=[]
wstd_RF_CO2=[]
temp=np.shape(RF_CO2)
for i in range(temp[1]):
    if np.nan in RF_CO2[:,i]:
        continue
    wmean_RF_CO2.append(np.nansum(RF_CO2[:,i]*weight)/np.nansum(weight))
    wstd_RF_CO2.append(np.sqrt(np.nansum((RF_CO2[:,i]-wmean_RF_CO2[i])**2*weight)/np.nansum(weight)))

for i in range(12):
    data[:,i]=data[:,i]/np.sum(data[:,i])*wmean_RF_CO2[i]

list1=['FF-CO2','LUC-CO2']+['CH$_4$','GHG other','O3s','O3t','Aerosol','LUC albedo','H2Os','BC snow','Contrails','Volcano','Solar']
#temp11=[0      ,1]+        [2       ,3          ,4    ,5    ,6        ,7           ,8     ,9        ,10         ,11       ,12]
color_list={'FF-CO2':'#FF0000','LUC-CO2':'#ff5a4e','GHG other':'#993300','CH$_4$':'#FF6600','O3t':'#66FF66',
    'O3s':'#FF9999','Aerosol':'#00CCFF','LUC albedo':'#006600',
    'H2Os':'#FFCC00','BC snow':'#CC0066','Contrails':'#660099','Solar':'#FFE490',
    'Volcano':'#0000FF'}
RF_name = ['FF-CO$_2$','LUC-CO$_2$','CH$_4$','GHG other','O$_3$s','O$_3$t','Aerosol','LUC albedo','H$_2$Os','BC snow','Contrails','Volcano','Solar'  ]    
RF_loc   =[          1,           2,       3,       7,       4,        10,              5,        6,           9,         11,       12,        8]
RF_label=RF_name

ax1 = plt.subplot2grid((2,1),(1,0))
#ax1=plt.subplot()
data_shape=np.shape(data)
period=[100,50,25,25,10,10,10,10,1,1,4,4,2,2,2,2,2,1]
year=[0]
for i in range(len(period)):
    year.append(year[i]+period[i])
bottom=np.zeros([data_shape[0],2])

for i in range(data_shape[0]):
#    for j in range(data_shape[1]):
    for j in [2,4,5,6,8,9,10,11]+[0,1,3,7,12]:    
        if j<=1:
            continue
        hatch='.....'
        if data[i,j]>=0:    
            ax1.bar(1750+year[i],data[i,j]/period[i],width=period[i],color=color_list[list1[j]],bottom=bottom[i,0],align='edge',edgecolor='k',hatch=hatch)
            bottom[i,0]+=data[i,j]/period[i]
        else:
            ax1.bar(1750+year[i],data[i,j]/period[i],width=period[i],color=color_list[list1[j]],align='edge',edgecolor='k',bottom=bottom[i,1],hatch=hatch)
            bottom[i,1]+=data[i,j]/period[i]
    temp=(data0[i,2]-np.sum(bottom[i]))/period[i]
    if temp>=0:
        ax1.bar(1750+year[i],temp,width=period[i],color='#FF0000',bottom=bottom[i,0],align='edge',edgecolor='k',hatch=hatch)  
        bottom[i,0]+=temp  
'''
label_list=['CO$_2$','CH$_4$','LL-GHG other',
            'O$_3$s','O$_3$t',
            'All Aerosol','LUC albedo','H$_2$Os',
            'BC snow','Contrails','Volcano','Solar'  ]
color_list=['#FF0000','#FF6600','#993300',
            '#FF9999','#66FF66',
            '#00CCFF','#006600','#FFCC00',
            '#CC0066','#660099','#0000FF','#FFE490']
'''
label_list=['CO$_2$','LL-GHG other',
            'LUC albedo',
            'Solar'  ]+['CH$_4$',
            'O$_3$s','O$_3$t',
            'Anthropogenic Aerosol','H$_2$Os',
            'BC snow','Contrails','Volcano Aerosol']
color_list=['#FF0000','#993300',
            '#006600',
            '#FFE490']+['#FF6600',
            '#FF9999','#66FF66',
            '#00CCFF','#FFCC00',
            '#CC0066','#660099','#0000FF']

for i in range(len(label_list)):
   ax1.bar(0,0,width=0,color=color_list[i],label=label_list[i],bottom=0,align='edge',edgecolor='k',hatch=hatch) 
ax1.legend(ncol=3)
ax1.set_xlim([1900,2010])
ax1.set_ylabel(r'Contribtions to $RF_{CO_2-2010}$ induced by climate-carbon feedbacks (mW m$^{-2}$ yr$^{-1}$)',fontsize='large')
ax1.set_xticks(np.arange(1900,2010+0.1,20))

ax1.set_yticks(np.arange(-0.01,0.030,0.005))
ax1.set_yticklabels(np.arange(-10,30,5),fontsize='large')
ax1.set_ylim([-0.007,0.026])
ax1.set_xlabel('year of forcing',fontsize='large')
ax1.set_title('b', fontweight='bold') 
plt.savefig('Figure3-new2-new.png',dpi=600)
