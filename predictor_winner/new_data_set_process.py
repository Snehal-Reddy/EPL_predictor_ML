import numpy as np
import math
import pandas as pd
from datetime import datetime as dt
import itertools

number_of_teams = 0

season_data_18 = pd.read_csv('../data_season_wise/E0.csv')
season_data_17 = pd.read_csv('../data_season_wise/E0(1).csv')
season_data_16 = pd.read_csv('../data_season_wise/E0(2).csv')
season_data_15 = pd.read_csv('../data_season_wise/E0(3).csv')
season_data_14 = pd.read_csv('../data_season_wise/E0(4).csv')
season_data_13 = pd.read_csv('../data_season_wise/E0(5).csv')
season_data_12 = pd.read_csv('../data_season_wise/E0(6).csv')
season_data_11 = pd.read_csv('../data_season_wise/E0(7).csv')
season_data_10 = pd.read_csv('../data_season_wise/E0(8).csv')
season_data_09 = pd.read_csv('../data_season_wise/E0(9).csv')
season_data_08 = pd.read_csv('../data_season_wise/E0(10).csv')
season_data_07 = pd.read_csv('../data_season_wise/E0(11).csv')
season_data_06 = pd.read_csv('../data_season_wise/E0(12).csv')
season_data_05 = pd.read_csv('../data_season_wise/E0(13).csv')
season_data_04 = pd.read_csv('../data_season_wise/E0(14).csv')
season_data_03 = pd.read_csv('../data_season_wise/E0(15).csv')
season_data_02 = pd.read_csv('../data_season_wise/E0(16).csv')
season_data_01 = pd.read_csv('../data_season_wise/E0(17).csv')

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

concat_stat = pd.concat([season_data_01,season_data_02,season_data_03,season_data_04,season_data_05,season_data_06,season_data_07,season_data_08,season_data_09,season_data_10,season_data_11,season_data_12,season_data_13,season_data_14,season_data_15,season_data_16,season_data_17,season_data_18] ,ignore_index=True)

def create_team_dict(season_stats):
	teams = {}
	for i in season_stats.groupby('HomeTeam').mean().T.columns:
		teams[i] = []
	return teams

def goals_scored_till_matchweek(season_stats):
	teams = {}
	global number_of_teams

	for i in season_stats.groupby('HomeTeam').mean().T.columns:
		teams[i] = np.zeros(shape = 684)
	#print(len(season_stats))
	number_of_teams = len(teams)
	for i in range(len(season_stats)):
		teams[season_stats.iloc[i].HomeTeam][i/10] = (season_stats.iloc[i].FTHG)
		teams[season_stats.iloc[i].AwayTeam][i/10] = (season_stats.iloc[i].FTAG)

	Cumu_scored_till_matchweek = pd.DataFrame(data = teams, index = [i for i in range(1,685)]).T
	Cumu_scored_till_matchweek[0] = 0
	Cumu_scored_till_matchweek[2] = Cumu_scored_till_matchweek[1]
	Cumu_scored_till_matchweek[1] = 0
	for i in range(3,685):
		Cumu_scored_till_matchweek[i] = Cumu_scored_till_matchweek[i-1] + Cumu_scored_till_matchweek[i-2]
	return Cumu_scored_till_matchweek

def goals_conceded_till_matchweek(season_stats):
	teams = {}
	for i in season_stats.groupby('HomeTeam').mean().T.columns:
		teams[i] = np.zeros(shape = 684)
	for i in range(len(season_stats)):
		teams[season_stats.iloc[i].HomeTeam][i/10] = (season_stats.iloc[i].FTAG)
		teams[season_stats.iloc[i].AwayTeam][i/10] = (season_stats.iloc[i].FTHG)

	Cumu_conceded_till_matchweek = pd.DataFrame(data = teams, index = [i for i in range(1,685)]).T
	Cumu_conceded_till_matchweek[0] = 0
	Cumu_conceded_till_matchweek[2] = Cumu_conceded_till_matchweek[1]
	Cumu_conceded_till_matchweek[1] = 0
	for i in range(3,685):
		Cumu_conceded_till_matchweek[i] = Cumu_conceded_till_matchweek[i-2] + Cumu_conceded_till_matchweek[i-1]
	return Cumu_conceded_till_matchweek

def apply_map(result):
	if result == 'W':
		return 3
	elif result == 'D':
		return 1
	else:
		return 0

def team_result(season_stats):
	#teams =  create_team_dict(season_stats)
	teams = {}
	for i in season_stats.groupby('HomeTeam').mean().T.columns:
		teams[i] = ['D']*684
	for i in range(len(season_stats)):
		if season_stats.iloc[i].FTR == 'H':
			teams[season_stats.iloc[i].HomeTeam][i/10]='W'
			teams[season_stats.iloc[i].AwayTeam][i/10]='L'
		elif season_stats.iloc[i].FTR == 'A':
			teams[season_stats.iloc[i].HomeTeam][i/10]='L'
			teams[season_stats.iloc[i].AwayTeam][i/10]='W'
		else:
			teams[season_stats.iloc[i].HomeTeam][i/10]='D'
			teams[season_stats.iloc[i].AwayTeam][i/10]='D'

	return pd.DataFrame(data = teams, index = [i for i in range(1,685)]).T

def points_till_matchweek(matchres):
	matchres_points = matchres.applymap(apply_map)
	matchres_points[2] = matchres_points[1]
	matchres_points[1] = 1
	matchres
	for i in range(3,685):
		matchres_points[i] = matchres_points[i-1] + matchres_points[i-2]
	#print(season_point_stats)
	matchres_points.insert(column = 0, loc = 0, value = [0*i for i in range(number_of_teams)])
	#print("new")
	#print(season_point_stats)
	return matchres_points

def update_sheet (season_stats):
	scored = goals_scored_till_matchweek(season_stats)
	conceded = goals_conceded_till_matchweek(season_stats)
	points_so_far = points_till_matchweek(team_result(season_stats))
	row = 0
	HTGS = []
	HTGC = []
	ATGS = []
	ATGC = []
	HTP = []
	ATP = []
	MW = []

	for i in range(6840):
		HTGS.append(scored.loc[season_stats.iloc[i].HomeTeam][row])
		HTGC.append(conceded.loc[season_stats.iloc[i].HomeTeam][row])
		ATGS.append(scored.loc[season_stats.iloc[i].AwayTeam][row])
		ATGC.append(conceded.loc[season_stats.iloc[i].AwayTeam][row])
		HTP.append(points_so_far.loc[season_stats.iloc[i].HomeTeam][row])
		ATP.append(points_so_far.loc[season_stats.iloc[i].AwayTeam][row])
		MW.append(row)
		if ( (i+1)%10 == 0 ):
			row+=1

	season_stats['HTGS'] = HTGS
	season_stats['ATGS'] = ATGS
	season_stats['HTGC'] = HTGC
	season_stats['ATGC'] = ATGC
	season_stats['HTP'] = HTP
	season_stats['ATP'] = ATP
	#season_stats['MW'] = MW

	return season_stats

concat_stat = update_sheet(concat_stat)

def get_form(playing_stat,num):
	form = team_result(playing_stat)
	form_final = form.copy()
	for i in range(num+1,685):
		form_final[i] = ''
		j = 1
		while j < num+1:
			#print(form[i])
			#print(type(form[i]))
			form_final[i] += form[i-j]
			j += 1           
	return form_final

def add_prev_match_results(playing_stat,num):
	form = get_form(playing_stat,num)  
	h = ['M' for i in range(num * 10)]  # since form is not available for n MW (n*10)
	a = ['M' for i in range(num * 10)]
	#print(num)
	#print(form)
	j = num+1
	for i in range((num*10),6840):
		ht = playing_stat.iloc[i].HomeTeam
		at = playing_stat.iloc[i].AwayTeam

		past = form.loc[ht][j]  
		#print(len(past))						 #get past num results
		h.append(past[num-1])                    #numth recent result
		
		#print(past)
		#print(past[num-1])

		past = form.loc[at][j]               # get past num results.
		a.append(past[num-1])                # numth previous match
		
		if ((i + 1)% 10) == 0:
			j = j + 1

	#print(h)
	playing_stat['HM' + str(num)] = h                 
	playing_stat['AM' + str(num)] = a

	#print('new')
	print(num)
	return playing_stat


def add_prev_match_results_df(season_stats):
	season_stats = add_prev_match_results(season_stats,1)
	season_stats = add_prev_match_results(season_stats,2)
	season_stats = add_prev_match_results(season_stats,3)
	season_stats = add_prev_match_results(season_stats,4)
	season_stats = add_prev_match_results(season_stats,5)
	return season_stats  

concat_stat = add_prev_match_results_df(concat_stat)

previous_years_standings = pd.read_csv('../predictor_match/final_dataset.csv')

def get_previous_year_standings (season_stats):
	global previous_years_standings
	DiffLP = []
	
	for i in range(380*18):
		DiffLP.append(previous_years_standings.iloc[i].DiffLP)

	season_stats['DiffLP'] = DiffLP

	return season_stats

concat_stat = get_previous_year_standings(concat_stat)
def get_form_points(string):
	sum = 0
	for letter in string:
		sum += apply_map(letter)
	return sum

concat_stat['HTFormStr'] = concat_stat['HM1'] + concat_stat['HM2'] + concat_stat['HM3'] + concat_stat['HM4'] + concat_stat['HM5']
concat_stat['ATFormStr'] = concat_stat['AM1'] + concat_stat['AM2'] + concat_stat['AM3'] + concat_stat['AM4'] + concat_stat['AM5']

concat_stat['HTFormPts'] = concat_stat['HTFormStr'].apply(get_form_points)
concat_stat['ATFormPts'] = concat_stat['ATFormStr'].apply(get_form_points)

def get_3game_ws(string):
	if string[-3:] == 'WWW':
		return 1
	else:
		return 0
	
def get_5game_ws(string):
	if string == 'WWWWW':
		return 1
	else:
		return 0
	
def get_3game_ls(string):
	if string[-3:] == 'LLL':
		return 1
	else:
		return 0
	
def get_5game_ls(string):
	if string == 'LLLLL':
		return 1
	else:
		return 0
	
concat_stat['HTWinStreak3'] = concat_stat['HTFormStr'].apply(get_3game_ws)
concat_stat['HTWinStreak5'] = concat_stat['HTFormStr'].apply(get_5game_ws)
concat_stat['HTLossStreak3'] = concat_stat['HTFormStr'].apply(get_3game_ls)
concat_stat['HTLossStreak5'] = concat_stat['HTFormStr'].apply(get_5game_ls)

concat_stat['ATWinStreak3'] = concat_stat['ATFormStr'].apply(get_3game_ws)
concat_stat['ATWinStreak5'] = concat_stat['ATFormStr'].apply(get_5game_ws)
concat_stat['ATLossStreak3'] = concat_stat['ATFormStr'].apply(get_3game_ls)
concat_stat['ATLossStreak5'] = concat_stat['ATFormStr'].apply(get_5game_ls)

concat_stat['DiffPts'] = concat_stat['HTP'] - concat_stat['ATP']
concat_stat['DiffFormPts'] = concat_stat['HTFormPts'] - concat_stat['ATFormPts']

def average_per_MW (season_stats):
	teams = {}
	for i in season_stats.groupby('HomeTeam').mean().T.columns:
		teams[i] = 0


	for i in range(6840):
		if not (teams[season_stats.iloc[i].HomeTeam] == 0):	
			season_stats.iloc[i].HTGS/=teams[season_stats.iloc[i].HomeTeam]								
			season_stats.iloc[i].HTGC/=teams[season_stats.iloc[i].HomeTeam]	
			season_stats.iloc[i].HTP/=teams[season_stats.iloc[i].HomeTeam]	

		if (not(teams[season_stats.iloc[i].AwayTeam] == 0)):
			season_stats.iloc[i].ATGS/=teams[season_stats.iloc[i].AwayTeam]
			season_stats.iloc[i].ATGC/=teams[season_stats.iloc[i].AwayTeam]	
			season_stats.iloc[i].ATP/=teams[season_stats.iloc[i].AwayTeam]

		teams[season_stats.iloc[i].HomeTeam]+=1
		teams[season_stats.iloc[i].AwayTeam]+=1

	return season_stats

concat_stat = average_per_MW(concat_stat)

concat_stat.replace([np.inf, -np.inf], np.nan)
concat_stat.fillna(concat_stat.mean())
#concat_stat.replace([np.inf, -np.inf], np.).dropna(axis = 1, how = 'all')
concat_stat.to_csv("new_final_dataset.csv")
