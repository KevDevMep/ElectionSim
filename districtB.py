import geopandas as gp
import random as r
import matplotlib.pyplot as plt
import csv

safe_point = .15
gdf = gp.GeoDataFrame()
expected = lambda n: min(max((1 + (1 / safe_point) * n) / 2.0, 0.0), 1.0)

def majority():
    gdf['Majority'] = ''
    for i in range(len(gdf)):
        if gdf['WhitePct'][i] > .5:
            gdf.loc[i, 'Majority'] = "White"
        elif gdf['HispanicPct'][i] > gdf['WhitePct'][i] and gdf['HispanicPct'][i] > gdf['BlackPct'][i] and gdf['HispanicPct'][i] > gdf['AsianPct'][i] and gdf['HispanicPct'][i] > gdf['NativePct'][i] and gdf['HispanicPct'][i] > gdf['PacificPct'][i]:
            gdf.loc[i, 'Majority'] = "Hispanic"
        elif gdf['BlackPct'][i] > gdf['WhitePct'][i] and gdf['BlackPct'][i] > gdf['AsianPct'][i] and gdf['BlackPct'][i] > gdf['NativePct'][i] and gdf['BlackPct'][i] > gdf['PacificPct'][i]:
            gdf.loc[i, 'Majority'] = "Black"
        elif gdf['AsianPct'][i] > gdf['WhitePct'][i] and gdf['AsianPct'][i] > gdf['NativePct'][i] and gdf['AsianPct'][i] > gdf['PacificPct'][i]:
            gdf.loc[i, 'Majority'] = "Asian"
        elif gdf['NativePct'][i] > gdf['WhitePct'][i] and gdf['NativePct'][i] > gdf['PacificPct'][i]:
            gdf.loc[i, 'Majority'] = "Native"
        elif gdf['PacificPct'][i] > gdf['WhitePct'][i]:
            gdf.loc[i, 'Majority'] = "Pacific"
        else:
            gdf.loc[i, 'Majority'] = "Minority"

def setExpected(load: bool=False):
    if safe_point == 0:
        print('Safe Point can not 0')
        pass
    if load:
        gdf['Expected'] = 0.0
    for i in range(len(gdf)):
        gdf.loc[i, 'Expected'] = expected(gdf['Margin'][i])

def adjust(load: bool=False):
    setExpected(load)
    classify(load)

def loading():
    gdf['id'] = [i + 1 for i in range(len(gdf))]
    majority()
    reset(True)

def comp():
    n = len(gdf)
    env = gdf['Margin'].mean()
    total = sum(2 * abs(.5 - gdf['Expected'] + env))
    print(f'Competitveness: {((n - total) / n):.2%}')

def prop():
    n, env = len(gdf), gdf['Margin'].mean()
    base = n * (.5 + env)
    diff = (gdf['Expected'].sum() - base) / n
    print(f'Proportionality: {1 - abs(diff):.2%}, Map Diff: {diff:.2%}')
    print(f'D Above Mean: {len(gdf[gdf['Margin'] > env])}, R Above Mean: {len(gdf[gdf['Margin'] < env])}')

def stats():
    print(f'Number of Districts: {len(gdf)}')
    print(f'Expected Value: {gdf['Expected'].sum():.2f}')
    print(f'Seat %: {(gdf['Expected'].sum() / len(gdf)):.2%}')
    print(f'Median District Margin: {gdf['Margin'].median():.2%}')
    print(f'Min District Margin: {gdf['Margin'].min():.2%}')
    print(f'Max District Margin: {gdf['Margin'].max():.2%}')
    print(f'Environment: {gdf['Margin'].mean():.2%}')
    print(gdf['Majority'].value_counts())
    print(gdf.groupby('Majority').agg({'Margin': ['mean', 'min', 'max']}))
    print(gdf['Class'].value_counts())
    prop()
    comp()

def reset(load=False):
    gdf['Margin'] = gdf['DemPct'] - gdf['RepPct']
    adjust(load)

def filter(selections: set, class_: set, details: bool):
    filtered = gdf[gdf['Majority'].isin(selections)]
    filtered = filtered[filtered['Class'].isin(class_)]
    if details:
        print(filtered.drop(columns=['geometry', 'Class', 'Expected', 'DemPct', 'RepPct']))
    print(f'Total: {len(filtered)}')

def shift(shift_amount:float, index: int, group:str):
    if shift_amount != 0:
        ajusted = shift_amount
        match group:
            case 'W':
                ajusted *= gdf['WhitePct'][index]
            case 'B':
                ajusted *= gdf['BlackPct'][index]
            case 'H':
                ajusted *= gdf['HispanicPct'][index]
            case 'P':
                ajusted *= gdf['PacificPct'][index]
            case 'A':
                ajusted *= gdf['AsianPct'][index]
            case 'N':
                ajusted *= gdf['NativePct'][index]
            case _:
                ajusted *= 1
        gdf.loc[index, 'Margin'] = max(min((gdf['Margin'][index] + ajusted), 1), -1)
        gdf.loc[index, 'Expected'] = expected(gdf['Margin'][index])

def shifter(groups:list[str], vals:list[float], print_=True):
    if print_:
        median = gdf['Margin'].median()
        expected = gdf['Expected'].sum()
        min = gdf['Margin'].min()
        max = gdf['Margin'].max()
        seatPct = expected / len(gdf)
        env = gdf['Margin'].mean()
    for i in range(len(groups)):
        for j in range(len(gdf)):
            shift(vals[i], j, groups[i])
    if print_:
        print(f'Before, Median: {median:.2%}, Expected Value: {expected:.2f}, Seat %: {seatPct:.2%}, Min: {min:.2%}, Max: {max:.2%}, Environment: {env:.2%}')
        print(f'After, Median: {gdf['Margin'].median():.2%}, Expected Value: {gdf['Expected'].sum():.2f}, Seat %: {gdf['Expected'].sum() / len(gdf):.2%} , Min: {gdf['Margin'].min():.2%}, Max: {gdf['Margin'].max():.2%}, Environment: {gdf['Margin'].mean():.2%}')
    adjust()

def classify(load=False):
    if load:
        gdf['Class'] = ''
    for i in range(len(gdf)):
        if gdf['Margin'][i] > safe_point:
            gdf.loc[i, 'Class'] = 'D'
        elif gdf['Margin'][i] > 0:
            gdf.loc[i, 'Class'] = 'D_Comp'
        elif gdf['Margin'][i] < -safe_point:
            gdf.loc[i, 'Class'] = 'R'
        else:
            gdf.loc[i, 'Class'] = 'R_Comp'

def simulator(nTrails: int):
    seats = len(gdf)
    results = {}
    total, wins, d_safe = 0, 0, len(gdf[gdf['Class'] == 'D'])
    comp = gdf[(gdf['Class'] == 'D_Comp') | (gdf['Class'] == 'R_Comp')]
                    
    with open('Results.csv', 'w', newline='') as csvfile:
        fieldnames = ['trail', 'd_seats', 'r_seats', 'winner']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(nTrails):
            trail_total = d_safe
            total += d_safe
            for expected in comp['Expected']:
                n = r.random()
                if n < expected:
                    total += 1
                    trail_total += 1
            results[trail_total] = results.get(trail_total, 0) + 1
            writer.writerow({'trail': i + 1, 'd_seats': trail_total, 'r_seats': seats - trail_total, 'winner': 1 if trail_total > (seats - trail_total) else 0})
            if trail_total > (seats - trail_total):
                wins += 1

    print(f'Average Districts Won: {total / nTrails}, Wins: (D: {wins}, R: {nTrails - wins})')
    plt.scatter(results.keys(), results.values())
    plt.xlabel('Number of D Seats')
    plt.ylabel('Count')
    plt.title('Simulator Results')
    plt.show()

def map(type:str):
    match type:
        case 'Margin':
            gdf.plot(column='Margin', cmap='RdBu', legend=True, legend_kwds={'label': 'Margin', 'orientation': 'horizontal'})
            plt.title('Margin')
            plt.show()
        case 'White':
            gdf.plot(column='WhitePct', cmap='gray', legend=True, legend_kwds={'label': 'White', 'orientation': 'horizontal'})
            plt.title('White')
            plt.show()
        case 'MinorityPct':
            gdf.plot(column='MinorityPct', cmap='Greys', legend=True, legend_kwds={'label': 'Minority', 'orientation': 'horizontal'})
            plt.title('MinorityPct')
            plt.show()
        case 'DemPct':
            gdf.plot(column='DemPct', cmap='Blues', legend=True, legend_kwds={'label': 'Dem', 'orientation': 'horizontal'})
            plt.title('DemPct')
            plt.show()
        case 'RepPct':
            gdf.plot(column='RepPct', cmap='Reds', legend=True, legend_kwds={'label': 'Rep', 'orientation': 'horizontal'})
            plt.title('RepPct')
            plt.show()
        case _:
            print('Make a Selection')

def web_map(type:str):
    match type:
        case 'Margin':
            map = gdf.explore(column='Margin', cmap='RdBu', legend=True, tiles="CartoDB positron", scheme='equal_interval', k=8, legend_kwds=dict(colorbar=False))
            map.show_in_browser()
        case 'White':
            map = gdf.explore(column='WhitePct', cmap='gray', legend=True, tiles="CartoDB positron")
            map.show_in_browser()
        case 'MinorityPct':
            map = gdf.explore(column='MinorityPct', cmap='Greys', legend=True, tiles="CartoDB positron")
            map.show_in_browser()
        case 'DemPct':
            map = gdf.explore(column='DemPct', cmap='Blues', legend=True, tiles="CartoDB positron")
            map.show_in_browser()
        case 'RepPct':
            map = gdf.explore(column='RepPct', cmap='Reds', legend=True, tiles="CartoDB positron")
            map.show_in_browser()
        case _:
            print('Make a Selection')