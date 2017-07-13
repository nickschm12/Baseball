import pandas as pd
from scipy import stats

batting_cats = ['R','H','HR','RBI','SB','AVG','OPS']
pitching_cats = ['W','L','SV','K','HLD','ERA','WHIP']
batting_ranks = ['R_Rank','H_Rank','HR_Rank','RBI_Rank','SB_Rank','AVG_Rank','OPS_Rank']
pitching_ranks = ['W_Rank','L_Rank','SV_Rank','K_Rank','HLD_Rank','ERA_Rank','WHIP_Rank']
valid_years = ['2010','2011','2012','2013','2014','2015','2016','2017']
valid_weeks = ['All','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22']

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

season = get_input("Which season? (" + " ".join(valid_years) + "): ",valid_years)
week = get_input("Which week? (" + " ".join(valid_weeks) + "): ",valid_weeks)

if week == 'All':
	input_path = "Data/team_stats_" + season + ".csv"
	output_path = "Data/Roto_Standings_" + season + ".csv";
else:
	input_path = "Data/team_stats_" + season + '_week_' + week + ".csv"
	output_path = "Data/Roto_Standings_" + season + '_week_' + week + ".csv"
	
team_stats = pd.read_csv(input_path)
team_stats = team_stats.set_index(['Team'])

stats_df = pd.DataFrame(team_stats)
ranks_df = pd.DataFrame(team_stats.index)

for cat in batting_cats:
	key = cat + "_Rank"
	stats_df[key] = stats_df[cat].rank()

for cat in pitching_cats:
	key = cat + "_Rank"
	if cat in ['L','ERA','WHIP']:
		stats_df[key] = stats_df[cat].rank(ascending=False)
	else:
		stats_df[key] = stats_df[cat].rank()
	
stats_df['Batting Total Rank'] = stats_df[batting_ranks].sum(axis=1)
stats_df['Pitching Total Rank'] = stats_df[pitching_ranks].sum(axis=1)
stats_df['Total Rank'] = stats_df[['Batting Total Rank','Pitching Total Rank']].sum(axis=1)

final_df = stats_df[['R','H','HR','RBI','SB','AVG','OPS','Batting Total Rank','W','L','SV','K','HLD','ERA','WHIP','Pitching Total Rank','Total Rank']]
final_df = final_df.sort_values(['Total Rank'],ascending=[0])
final_df.to_csv(output_path, sep=',')
print final_df