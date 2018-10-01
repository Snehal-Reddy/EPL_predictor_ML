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
	#print(date,type(date))  
	if date == '' or type(date) != str :
		return None
	else:
		return dt.strptime((date), '%d/%m/%y').date()
	

def parse_date_other(date):
	if date == '':
		return None
	else:
		return dt.strptime((date), '%d/%m/%Y').date()

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

def create_team_dict(season_stats):
	teams = {}
	for i in season_stats.groupby('HomeTeam').mean().T.columns:
		teams[i] = []
	return teams

def goals_scored_till_matchweek(season_stats):
	teams = create_team_dict(season_stats)
	print(len(season_stats))
	for i in range(len(season_stats)):
		teams[season_stats.iloc[i].HomeTeam].append(season_stats.iloc[i].FTHG)
		teams[season_stats.iloc[i].AwayTeam].append(season_stats.iloc[i].FTAG)

	Cumu_scored_till_matchweek = pd.DataFrame(data = teams, index = [i for i in range(1,39)]).T
	Cumu_scored_till_matchweek[0] = 0
	for i in range(2,39):
		Cumu_scored_till_matchweek[i] = Cumu_scored_till_matchweek[i] + Cumu_scored_till_matchweek[i-1]
	return Cumu_scored_till_matchweek

def goals_conceded_till_matchweek(season_stats):
	teams = create_team_dict(season_stats)
	for i in range(len(season_stats)):
		teams[season_stats.iloc[i].HomeTeam].append(season_stats.iloc[i].FTAG)
		teams[season_stats.iloc[i].AwayTeam].append(season_stats.iloc[i].FTHG)

	Cumu_conceded_till_matchweek = pd.DataFrame(data = teams, index = [i for i in range(1,39)]).T
	Cumu_conceded_till_matchweek[0] = 0
	for i in range(2,39):
		Cumu_conceded_till_matchweek[i] = Cumu_conceded_till_matchweek[i] + Cumu_conceded_till_matchweek[i-1]
	return Cumu_conceded_till_matchweek

def update_sheet (season_stats):
	scored = goals_scored_till_matchweek(season_stats)
	conceded = goals_conceded_till_matchweek(season_stats)
	row = 0
	HTGS = []
	HTGC = []
	ATGS = []
	ATGC = []

	for i in range(380):
		HTGS.append(scored.loc[season_stats.iloc[i].HomeTeam][row])
		HTGC.append(conceded.loc[season_stats.iloc[i].HomeTeam][row])
		ATGS.append(scored.loc[season_stats.iloc[i].AwayTeam][row])
		ATGC.append(conceded.loc[season_stats.iloc[i].AwayTeam][row])

		if ( (i+1)%10 == 0 ):
			row+=1

	season_stats['HTGS'] = HTGS
	season_stats['ATGS'] = ATGS
	season_stats['HTGC'] = HTGC
	season_stats['ATGC'] = ATGC

	return season_stats

season_data_18 = update_sheet(season_data_18)
season_data_17 = update_sheet(season_data_17)
season_data_16 = update_sheet(season_data_16)
season_data_15 = update_sheet(season_data_15)
season_data_14 = update_sheet(season_data_14)
season_data_13 = update_sheet(season_data_13)
season_data_12 = update_sheet(season_data_12)
season_data_11 = update_sheet(season_data_11)
season_data_10 = update_sheet(season_data_10)
season_data_09 = update_sheet(season_data_09)
season_data_08 = update_sheet(season_data_08)
season_data_07 = update_sheet(season_data_07)
season_data_06 = update_sheet(season_data_06)
season_data_05 = update_sheet(season_data_05)
season_data_04 = update_sheet(season_data_04)
season_data_03 = update_sheet(season_data_03)
season_data_02 = update_sheet(season_data_02)
season_data_01 = update_sheet(season_data_01)