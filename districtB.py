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

def setExpected():
    gdf['Expected'] = 0.0
    for i in range(len(gdf)):
        gdf.loc[i, 'Expected'] = expected(gdf['ShiftedMargin'][i])

def setMargin():
    for i in range(len(gdf)):
        gdf.loc[i, 'Margin'] = gdf['DemPct'][i] - gdf['RepPct'][i]
    gdf['ShiftedMargin'] = gdf['Margin']
    gdf['Swing'] = 0.0

def setId():
    gdf['id'] = [i + 1 for i in range(len(gdf))]

def loading(label: bool):
    if label:
        setId()
    majority()
    setMargin()
    setExpected()
    classify()

def comp():
    n = len(gdf)
    total = sum(2 * abs(.5 - gdf['Expected']))
    print(f'Competitveness: {((n - total) / n):.2%}')

def stats():
    print(f'Expected Value: {gdf['Expected'].sum():.2f}')
    print(f'Median District Margin: {gdf['ShiftedMargin'].median():.2%}')
    print(f'Min District Margin: {gdf['ShiftedMargin'].min():.2%}')
    print(f'Max District Margin: {gdf['ShiftedMargin'].max():.2%}')
    print(gdf['Majority'].value_counts())
    print(gdf.groupby('Majority').agg({'ShiftedMargin': ['mean', 'min', 'max']}))
    print(gdf['Class'].value_counts())
    comp()

def reset():
    gdf['ShiftedMargin'] = gdf['Margin']
    gdf['Swing'] = 0.0

def filter(selections: set, dem: bool, rep: bool, details: bool):
    count = 0
    for i in range(len(gdf)):
        if gdf['Majority'][i] in selections:
            if dem and gdf['ShiftedMargin'][i] > 0:
                count += 1
                if details:
                    print(gdf.iloc[i])
            elif rep and gdf['ShiftedMargin'][i] < 0:
                count += 1
                if details:
                    print(gdf.iloc[i])
    print(f'Total: {count}')

def shift(shift_amount:float, index: int, group:str, turnout:float):
    if shift_amount != 0:
        ajusted = shift_amount
        match group:
            case 'W':
                ajusted *= gdf['WhitePct'][index] * turnout
            case 'B':
                ajusted *= gdf['BlackPct'][index] * turnout
            case 'H':
                ajusted *= gdf['HispanicPct'][index] * turnout
            case 'P':
                ajusted *= gdf['PacificPct'][index] * turnout
            case 'A':
                ajusted *= gdf['AsianPct'][index] * turnout
            case 'N':
                ajusted *= gdf['NativePct'][index] * turnout
            case _:
                ajusted *= 1
        gdf.loc[index, 'ShiftedMargin'] = max(min((gdf['ShiftedMargin'][index] + ajusted), 1), -1)
        gdf.loc[index, 'Expected'] = expected(gdf['ShiftedMargin'][index])
        gdf.loc[index, 'Swing'] = gdf['Swing'][index] + ajusted

def shifter(groups, vals, turnout):
    medianA = gdf['ShiftedMargin'].median()
    expectedA = gdf['Expected'].sum()
    minA = gdf['ShiftedMargin'].min()
    maxA = gdf['ShiftedMargin'].max()
    for i in range(len(groups)):
        for j in range(len(gdf)):
            shift(vals[i], j, groups[i], turnout[i])
    print(f'Before, Median: {medianA:.2%}, Expected: {expectedA:.2f}, Min: {minA:.2%}, Max: {maxA:.2%}')
    print(f'After, Median: {gdf['ShiftedMargin'].median():.2%}, Expected: {gdf['Expected'].sum():.2f}, Min: {gdf['ShiftedMargin'].min():.2%}, Max: {gdf['ShiftedMargin'].max():.2%}')
    classify()

def classify():
    gdf['Class'] = ''
    for i in range(len(gdf)):
        if gdf['ShiftedMargin'][i] > safe_point:
            gdf.loc[i, 'Class'] = 'D'
        elif gdf['ShiftedMargin'][i] > 0:
            gdf.loc[i, 'Class'] = 'D_Comp'
        elif gdf['ShiftedMargin'][i] < -safe_point:
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
            for i in comp['Expected']:
                n = r.random()
                if n < i:
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
    pass

def map(type:str):
    match type:
        case 'Margin':
            gdf.plot(column='ShiftedMargin', cmap='RdBu', legend=True, legend_kwds={'label': 'Margin', 'orientation': 'horizontal'})
            plt.title('Margin')
            plt.show()
        case 'MinorityPct':
            gdf.plot(column='MinorityPct', cmap='Greys', legend=True, legend_kwds={'label': 'Margin', 'orientation': 'horizontal'})
            plt.title('MinorityPct')
            plt.show()
        case 'DemPct':
            gdf.plot(column='ShiftedMargin', cmap='Blues', legend=True, legend_kwds={'label': 'Margin', 'orientation': 'horizontal'})
            plt.title('DemPct')
            plt.show()
        case 'RepPct':
            gdf.plot(column='ShiftedMargin', cmap='Reds', legend=True, legend_kwds={'label': 'Margin', 'orientation': 'horizontal'})
            plt.title('RepPct')
            plt.show()
        case 'Swing':
            gdf.plot(column='Swing', cmap='RdBu', legend=True, legend_kwds={'label': 'Margin', 'orientation': 'horizontal'})
            plt.title('Swing')
            plt.show()
        case _:
            print('Make a Selection')
    pass