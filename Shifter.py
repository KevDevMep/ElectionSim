import pandas as pd

df = pd.DataFrame()

def shifter(shift: int, senBefore: int, govBefore: int):
    print('Before:')
    stats(senBefore, govBefore)
    for i in range(len(df)):
        df.loc[i, 'Margin'] = min(max(df.loc[i, 'Margin'] + shift, -100), 100)
    print('After:')
    stats(senBefore, govBefore)

def stats(senBefore: int, govBefore: int):
    dPres = df[(df['Type'] == 'Pres') & (df['Margin'] > 0.0)]['EV'].sum()
    pres = df[df['Type'] == 'Pres']['EV'].sum()
    dHouse = df[(df['Type'] == 'House') & (df['Margin'] > 0.0)]['EV'].sum()
    house = df[(df['Type'] == 'House')]['EV'].sum()
    dSen = df[(df['Type'] == 'Senate') & (df['Margin'] > 0.0)]['EV'].sum()
    dGov = df[(df['Type'] == 'Gov') & (df['Margin'] > 0.0)]['EV'].sum()
    print(f'Pres: ({dPres}, {pres - dPres})')
    print(f'House: ({dHouse}, {house - dHouse}), Median Seat: {df[df['Type'] == 'House']['Margin'].median():.2f}')
    print(f'Senate: ({senBefore + dSen}, {100 - (senBefore + dSen)})')
    print(f'Gov: ({govBefore + dGov}, {50 - (govBefore + dGov)})')

def reset():
    for i in range(len(df)):
        df.loc[i, 'Margin'] = df.loc[i, 'DemPct'] - df.loc[i, 'RepPct']