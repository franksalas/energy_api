
import requests
import pandas as pd
import matplotlib.pyplot as plt


def category(category_id,api_key):
    '''
    input: category_id,api_key
    return: dict of category
    '''
    url = 'http://api.eia.gov/category/'
    payload = {'api_key':api_key,
               'category_id':category_id}
    r = requests.get(url, params=payload)
    return r.json()


def series(series_id,api_key):
    '''input: series_id, api_key
    return: dic of series_id'''
    url = 'http://api.eia.gov/series/'
    payload = {'api_key':api_key,
               'series_id':series_id}
    r = requests.get(url, params=payload)
    return r.json()




def df_category(dic):
    '''create dataframe from category'''
    # if not null, create childcategories df
    if len(dic['category']['childcategories']) is not 0:
        data = dic['category']['childcategories']
        df = pd.DataFrame.from_dict(data)  
    # if not null, create childseries df
    elif len(dic['category']['childseries']) is not 0:
        data = dic['category']['childseries']
        df = pd.DataFrame.from_dict(data)
    
    # if not null, create parent_id
    if dic['category']['parent_category_id'] is not None:
        parent_id = dic['category']['parent_category_id']
        df['parent_category_id'] = parent_id    
    # create name of dataset column
    name = dic['category']['name']
    name = name.replace(" ", "_")
    df['dataset'] = name
    return df


def plot_series(dic):
    figs = (15,3)
    name = dic['series'][0]['name']
    units_desc = dic['series'][0]['units']
    units_short = dic['series'][0]['unitsshort']
    df = df_series(dic)
    ax =  df.plot(figsize=figs)
    ax.legend([units_short])
    ax.set_ylabel(units_desc)
    plt.title(name)
    #return df



def df_series(dic):
    '''input" dict
    output: dataframe
    convert dictionary data into dataframe'''
    # if statement to convert date
    if dic['series'][0]['f'] == 'M':
        #201002
        fmat = '%Y%m'
    else:
        fmat= None
    # select data
    plot_data = dic['series'][0]['data']
    # create dataframe
    df = pd.DataFrame.from_dict(plot_data)
    # rename cols
    df.rename(columns={0: 'date',1: 'value',}, 
              inplace=True)
    # change to datetime index
    df.date = pd.to_datetime(df['date'],format=fmat)
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df


def df_series_all(dic):
    '''input" dict
    output: dataframe
    convert dictionary data into dataframe'''
    # if statement to convert date
    name = dic['series'][0]['series_id']
    if dic['series'][0]['f'] == 'M':
        #201002
        fmat = '%Y%m'
    else:
        fmat= None
    # select data
    plot_data = dic['series'][0]['data']
    # create dataframe
    df = pd.DataFrame.from_dict(plot_data)
    # rename cols
    df.rename(columns={0: 'date',1: name,}, 
              inplace=True)
    # change to datetime index
    df.date = pd.to_datetime(df['date'],format=fmat)
    #df.set_index('date', inplace=True)
    return df



def data_frame_name(dic):
    '''convert dictionary data into dataframe'''
    # if statement to convert date
    if dic['series'][0]['f'] == 'M':
        #201002
        fmat = '%Y%m'
    else:
        fmat= None
    # select data
    name =  dic['series'][0]['series_id']
    plot_data = dic['series'][0]['data']
    # create dataframe
    df = pd.DataFrame.from_dict(plot_data)
    # rename cols
    df.rename(columns={0: 'date',1: name,}, 
              inplace=True)
    # change to datetime index
    df.date = pd.to_datetime(df['date'],format=fmat)
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df

def series_to_df(series_id,api_key):
    '''combine two function to return
    data from api call'''
    json_data = series(series_id,api_key)
    name = json_data['series'][0]['name']
    df = data_frame_name(json_data)
    return df



def mul_frames(ser_list,api_key):
    '''input list of series
    output: dataframe with data'''
    
    series_list = []
    for i in ser_list:
        ser_data = series(i,api_key)
        series_list.append(ser_data)
    
    frames = []
    for j in series_list:
        data = df_series_all(j)
        frames.append(data)
    # concat frames
    df  = pd.concat(frames, axis=1, sort=False)
    # drop duplicate date columns
    df = df.T.drop_duplicates().T
    # convert to datetime,axis,and drop date col
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(df['date'],inplace=True)
    df.drop(['date'],axis=1,inplace=True)
    df.sort_index(inplace=True)
    return df