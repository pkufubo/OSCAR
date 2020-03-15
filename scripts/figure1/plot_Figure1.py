# -*- coding: utf-8 -*-
"""
Plot Figure1
"""

import csv
import numpy  as np
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
dty=np.float32

execfile('OSCAR.py')
data=[]
for filename in os.listdir('./results_ideal/'):   
    TMP=np.array([line for line in csv.reader(open('./results_ideal/'+filename,'r'))],dtype=dty)
    if np.isnan(TMP[0,-1]):
        continue
    data_tmp=[]
    for i in range(8):
        data_tmp.append(TMP[i+8,:]-TMP[i,:])
    data_tmp=np.array(data_tmp)
    data.append(data_tmp)
data=np.array(data)
N=int(data.shape[0])

plt.figure(figsize=(10,19))
color_list={'FF-CO2':'#FF0000','LUC-CO2':'#993300','GHG other':'#FF6600','O3t':'#66FF66',
    'O3s':'#FF9999','Aerosol':'#00CCFF','LUC albedo':'#006600',
    'H2Os':'#FFCC00','BC snow':'#CC0066','Contrails':'#660099','Solar':'#FFE490',
    'Volcano':'#0000FF'}
the_year=1964
xticks_list=[1910,1920,1940,1964,1980,2000,2010]
xticks_list=np.arange(1910,2011,10)
ax1 = plt.subplot2grid((5,1),(0,0))
#ax1 = plt.subplot2grid((9,1),(0,0))
plt.plot([2011-100,2011],[0,0],color='k')
RFvolc_tmp=RFvolc.copy()
RFvolc_tmp[the_year-1700]*=0
#ax1.plot(np.arange(2011-100,2011),RFvolc_tmp[-100:],color=color_list['Volcano'],label='Rm$_{64}$: Removing volcano RF in 1964 \n from IPCC volcano RF (base)',linewidth=3)
#ax1.plot(np.arange(2011-100,2011),RFvolc[-100:],color=color_list['Volcano'],linestyle='--',linewidth=1)
ax1.plot(np.arange(2011-100,2011),RFvolc_tmp[-100:],color=color_list['Volcano'],label='Volcano RF in Rm$_{64}$ simulation',linewidth=1.5)
ax1.plot(np.arange(2011-100,2011),RFvolc[-100:],color='grey',linestyle='--',linewidth=1,label='Volcano RF in control simulation')
ax1.legend(fontsize='x-large')
ax1.set_ylabel('Volcano radiative\nforcing (W m$^{-2}$)',fontsize='x-large')
ax1.set_xlim([2011-100,2010])
ax1.set_title('a', fontweight='bold')
ax1.plot([the_year,the_year],[-3.2,-1.7],linestyle=':',color='k')
ax1.set_ylim(-2.7,0.5)
plt.xticks(xticks_list,xticks_list,fontsize='x-large',fontstretch='condensed')
plt.yticks(fontsize='x-large')
ax2 = plt.subplot2grid((5,1),(1,0))

ax2.plot([2011-100,2011],[0,0],color='k',linewidth=1)
ax2.plot(np.arange(2010-100,the_year),np.mean(data[:,0,1910-1700:the_year-1700],0),color=color_list['GHG other'],linewidth=1,label='The response of GMST')
plot_mean=np.mean(data[:,0,the_year-1700:],0)
plot_std=np.std(data[:,0,the_year-1700:],0)
ax2.plot(np.arange(the_year,2011),plot_mean,color=color_list['GHG other'],linewidth=1.5)
ax2.plot(np.arange(the_year,2011),plot_mean-plot_std,color=color_list['GHG other'],linewidth=1,linestyle=':')
ax2.plot(np.arange(the_year,2011),plot_mean+plot_std,color=color_list['GHG other'],linewidth=1,linestyle=':')
ax2.legend(loc='upper left',fontsize='x-large')
ax2.set_ylabel('Global mean surface\ntemperature response ($^{\circ}$C)',fontsize='x-large')
ax2.set_xlim([2010-100,2010])
plt.xticks(xticks_list,xticks_list,fontsize='x-large',fontstretch='condensed')
ax2.set_ylim([0.0,0.13])
ax2.plot([the_year,the_year],[0,0.15],linestyle=':',color='k')
ax2.text(the_year+2,0.11,'Peak-T year: +1 year',fontsize='x-large')
ax2.set_title('b', fontweight='bold')
plt.yticks(fontsize='x-large')

ax3 = plt.subplot2grid((5,1),(2,0))
ax3.plot([2011-100,2011],[0,0],color='k',linewidth=1)
ax3.plot(np.arange(2010-100,the_year),np.mean(data[:,1,1910-1700:the_year-1700],0),color=color_list['FF-CO2'],linewidth=1.5,label='The response of atmos-CO$_2$\nconcentration')
ax3.plot(np.arange(the_year,2011),np.mean(data[:,1,the_year-1700:],0),color=color_list['FF-CO2'],linewidth=1.5)
plot_mean=np.mean(data[:,1,the_year-1700:],0)
plot_std=np.std(data[:,1,the_year-1700:],0)
ax3.plot(np.arange(the_year,2011),plot_mean,color=color_list['FF-CO2'],linewidth=1.5)
ax3.plot(np.arange(the_year,2011),plot_mean-plot_std,color=color_list['FF-CO2'],linewidth=1,linestyle=':')
ax3.plot(np.arange(the_year,2011),plot_mean+plot_std,color=color_list['FF-CO2'],linewidth=1,linestyle=':')
ax3.legend(loc='upper left',fontsize='x-large')
ax3.set_ylabel('Atmosphere CO$_2$\nconcentration response\n(ppm)',fontsize='x-large')
ax3.set_xlim([2010-100,2010])
plt.xticks(xticks_list,xticks_list,fontsize='x-large',fontstretch='condensed')
ax3.set_ylim([0.0,0.6])
ax3.plot([the_year,the_year],[0,0.6],linestyle=':',color='k')
ax3.text(the_year+6,0.35,'Peak-C year: +4 year',fontsize='x-large')
ax3.set_title('c', fontweight='bold')
plt.yticks(fontsize='x-large')

ax4 = plt.subplot2grid((5,1),(3,0))
ax4.plot([2011-100,2011],[0,0],color='k',linewidth=1)

ax4.plot(np.arange(2010-100,the_year),np.mean(data[:,2,1910-1700:the_year-1700],0),color=color_list['LUC albedo'],linewidth=1.5,label='The response of RH')
ax4.plot(np.arange(2010-100,the_year),np.mean(data[:,3,1910-1700:the_year-1700],0),color=color_list['O3t'],linewidth=1.5,label='The response of NPP')
ax4.plot(np.arange(2010-100,the_year),np.mean(data[:,4,1910-1700:the_year-1700],0),color='k',linewidth=1.5,label='The response of net land sink')

plot_mean=np.mean(data[:,2,the_year-1700:],0)
plot_std=np.std(data[:,2,the_year-1700:],0)
ax4.plot(np.arange(the_year,2011),plot_mean,color=color_list['LUC albedo'],linewidth=1.5)
ax4.plot(np.arange(the_year,2011),plot_mean-plot_std,color=color_list['LUC albedo'],linewidth=1,linestyle=':')
ax4.plot(np.arange(the_year,2011),plot_mean+plot_std,color=color_list['LUC albedo'],linewidth=1,linestyle=':')

plot_mean=np.mean(data[:,3,the_year-1700:],0)
plot_std=np.std(data[:,3,the_year-1700:],0)
ax4.plot(np.arange(the_year,2011),plot_mean,color=color_list['O3t'],linewidth=1.5)
ax4.plot(np.arange(the_year,2011),plot_mean-plot_std,color=color_list['O3t'],linewidth=1,linestyle=':')
ax4.plot(np.arange(the_year,2011),plot_mean+plot_std,color=color_list['O3t'],linewidth=1,linestyle=':')

plot_mean=np.mean(data[:,4,the_year-1700:],0)
plot_std=np.std(data[:,4,the_year-1700:],0)
ax4.plot(np.arange(the_year,2011),plot_mean,color='k',linewidth=1.5)
ax4.plot(np.arange(the_year,2011),plot_mean-plot_std,color='k',linewidth=1,linestyle=':')
ax4.plot(np.arange(the_year,2011),plot_mean+plot_std,color='k',linewidth=1,linestyle=':')

ax4.legend(loc='upper left',fontsize='x-large')
ax4.set_ylabel('The response of\nland carbon sink (GtC)',fontsize='x-large')
ax4.set_xlim([2010-100,2010])
plt.xticks(xticks_list,xticks_list,fontsize='x-large',fontstretch='condensed')
ax4.set_ylim([-0.2,0.3])
ax4.plot([the_year,the_year],[-0.21,0.3],linestyle=':',color='k')
ax4.set_title('d', fontweight='bold')
plt.yticks(fontsize='x-large')

ax5 = plt.subplot2grid((5,1),(4,0))
ax5.plot([2011-100,2011],[0,0],color='k',linewidth=1)

ax5.plot(np.arange(2010-100,the_year),np.mean(data[:,5,1910-1700:the_year-1700],0),color='#00CCFF',linewidth=1.5,label='The response of Fin')
ax5.plot(np.arange(2010-100,the_year),np.mean(data[:,6,1910-1700:the_year-1700],0),color='#0000FF',linewidth=1.5,label='The response of Fout')
ax5.plot(np.arange(2010-100,the_year),np.mean(data[:,7,1910-1700:the_year-1700],0),color='k',linewidth=1.5,label='The response of net ocean sink')

plot_mean=np.mean(data[:,5,the_year-1700:],0)
plot_std=np.std(data[:,5,the_year-1700:],0)
ax5.plot(np.arange(the_year,2011),plot_mean,color='#00CCFF',linewidth=1.5)
ax5.plot(np.arange(the_year,2011),plot_mean-plot_std,color='#00CCFF',linewidth=1,linestyle=':')
ax5.plot(np.arange(the_year,2011),plot_mean+plot_std,color='#00CCFF',linewidth=1,linestyle=':')

plot_mean=np.mean(data[:,6,the_year-1700:],0)
plot_std=np.std(data[:,6,the_year-1700:],0)
ax5.plot(np.arange(the_year,2011),plot_mean,color='#0000FF',linewidth=1.5)
ax5.plot(np.arange(the_year,2011),plot_mean-plot_std,color='#0000FF',linewidth=1,linestyle=':')
ax5.plot(np.arange(the_year,2011),plot_mean+plot_std,color='#0000FF',linewidth=1,linestyle=':')

plot_mean=np.mean(data[:,7,the_year-1700:],0)
plot_std=np.std(data[:,7,the_year-1700:],0)
ax5.plot(np.arange(the_year,2011),plot_mean,color='k',linewidth=1.5)
ax5.plot(np.arange(the_year,2011),plot_mean-plot_std,color='k',linewidth=1,linestyle=':')
ax5.plot(np.arange(the_year,2011),plot_mean+plot_std,color='k',linewidth=1,linestyle=':')

ax5.legend(loc='upper left',fontsize='x-large')
ax5.set_ylabel('The response of\nocean carbon sink (GtC)',fontsize='x-large')
ax5.set_xlim([2011-100,2010])
plt.xticks(xticks_list,xticks_list,fontsize='x-large',fontstretch='condensed')
ax5.set_ylim([-0.05,0.25])
ax5.plot([the_year,the_year],[-0.16,0.25],linestyle=':',color='k')
ax5.set_title('e', fontweight='bold')
plt.yticks(fontsize='x-large')

plt.savefig('Figure1.pdf',dpi=600)
