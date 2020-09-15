# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 23:37:27 2020

@author: Rahul Jakkamsetty
"""

import pandas as pd
import numpy as np

from scipy import optimize
from scipy import integrate

import matplotlib.pyplot as plt


pd.set_option('display.max_rows', 500)
def SIR_parameters_opt_static(ydata,t):
    '''
    Static parameter modelling of SIR simulation. beta is assumed constant i.e no effect of measure taken by respective governemnts of the countries.

    Parameters
    ----------
    ydata : array or list or dataframe column. 
        DESCRIPTION: The daily cases of all the countries for which we are trying to fit a curve.

    Returns curve parameters beta and gamma. 
    -------
    None.

    '''
    

    try:
        popt, pcov = optimize.curve_fit(fit_odeint, t, ydata)
    except RuntimeError:
        print('More iterations required. Trying with new value.')
        popt, pcov = optimize.curve_fit(fit_odeint, t, ydata,maxfev=15000)
    fitted=fit_odeint(t,*popt)
    return fitted
        
    
def SIR_model_fit(SIR, time, beta, gamma):
    '''
    Simple SIR model implementation.
    S: Suspected population
    I: Infected population
    R: Recovered population
    beta: rate of infection
    gamma: rate of recovery
    time: for integral as define in odeint function of scipy.integrate
    as per slides: ds+dI+dR = 0 and S+R+I=N (total population)

    Make a note tht in this model a recovered person can not get infected again.
    '''

    S,I,R = SIR
    dS_dt = -beta*S*I/N0
    dI_dt = beta*S*I/N0 - gamma*I
    dR_dt = gamma*I

    return dS_dt, dI_dt, dR_dt
def fit_odeint(x, beta, gamma):
    ''' To call integrate funtion of scipy'''
    return integrate.odeint(SIR_model_fit, (S0, I0, R0), t, args=(beta, gamma))[:,1]  #we are only fetching dI
if __name__=='__main__':
    print('Modelling with SIR...')
    N0 = 5000000
    I0 = 20   #Infected population
    S0 = N0 - I0    #Suspected population
    R0 = 0          #Recovered population
    beta = 0.4      #Rate of infection
    gamma = 0.1     #Rate of recovery
    SIR_df=pd.DataFrame()
    total_data=pd.read_csv('data/processed/COVID_total_flat_table.csv',sep=';')
    total_data=total_data.sort_values('date',ascending=True)
    country_only=total_data.drop(['date'],axis=1)
    for each in country_only:
        ydata=np.array(country_only[each][35:100])
        t=np.arange(len(ydata))
        fitted=SIR_parameters_opt_static(ydata,t)
        SIR_df[each]=fitted
    SIR_df.to_csv('data/processed/SIR_fitted_parameters.csv', sep=';',index=False)
    print('Total Entries:',SIR_df.shape[0])

