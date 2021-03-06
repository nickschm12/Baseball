from YHandler import YHandler, YQuery
from xmljson import badgerfish as xj
import xml.etree.ElementTree as ET
import requests
import json
import sys
import csv

handler = YHandler()
query = YQuery(handler, 'mlb')

valid_years = ['2010','2011','2012','2013','2014','2015','2016','2017']
valid_weeks = ['All','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22']
categories = ['Team', 'R', 'H', 'HR', 'RBI', 'SB', 'AVG', 'OPS', 'IP', 'W', 'L', 'SV', 'K', 'HLD', 'ERA', 'WHIP']

def get_input(prompt,valid_args):
    while True:
        try:
            value = raw_input(prompt)
        except ValueError:
            print("Can't handle that kind of input, try again.")
            continue
        if value not in valid_args:
            print("Invalid input, try again.")
            continue
        else:
            break
    return value

def write_row(league,team_id,week,writer):
	team_csv_line = []
	if week == 'All':
		resp = handler.api_req(str.format('team/{0}.t.{1}/stats', league['league_key'], team_id))
	else:
		resp = handler.api_req(str.format('team/{0}.t.{1}/stats;type=week;week={2}', league['league_key'], team_id, week))
				
	xml_to_json = json.dumps(xj.data(ET.fromstring(resp.content)))
	parsed_json = json.loads(xml_to_json)

	fantasy_content = parsed_json["{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}fantasy_content"]
	team = fantasy_content['{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}team']
	team_stats = team['{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}team_stats']
	stats = team_stats['{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}stats']
	stat = stats['{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}stat']
    
	team_csv_line.append(team['{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}name']["$"])
    
	for i in stat:
		if i['{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}stat_id']["$"] != 60:
			team_csv_line.append(i['{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}value']["$"])

	writer.writerow(team_csv_line)

season = get_input("Which season? (" + " ".join(valid_years) + "): ",valid_years)
week = get_input("Which week? (" + " ".join(valid_weeks) + "): ",valid_weeks)

if week == 'All':
	path = "Data/team_stats_" + season + ".csv"
else:
	path = "Data/team_stats_" + season + '_week_' + week + ".csv"


writer = csv.writer(open(path,"w"), delimiter=',')

leagues = query.get_user_leagues()

league = ''
team_ids = []

for l in leagues:
    if "WWP Keeper Leagues Year" in l['name'] and l['season'] == season:
        league = l
        if league['season'] <= '2010' :
        	team_ids = [1,2,3,4,5,6,7]
        elif league['season'] > '2010' and league['season'] <= '2013':
        	team_ids = [1,2,3,4,5,6,7,8,9,10]
        else:
        	team_ids = [1,2,3,4,5,6,7,8,9,10,11,12]

if league == '':
    print "No league was found!"
    sys.exit(0)

writer.writerow(categories)

for team_id in team_ids:
	write_row(league,team_id,week,writer)

print "Output: " + path

