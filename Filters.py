
import numpy as np

from scipy import ndimage,signal

#####################################
''' Image Processing Filters'''
#####################################

''' Mean trace removal'''

def mean_removal_func(window_Title,Data,dt,nrx,rx_component):
    print("Mean removal Started!")
    m_trace = np.mean(Data,1)
    mean_Mat = np.zeros((np.size(Data,0),np.size(Data,1)))
    
    for i in range(np.size(Data,1)):
        mean_Mat[:,i] = m_trace
    mean_Removed = Data-mean_Mat
    print("Mean removal Done!")
    return mean_Removed

'''Median trace removal'''

def median_removal_func(window_Title,Data,dt,nrx,rx_component):
    print("Median removal Started!")
    m_trace = np.median(Data,1)
    Median_mat = np.zeros((np.size(Data,0),np.size(Data,1)))
    for i in range(np.size(Data,1)):
        Median_mat[:,i] = m_trace
    median_Removed = Data-Median_mat
    print("Median removal Done!")
    return median_Removed


'''Field strength to Power dB'''

def field_to_Power_func(window_Title,Data,dt,nrx,rx_component,dx):
    V = pow((Data*dx),2) # Power in Volts^2
    L = 10*np.log10(V[np.nonzero(V)]) # power in dB
    # Correction for Zero rows in simulated Data Applied i.e trimmed Zero value rows as log10(0) = Inf
    f_Power = np.reshape(L,(int(np.size(L)/np.size(V,1)),np.size(V,1))) 
    print(np.min(f_Power),np.max(f_Power))
    return f_Power

'''Time inverse exponential gain'''
def time_gain_func(window_Title,Data,dt,nrx,rx_component,tpow):
    
    t = np.ones((np.size(Data,0),)) 
    for i in range(np.size(Data,0)):
        t[i] = (i+1) * dt * np.exp(tpow)
    time_trace = np.ones((np.size(Data,0),np.size(Data,1)))
    for i in range(np.size(Data,1)):
        time_trace[:,i] = t
    gain = Data*time_trace
#    print(np.min(gain),np.max(gain))
    print("Time gain successfully Applied!")
    return gain


'''Median Filter'''
def median_Filter_func(window_Title,Data,dt,nrx,rx_component,wins1,wins2):  
    median_filt_Data = ndimage.median_filter(Data,[wins1,wins2])              
    print("Median Filter successfully Applied!")
    return median_filt_Data

'''Gaussian Filter'''   
def gauss_Filter_func(window_Title,Data,dt,nrx,rx_component,sigma):
    gauss_filt_Data = ndimage.gaussian_filter(Data,sigma)         
    print("Gaussian Filter successfully Applied!")
    return gauss_filt_Data

#####################################
''' Signal Processing Filters'''
#####################################


def FIR_lp_func(window_Title,Data,dt,nrx,rx_component,numtaps,f,win):

    a = 1 # Default Value
    lp_Coeff = signal.firwin(numtaps,f,window = win)       
    FIR_lp_Data = signal.lfilter(lp_Coeff, a, Data, axis=1, zi=None)
        
    print("FIR lowpass Filter successfully Applied!")
    return FIR_lp_Data
    
def FIR_hp_func(window_Title,Data,dt,nrx,rx_component,numtaps,f,win):   

    a = 1 # Default Value
    hp_Coeff = signal.firwin(numtaps,f,window = win,pass_zero=False)       
    FIR_hp_Data = signal.lfilter(hp_Coeff, a, Data, axis=1, zi=None)
        
    print("FIR highpass Filter successfully Applied!")
    return FIR_hp_Data

def FIR_bp_func(window_Title,Data,dt,nrx,rx_component,numtaps,f1,f2,win):

    a = 1 # Default Value
    bp_Coeff = signal.firwin(numtaps,[f1,f2],pass_zero=False,window = win)       
    FIR_bp_Data = signal.lfilter(bp_Coeff, a, Data, axis=1, zi=None)
    print("FIR bandpass Filter successfully Applied!")
    return FIR_bp_Data

def FIR_bs_func(window_Title,Data,dt,nrx,rx_component,numtaps,f1,f2,win):
    
    a = 1 # Default Value
    bs_Coeff = signal.firwin(numtaps,[f1,f2],window = win)       
    FIR_bs_Data = signal.lfilter(bs_Coeff, a, Data, axis=1, zi=None)        
    print("FIR bandstop Filter successfully Applied!")
    return FIR_bs_Data


