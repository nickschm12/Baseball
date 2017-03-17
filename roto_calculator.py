import pandas as pd
from scipy import stats

batting_cats = ['R','H','HR','RBI','SB','AVG','OPS']
pitching_cats = ['W','L','SV','K','HLD','ERA','WHIP']
batting_ranks = ['R_Rank','H_Rank','HR_Rank','RBI_Rank','SB_Rank','AVG_Rank','OPS_Rank']
pitching_ranks = ['W_Rank','L_Rank','SV_Rank','K_Rank','HLD_Rank','ERA_Rank','WHIP_Rank']
valid_years = ['2010','2011','2012','2013','2014','2015','2016','2017']

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

team_stats = pd.read_csv('team_stats_' + season + '.csv')
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
	
stats_df['Batting_Total_Rank'] = stats_df[batting_ranks].sum(axis=1)
stats_df['Pitching_Total_Rank'] = stats_df[pitching_ranks].sum(axis=1)
stats_df['Total_Rank'] = stats_df[['Batting_Total_Rank','Pitching_Total_Rank']].sum(axis=1)

stats_df[['Batting_Total_Rank','Pitching_Total_Rank','Total_Rank']].sort(['Total_Rank'],ascending=[0]).to_csv("Roto_Standings_" + season + ".csv", sep=',')