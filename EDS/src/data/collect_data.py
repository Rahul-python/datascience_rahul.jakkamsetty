# -*- coding: utf-8 -*-
"""
@Rahul Jakkamsetty 414534

"""
import subprocess # for accessing command prompt
import os # for accessing os operations
import pandas as pd # importing pandas library



import requests;import json# for webscraping

def get_john_hopkins():
    """
    access john_hopkins git file using git commands and store the data ito a csv file.

    Returns a csv file with coronavirus numbers data from johnhopkins data base.
    -------
    None.

    """
    git_get=subprocess.Popen(['git','pull'], cwd=os.path.dirname(r'data/raw/COVID-19'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # runs the git pull command to get git file from JH database.
    (out,error)=git_get.communicate() #store output and errors when the above command is executed.
    print("Error:"+str(error),'\n','out:'+str(out))
def get_current_data_germany():
    """
    To get Germany Coronivirus data using API.
    Data is collected from RobertKoch Institut.
    Scrapes RKi Website.

    Returns Panda DataFrame with Coronovirus numbers of Germany.
    -------
    None.

    """
    data=requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')#accessing the RKI website.
    json_object=json.loads(data.content) # obtaining json data from the webpage.
    full_list=[]
    for pos,each_dict in enumerate (json_object['features'][:]): # looping through the 'features' attribute to get our numbers
        full_list.append(each_dict['attributes']) # appending to emptylist to save the data.

    pd_full_list=pd.DataFrame(full_list)
    try:
        pd_full_list.to_csv('data/raw/NPGEO/GER_state_data.csv',sep=';') 
    except FileNotFoundError:
        os.mkdir('data/raw/NPGEO')
        pd_full_list.to_csv('data/raw/NPGEO/GER_state_data.csv',sep=';')
        print ('Directory NPGEO created.')
    print(' Number of regions rows: '+str(pd_full_list.shape[0]))

if __name__ == '__main__':
    get_john_hopkins()
    get_current_data_germany()