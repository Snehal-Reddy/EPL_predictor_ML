import numpy as np
import pandas as pd
from datetime import datetime as dt
import itertools

season_data_18 = pd.read_csv('E0.csv')
season_data_17 = pd.read_csv('E0(1).csv')
season_data_16 = pd.read_csv('E0(2).csv')
season_data_15 = pd.read_csv('E0(3).csv')
season_data_14 = pd.read_csv('E0(4).csv')
season_data_13 = pd.read_csv('E0(5).csv')
season_data_12 = pd.read_csv('E0(6).csv')
season_data_11 = pd.read_csv('E0(7).csv')
season_data_10 = pd.read_csv('E0(8).csv')
season_data_09 = pd.read_csv('E0(9).csv')
season_data_08 = pd.read_csv('E0(10).csv')
season_data_07 = pd.read_csv('E0(11).csv')
season_data_06 = pd.read_csv('E0(12).csv')
season_data_05 = pd.read_csv('E0(13).csv')
season_data_04 = pd.read_csv('E0(14).csv')
season_data_03 = pd.read_csv('E0(15).csv')
season_data_02 = pd.read_csv('E0(16).csv')
season_data_01 = pd.read_csv('E0(17).csv')

def parse_date(date):  
	if date == '':
    	return None
    else:
    	return dt.strptime(date, '%d/%m/%y').date()
    

def parse_date_other(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%d/%m/%Y').date()

season_data_01.Date = season_data_01.Date.apply(parse_date)    
season_data_02.Date = season_data_02.Date.apply(parse_date)    
season_data_03.Date = season_data_03.Date.apply(parse_date_other)         # The date format for this dataset is different  
season_data_04.Date = season_data_04.Date.apply(parse_date)    
season_data_05.Date = season_data_05.Date.apply(parse_date)    
season_data_06.Date = season_data_06.Date.apply(parse_date)    
season_data_07.Date = season_data_07.Date.apply(parse_date)    
season_data_08.Date = season_data_08.Date.apply(parse_date)    
season_data_09.Date = season_data_09.Date.apply(parse_date)    
season_data_10.Date = season_data_10.Date.apply(parse_date)
season_data_11.Date = season_data_11.Date.apply(parse_date)
season_data_12.Date = season_data_12.Date.apply(parse_date)
season_data_13.Date = season_data_13.Date.apply(parse_date)
season_data_14.Date = season_data_14.Date.apply(parse_date)
season_data_15.Date = season_data_15.Date.apply(parse_date)
season_data_16.Date = season_data_16.Date.apply(parse_date)
season_data_17.Date = season_data_17.Date.apply(parse_date)
season_data_18.Date = season_data_18.Date.apply(parse_date)

columns_req = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HST','AST','HC','AC']

season_stats_01 = season_data_01[columns_req]                      
season_stats_02 = season_data_02[columns_req]
season_stats_03 = season_data_03[columns_req]
season_stats_04 = season_data_04[columns_req]
season_stats_05 = season_data_05[columns_req]
season_stats_06 = season_data_06[columns_req]
season_stats_07 = season_data_07[columns_req]
season_stats_08 = season_data_08[columns_req]
season_stats_09 = season_data_09[columns_req]
season_stats_10 = season_data_10[columns_req]
season_stats_11 = season_data_11[columns_req]   
season_stats_12 = season_data_12[columns_req]
season_stats_13 = season_data_13[columns_req]
season_stats_14 = season_data_14[columns_req]
season_stats_15 = season_data_15[columns_req]
season_stats_16 = season_data_16[columns_req]
season_stats_17 = season_data_17[columns_req]
season_stats_18 = season_data_18[columns_req]

