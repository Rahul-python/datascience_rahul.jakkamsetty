# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 00:44:07 2020

@author: Rahul Jakkamsetty
"""

import pandas as pd 

#from datetime import datetime #datetime library to convert the date from string to datetime object.

def store_relational_data_JH():
    '''
    Converts the COVID data from JH data base to relational data set.

    Returns a relational data set in a csv file.
    -------
    None.

    '''
    data_path='data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    jh_raw=pd.read_csv(data_path)
    jh_data_bs=jh_raw.rename(columns={'Country/Region':'country','Province/State': 'state'}) # rename the country and state for comfort.
    jh_data_bs['state']=jh_data_bs['state'].fillna('no')
    jh_data_bs=jh_data_bs.drop(columns=["Lat","Long"]) # dropping latitude and longitude columns
    jh_test_data=jh_data_bs.set_index(['state','country']).T 
    jh_rel_data=jh_test_data.stack(level=(0,1)).reset_index().rename(columns={'level_0':'date',0:'confirmed'}) #resetting the index and renaimg the numbered columns
    jh_rel_data['date']=jh_rel_data.date.astype('datetime64[ns]') #convert the date to date datatype
    jh_rel_data.to_csv('data/processed/COVID_relational_confirmed.csv',sep=';',index=False)
    print(' Number of rows stored: '+str(jh_rel_data.shape[0]))
    print(' Latest date is: '+str(max(jh_rel_data.date)))
if __name__ == '__main__':

    store_relational_data_JH()
          