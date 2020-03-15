import csv
import numpy  as np
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

dty=dty = np.float32

mean_RF_CO2=1.789
std_RF_CO2=0.1*mean_RF_CO2

TMP= np.array([line for line in csv.reader(open('data/HistClim_HadCRUT4/#DATA.HistClim_HadCRUT4.1850-2014.gst.csv','r'))], dtype=dty)
HistClim_gst_had = np.zeros([310+1],dtype=dty)
HistClim_gst_had[150:]=TMP[:-4,0]
HistClim_gst_had[150:310+1] = HistClim_gst_had[150:310+1] - np.mean(HistClim_gst_had[201:231])

mean_D_gst=np.mean(  HistClim_gst_had[-21:-1]  )
std_D_gst=0.9*mean_D_gst


weight=[]
weight1=[]
weight2=[]
D_gst=[]
temp=[]


for filename in os.listdir('results_exp2/'):   
    if 'att' in filename:
        TMP=np.array([line for line in csv.reader(open('results_exp2/'+filename,'r'))],dtype=dty)
        if np.isnan(TMP[0,-1]):
            continue
        D_gst.append(TMP[0,:])
        filename_tmp='weight'+filename[11:]
        TMP=np.array([line for line in csv.reader(open('results_exp2/'+filename_tmp,'r'))],dtype=dty)
        
        D_gst_tmp=TMP[0,:]
        D_gst_tmp -= np.mean(D_gst_tmp[201:231])
        temp.append(D_gst_tmp[-1])
        RF_CO2_tmp=TMP[1,-1]
        weight1.append(1 / np.sqrt(2*np.pi) / (std_D_gst) * np.exp(- 0.5 * (np.mean(D_gst_tmp[-21:-1])-mean_D_gst)**2 / std_D_gst**2))
        weight2.append(1 / np.sqrt(2*np.pi) / (std_RF_CO2) * np.exp(- 0.5 * (RF_CO2_tmp-mean_RF_CO2)**2 / std_RF_CO2**2))

weight1=np.array(weight1)
weight2=np.array(weight2)
weight=weight1*weight2
D_gst=np.array(D_gst)  

wmean_D_gst=[]
wstd_D_gst=[]
temp=np.shape(D_gst)
for i in range(temp[1]):
    if np.nan in D_gst[:,i]:
        continue
    wmean_D_gst.append(np.nansum(D_gst[:,i]*weight)/np.nansum(weight))
    wstd_D_gst.append(np.sqrt(np.nansum((D_gst[:,i]-wmean_D_gst[i])**2*weight)/np.nansum(weight)))

wmean_D_gst_sum=np.nansum(np.sum(D_gst,1)*weight)/np.nansum(weight)
wstd_D_gst_sum=np.sqrt(np.nansum((np.sum(D_gst,1)-wmean_D_gst_sum)**2*weight)/np.nansum(weight))



#RF_name = ['FF-CO$_2$','LUC-CO$_2$','GHG \n other','O$_3$t','O$_3$s','Aerosol','LUC \n albedo','H$_2$O$_s$','BC \n snow','Contrails','\nVolcano','Solar'  ]
RF_name = ['CO$_2$','CH$_4$','LL-GHG other','O$_3$s','O$_3$t','Anthropogenic Aerosol','LUC albedo','H$_2$Os','BC snow','Contrails','Volcano Aerosol','Solar'  ]
RF_loc   =[        1,      2,             10,       7,       6,        8,             11,        3,           4,          5,         9,       12]
RF_color = ['#FF0000' ,'#FF6600'   ,'#993300'  ,'#FF9999','#66FF66','#00CCFF','#006600'       ,'#FFCC00'   ,'#CC0066'   ,'#660099'  ,'#0000FF','#FFE490']
RF_label=[RF_name[RF_loc.index(i+1)] for i in np.arange(len(RF_name))]
            
w=0.6
we = 0.1
d = 0.03
da = 0.03
x=10
f=plt.figure(figsize=(25,18))
#ax = plt.subplot2grid((2,x),(0,0),colspan=x-1)
colspan_ax1=2
ax = plt.subplot2grid((2,x),(0,colspan_ax1),colspan=x-colspan_ax1)
#ax=plt.subplot()
plt.plot([-1,len(RF_name)],[0,0],'k-')
#sort 11.26
for n in range(len(wmean_D_gst)):
    plt.bar(RF_loc[n]-1,wmean_D_gst[n],width=w,color=RF_color[n],yerr=wstd_D_gst[n],capsize=4,edgecolor='k')
ax.set_title('b', fontweight='bold') 

for n in range(len(wmean_D_gst)):
    sgn = np.sign(wmean_D_gst[n])
    txt = str(np.round(wmean_D_gst[n]*1000,1))
    if ((txt[0]!='-')&(len(txt)==3))|((txt[0]=='-')&(len(txt)==4)):
        txt += '0'
    if (txt[0]=='-'):
        txt = '$-$'+txt[1:]
    if sgn>0:
        plt.text(RF_loc[n]-1+0.25,wmean_D_gst[n]+sgn*1*da,txt,ha="right",va="bottom",fontsize="xx-large")
    elif sgn<0:
        plt.text(RF_loc[n]-1+0.25,wmean_D_gst[n]+sgn*da,txt,ha="right",va="top",fontsize="xx-large")

#lable SLCFs
plt.plot([1,8],[-0.55,-0.55],color='k',linestyle='--')
plt.plot([1,1],[-0.1,-0.55],color='k',linestyle='--')
plt.plot([8,8],[-0.2,-0.55],color='k',linestyle='--')
plt.text(4.1,-0.48,'SLCFs')

# axis
plt.axis([-1+0.2,len(RF_name)-0.2,-0.6,1.0])
plt.xticks(np.arange(0,len(RF_name)),RF_label,fontsize='xx-large',fontstretch='condensed')
plt.yticks(np.arange(-0.6,1.1,0.2),fontsize='xx-large',alpha=0)
ax2 = ax.twinx()
ax2.set_ylim(-0.6,1)
ax2.set_yticks(np.arange(-0.6,1.1,0.2))
ax2.set_yticklabels(np.arange(-600,1001,200),fontsize='xx-large')
ax2.set_ylabel('Contribtions to $\Delta$GMST in 2010 (mK)',fontsize='xx-large')
plt.yticks(fontsize='x-large')

#ax1 = plt.subplot2grid((2,x),(0,x-1))
ax1 = plt.subplot2grid((2,x),(0,0),colspan=colspan_ax1)
plt.plot([-1,1],[0,0],'k-')
plt.bar(0.,np.sum(wmean_D_gst)*3/5.,width=w,color='0.5',edgecolor='k')
plt.errorbar(0,np.sum(wmean_D_gst)*3/5.,yerr=np.sqrt(np.sum(np.multiply(wstd_D_gst[1:],wstd_D_gst[1:])))*3/5.,color="k",capsize=4)
# annotation
txt = str(np.round(np.sum(wmean_D_gst),2))
plt.text(0-3.5*d,np.sum(wmean_D_gst)*3/5.+1*d,txt,ha="right",va="bottom",fontsize="xx-large")
# axis
plt.axis([-1+0.2,1-0.2,-0.4,0.8])
plt.yticks(np.arange(-0.4,0.8+0.01,0.2),['' for n in range(len(np.arange(-0.4,0.8+0.01,0.2)))])
ax1.set_ylim(-0.4,0.8)
ax1.set_yticks(list(np.arange(-0.4,0.8+0.01,0.2)))
ax1.set_yticklabels(['','']+[''+str(n)+'' for n in list(np.round(np.arange(-0.4,0.8+0.01,0.2)*5/3.,1))[2:]],fontsize='xx-large')
ax1.set_xticks([0])
ax1.set_xticklabels(['Total'],fontsize='xx-large')
ax1.set_ylabel('$\Delta$GMST in 2010($^{\circ}$C)',fontsize='xx-large')
ax1.set_title('a', fontweight='bold')
    

dty=dty = np.float32
mean_RF_CO2=1.789
std_RF_CO2=0.1*mean_RF_CO2

TMP= np.array([line for line in csv.reader(open('data/HistClim_HadCRUT4/#DATA.HistClim_HadCRUT4.1850-2014.gst.csv','r'))], dtype=dty)
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

for filename in os.listdir('results_EXP1/'):   
    if 'att' in filename:
        TMP=np.array([line for line in csv.reader(open('results_EXP1/'+filename,'r'))],dtype=dty)
        if np.isnan(TMP[0,-1]):
            continue
        TMP=np.array([line for line in csv.reader(open('results_EXP1/'+filename,'r'))],dtype=dty)
        RF_CO2.append(TMP[1,:])
        
        filename_tmp='weight'+filename[11:]
        TMP=np.array([line for line in csv.reader(open('results_EXP1/'+filename_tmp,'r'))],dtype=dty)
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

##PLOT
colspan_ax2=4
ax2 = plt.subplot2grid((2,x),(1,0),colspan=colspan_ax2)
#ax2=plt.subplot()

plt.plot([-1,4],[0,0],'k-')
plt.bar(0.,wmean_RF_CO2_sum/20.,width=w,color='0.5',edgecolor='k',hatch='')
plt.bar(0.,wmean_RF_CO2[2]/20.,width=w,color='0.5',edgecolor='k',hatch='.....')
plt.errorbar(0,wmean_RF_CO2_sum/20.,yerr=wstd_RF_CO2_sum/20.,color="k",capsize=4)

plt.bar(1.,wmean_RF_CO2[0]/20.,width=w,color='#FF0000',edgecolor='k',hatch='')
plt.errorbar(1,wmean_RF_CO2[0]/20.,yerr=wstd_RF_CO2[0]/20.,color="k",capsize=4)
plt.bar(2.,wmean_RF_CO2[1]/20.,width=w,color='#ff5a4e',edgecolor='k',hatch='')
plt.errorbar(2,wmean_RF_CO2[1]/20.,yerr=wstd_RF_CO2[1]/20.,color="k",capsize=4)
###11.14
plt.bar(3.,wmean_RF_CO2[2]/20.,width=w,color='#B5D04B',edgecolor='k',hatch='.....')
plt.errorbar(3,wmean_RF_CO2[2]/20.,yerr=wstd_RF_CO2[2]/20.,color="k",capsize=4)
txt = str(np.round(np.sum(wmean_RF_CO2[2]),2))
plt.text(3,wmean_RF_CO2[2]/20.,txt,ha="right",va="bottom",fontsize="xx-large")

cc_feedback=wmean_RF_CO2[2]
cc_feedback_std=wstd_RF_CO2[2]


txt = str(np.round(np.sum(wmean_RF_CO2_sum),2))
plt.text(0,np.sum(wmean_RF_CO2_sum)/20,txt,ha="right",va="bottom",fontsize="xx-large")
for i in np.arange(len(['FF-CO$_2$','LUC-CO$_2$'])):
    txt = str(np.round(wmean_RF_CO2[i],2))
    plt.text(i+1,wmean_RF_CO2[i]/20.,txt,ha="right",va="bottom",fontsize="xx-large")

ax2.set_xticks([0,1,2,3])
ax2.set_xticklabels(['Total','FF-CO$_2$\nEmissions','LUC-CO$_2$\nEmissions','Climate-carbon\nfeedback'],fontsize='xx-large')
ax2.set_title('c', fontweight='bold')
# axis
#plt.axis([-1+0.2,3-0.2,-0.06,0.12])
plt.yticks(np.arange(-0.06,0.12+0.001,0.02),['' for n in range(len(np.arange(-0.06,0.12+0.001,0.02)))])
ax2.set_ylim(-0.06,0.12)
ax2.set_xlim(-0.5-0.01,3.5+0.01)
ax2.set_yticks(list(np.arange(-0.06,0.12+0.001,0.02)))
ax2.set_yticklabels(['','']+[''+str(n)+'' for n in list(np.round(np.arange(-0.06,0.12+0.001,0.02)*20.,1))[2:]],fontsize='xx-large')

plt.ylabel('Contribtions to $RF_{CO_2}$ in 2010 (W m$^{-2}$)',fontsize='xx-large')

#figure04
dty=dty = np.float32
mean_RF_CO2=1.789
std_RF_CO2=0.1*mean_RF_CO2

TMP= np.array([line for line in csv.reader(open('data/HistClim_HadCRUT4/#DATA.HistClim_HadCRUT4.1850-2014.gst.csv','r'))], dtype=dty)
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

for filename in os.listdir('results_EXP3/'):   
    if 'att' in filename:
        TMP=np.array([line for line in csv.reader(open('results_EXP3/'+filename,'r'))],dtype=dty)        
        if np.isnan(TMP[0,-1]):
            continue
        RF_CO2.append(TMP[0,:])
        filename_tmp='weight'+filename[11:]
        TMP=np.array([line for line in csv.reader(open('results_EXP3/'+filename_tmp,'r'))],dtype=dty)
        
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

wmean_RF_CO2_sum=np.nansum(np.sum(RF_CO2,1)*weight)/np.nansum(weight)
wstd_RF_CO2_sum=np.sqrt(np.nansum((np.sum(RF_CO2,1)-wmean_RF_CO2_sum)**2*weight)/np.nansum(weight))

tmp=wmean_RF_CO2[0]+wmean_RF_CO2[1]
wmean_RF_CO2=wmean_RF_CO2[1:]
wmean_RF_CO2[0]=tmp
tmp=np.sqrt(wstd_RF_CO2[0]**2+wstd_RF_CO2[1]**2)
wstd_RF_CO2=wstd_RF_CO2[1:]
wstd_RF_CO2[0]=tmp

##PLOT
ax3 = plt.subplot2grid((2,x),(1,colspan_ax2),colspan=x-colspan_ax2)
#ax3=plt.subplot()
            
plt.plot([-5,14],[0,0],'k-')
for n in range(len(wmean_RF_CO2)):
    if n<=0:
        continue
    plt.bar((RF_loc[n]-1)-1,wmean_RF_CO2[n],width=w,color=RF_color[n],yerr=wstd_RF_CO2[n],capsize=4,edgecolor='k',hatch='.....')
wstd_RF_CO2=np.array(wstd_RF_CO2)    
plt.bar(-1,cc_feedback-sum(wmean_RF_CO2[2:]),width=w,color='#FF0000',
        yerr=np.sqrt(cc_feedback_std**2-np.sum(wstd_RF_CO2[2:]**2)),capsize=4,edgecolor='k',hatch='.....')
plt.text(-1,cc_feedback-sum(wmean_RF_CO2[2:])+0.005,str(np.round((cc_feedback-sum(wmean_RF_CO2[2:]))*1000,1)),ha="right",va="bottom",fontsize="xx-large")
for n in range(len(wmean_RF_CO2)):
    if n<=0:
        continue
    sgn = np.sign(wmean_RF_CO2[n])
    txt = str(np.round(wmean_RF_CO2[n]*1000,1))
    if ((txt[0]!='-')&(len(txt)==3))|((txt[0]=='-')&(len(txt)==4)):
        txt += '0'
    if (txt[0]=='-'):
        txt = '$-$'+txt[1:]
    if sgn>0:
        plt.text((RF_loc[n]-1)-1+0.5,wmean_RF_CO2[n]+sgn*0.005,txt,ha="right",va="bottom",fontsize="xx-large")
    elif sgn<0:
        plt.text((RF_loc[n]-1)-1+0.5,wmean_RF_CO2[n]+sgn*0.005,txt,ha="right",va="top",fontsize="xx-large")
# axis
plt.xticks(np.arange(-1,11),RF_label,fontsize='xx-large',fontstretch='condensed')
plt.axis([-2+0.2,11-0.2,-0.15,0.22])
plt.yticks(np.arange(-0.15,0.22,0.05),fontsize='xx-large',alpha=0)
plt.xlim(-2+0.25,11)
ax32 = ax3.twinx()
ax32.set_ylim(-0.15,0.22)
ax32.set_yticks(np.arange(-0.15,0.22,0.05))
ax32.set_yticklabels(np.arange(-150,220,50),fontsize='xx-large')
ax32.set_title('d', fontweight='bold')
plt.yticks(fontsize='x-large')
#f.autofmt_xdate()
###########3
ax32.set_ylabel('$RF_{CO_2}$ in 2010 induced by\nclimate-carbon feedbacks (mW m$^{-2}$)',fontsize='xx-large')
f.autofmt_xdate()
plt.savefig('Figure20-test-new.pdf',dpi=600)