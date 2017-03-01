import pandas as pd
from scipy import stats
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, show

def legal_player_type_values():
    return ["Batting", "Pitching"]

def legal_batting_position_values():
    return ["ALL", "C", "1B", "2B", "SS", "3B", "OF"]

def legal_pitching_position_values():
    return ["SP", "RP"]

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

year_entry = '2016'

player_type = get_input("Batting or Pitching?: ", legal_player_type_values())

if player_type == 'Pitching':
    position_entry = get_input("Position (ALL SP RP): ", legal_pitching_position_values())
    advanced = pd.read_csv('/Users/nschmidt/workspace/baseball/Data/' + position_entry + '_Advanced_' + year_entry + '.csv')
    standard = pd.read_csv('/Users/nschmidt/workspace/baseball/Data/' + position_entry + '_Standard_' + year_entry + '.csv')

    advanced = advanced[["Name","Team","K/9","BB/9","K/BB","HR/9","AVG","WHIP","BABIP","FIP","E-F","SIERA"]]
    standard = standard[["Name","W","L","ERA","CG","ShO","SV","HLD","BS","IP","R","ER","HR","H","BB","SO"]]
 
    master = pd.merge(advanced, standard, how='outer', on=['Name'])
    master = master[["Name","Team","K/9","BB/9","K/BB","HR/9","AVG","WHIP","BABIP","FIP","E-F","SIERA","W","L","ERA","CG","ShO","SV","HLD","BS","IP","R","ER","HR","H","BB","SO"]]
    master = master.set_index(['Name'])

    print("Category Options: W L ERA CG ShO SV HLD BS IP R ER HR H BB SO K/9 BB/9 K/BB HR/9 AVG WHIP BABIP FIP E-F SIERA")
else:
    position_entry = get_input("Position (ALL C 1B 2B SS 3B OF): ", legal_batting_position_values())
    advanced = pd.read_csv('/Users/nschmidt/workspace/baseball/Data/' + position_entry + '_Advanced_' + year_entry + '.csv')
    standard = pd.read_csv('/Users/nschmidt/workspace/baseball/Data/' + position_entry + '_Standard_' + year_entry + '.csv')

    advanced = advanced[["Name","Team","PA","BB/K","AVG","OBP","SLG","OPS","ISO","Spd","BABIP","UBR","wGDP","wSB","wRC","wRAA","wOBA","wRC+"]]
    standard = standard[["Name", "H", "BB", "HR", "R", "RBI", "SO", "SB", "CS"]]

    master = pd.merge(advanced, standard, how='outer', on=['Name'])
    master = master[["Name","Team", "H", "HR", "R", "RBI", "BB", "SO", "SB", "CS", "PA","BB/K","AVG","OBP","SLG","OPS","ISO","Spd","BABIP","UBR","wGDP","wSB","wRC","wRAA","wOBA","wRC+"]]
    master = master.set_index(['Name'])

    print("Category Options: H HR R RBI BB SO SB CS PA BB/K AVG OBP SLG OPS ISO Spd BABIP UBR wGDP wSB wRC wRAA wOBA wRC+")

cat1_entry = raw_input("First Category: ")
cat2_entry = raw_input("Second Category: ")

cat1_array = master[cat1_entry]
cat2_array = master[cat2_entry]

source = ColumnDataSource(
    data=dict(
        name=master.index,
        cat1=[cat1_array[i] for i in master.index],
        cat2=[cat2_array[i] for i in master.index],
    )
)

def plot_stats():
    slope, intercept, r_value, p_value, std_err = stats.linregress(cat1_array,cat2_array)
    line = slope*cat1_array+intercept

    print(r_value)

    hover = HoverTool(tooltips=[("name", "@name"),(cat1_entry, "@cat1"),(cat2_entry, "@cat2")])

    p = figure(title="Fantasy Baseball", tools=[hover])
    p.plot_width = 1200
    p.xaxis.axis_label = cat1_entry
    p.yaxis.axis_label = cat2_entry

    p.circle('cat1', 'cat2', size=10, color="#4DDB94", source=source, fill_alpha=0.2)
    p.line(cat1_array, line, line_width=2)

    show(p)

plot_stats()
