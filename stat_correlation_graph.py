import pandas as pd
from scipy import stats
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, show

LEGAL_PLAYER_TYPE_VALUES = ["Batting", "Pitching"]
LEGAL_BATTING_POSITION_VALUES = ["ALL", "C", "1B", "2B", "SS", "3B", "OF"]
LEGAL_PITCHING_POSITION_VALUES = ["SP", "RP"]
BATTING_ADVANCED_VALUES = ["Name", "PA", "BB/K", "AVG", "OBP", "SLG", "OPS", "ISO", "Spd", "BABIP", "UBR", "wGDP", "wSB", "wRC", "wRAA", "wOBA", "wRC+"]
BATTING_STANDARD_VALUES = ["Name", "H", "HR", "R", "RBI", "BB", "SO", "SB", "CS"]
BATTING_MASTER_VALUES = ["Name", "H", "HR", "R", "RBI", "BB", "SO", "SB", "CS", "PA", "BB/K", "AVG", "OBP", "SLG", "OPS", "ISO", "Spd", "BABIP", "UBR", "wGDP", "wSB", "wRC", "wRAA", "wOBA", "wRC+"]
BATTING_CATEGORY_OPTIONS = ["H", "HR", "R", "RBI", "BB", "SO", "SB", "CS", "PA", "BB/K", "AVG", "OBP", "SLG", "OPS", "ISO", "Spd", "BABIP", "UBR", "wGDP", "wSB", "wRC", "wRAA", "wOBA", "wRC+"]
PITCHING_ADVANCED_VALUES = ["Name", "K/9", "BB/9", "K/BB", "HR/9", "AVG", "WHIP", "BABIP", "FIP", "E-F", "SIERA"]
PITCHING_STANDARD_VALUES = ["Name", "W", "L", "ERA", "CG", "ShO", "SV", "HLD", "BS", "IP", "R", "ER", "HR", "H", "BB", "SO"]
PITCHING_MASTER_VALUES = ["Name", "W", "L", "ERA", "CG", "ShO", "SV", "HLD", "BS", "IP", "R", "ER", "HR", "H", "BB", "SO", "K/9", "BB/9", "K/BB", "HR/9", "AVG", "WHIP", "BABIP", "FIP", "E-F", "SIERA"]
PITCHING_CATEGORY_OPTIONS = ["W", "L", "ERA", "CG", "ShO", "SV", "HLD", "BS", "IP", "R", "ER", "HR", "H", "BB", "SO", "K/9", "BB/9", "K/BB", "HR/9", "AVG", "WHIP", "BABIP", "FIP", "E-F", "SIERA"]

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

def plot_stats(player_data, x_value, y_value):
    source = ColumnDataSource(
        data=dict(
            name=player_data.index,
            cat1=[player_data[x_value][i] for i in player_data.index],
            cat2=[player_data[y_value][i] for i in player_data.index],
        )
    )

    slope, intercept, r_value, p_value, std_err = stats.linregress(player_data[x_value],player_data[y_value])
    line = slope*player_data[x_value]+intercept

    print(r_value)

    hover = HoverTool(tooltips=[("name", "@name"),(x_value, "@cat1"),(y_value, "@cat2")])

    p = figure(title="Fantasy Baseball", tools=[hover])
    p.plot_width = 1200
    p.xaxis.axis_label = x_value
    p.yaxis.axis_label = y_value

    p.circle('cat1', 'cat2', size=10, color="#4DDB94", source=source, fill_alpha=0.2)
    p.line(player_data[x_value], line, line_width=2)

    show(p)

year_entry = '2016'

player_type = get_input("Batting or Pitching?: ", LEGAL_PLAYER_TYPE_VALUES)

if player_type == 'Pitching':
    position_entry = get_input("Position (" + " ".join(LEGAL_PITCHING_POSITION_VALUES) + "): ", LEGAL_PITCHING_POSITION_VALUES)
    advanced = pd.read_csv('Data/' + position_entry + '_Advanced_' + year_entry + '.csv')
    standard = pd.read_csv('Data/' + position_entry + '_Standard_' + year_entry + '.csv')

    advanced = advanced[PITCHING_ADVANCED_VALUES]
    standard = standard[PITCHING_STANDARD_VALUES]
 
    master = pd.merge(advanced, standard, how='outer', on=['Name'])
    master = master[PITCHING_MASTER_VALUES]
    master = master.set_index(['Name'])

    print("Category Options (" + " ".join(PITCHING_CATEGORY_OPTIONS) + "):")
    cat1_entry = get_input("First Category: ", PITCHING_CATEGORY_OPTIONS)
    cat2_entry = get_input("Second Category: ", PITCHING_CATEGORY_OPTIONS)
else:

    position_entry = get_input("Position (" + " ".join(LEGAL_BATTING_POSITION_VALUES) + "): ", LEGAL_BATTING_POSITION_VALUES)
    advanced = pd.read_csv('Data/' + position_entry + '_Advanced_' + year_entry + '.csv')
    standard = pd.read_csv('Data/' + position_entry + '_Standard_' + year_entry + '.csv')

    advanced = advanced[BATTING_ADVANCED_VALUES]
    standard = standard[BATTING_STANDARD_VALUES]

    master = pd.merge(advanced, standard, how='outer', on=['Name'])
    master = master[BATTING_MASTER_VALUES]
    master = master.set_index(['Name'])

    print("Category Options (" + " ".join(BATTING_CATEGORY_OPTIONS) + "):")
    cat1_entry = get_input("First Category: ", BATTING_CATEGORY_OPTIONS)
    cat2_entry = get_input("Second Category: ", BATTING_CATEGORY_OPTIONS)

plot_stats(master,cat1_entry,cat2_entry)
