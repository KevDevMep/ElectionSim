import pandas as pd

df = pd.DataFrame()

def shifter(shift: float, senBefore: int, govBefore: int):
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
    df['Margin'] = df['DemPct'] - df['RepPct']

def pathToVictory():
    pres = df[df['Type']=='Pres']
    if len(pres) == 0:
        print('No Pres')
    else:
        demEV = pres[pres['Margin'] > 0]['EV'].sum()
        totalEV = pres['EV'].sum()
        
        if demEV < (totalEV / 2):
            rep = pres[pres['Margin'] < 0].sort_values(by=['Margin'], ascending=False)
            n = len(rep)
            for i in range(n):
                print(rep.iloc[i])
                demEV += rep.iloc[i]['EV']
                if demEV > (totalEV / 2):
                    break
        else:
            dem = pres[pres['Margin'] > 0].sort_values(by=['Margin'])
            n = len(dem)
            for i in range(n):
                print(dem.iloc[i])
                demEV -= dem.iloc[i]['EV']
                if demEV < (totalEV / 2):
                    break

def senGoTo(senBefore: int, target: int=50):
    sen = df[df['Type']=='Senate']
    if len(sen) == 0:
        print('No Senate')
    else:
        demEV = senBefore + sen[sen['Margin'] > 0]['EV'].sum()
        if demEV < target:
            rep = sen[sen['Margin'] < 0].sort_values(by=['Margin'], ascending=False)
            n = len(rep)
            for i in range(n):
                print(rep.iloc[i])
                demEV += 1
                if demEV == target:
                    break
        else:
            dem = sen[sen['Margin'] > 0].sort_values(by=['Margin'])
            n = len(dem)
            for i in range(n):
                if demEV == target:
                    break
                print(dem.iloc[i])
                demEV -= 1

def comp():
    pres = df[df['Type']=='Pres']
    if len(pres) != 0:
        print('Pres:')
        print(pres[abs(pres['Margin']) < 5].sort_values(by=['Margin']))

    sen = df[df['Type']=='Senate']
    if len(sen) != 0:
        print('Senate:')
        print(sen[abs(sen['Margin']) < 5].sort_values(by=['Margin']))

    house = df[df['Type']=='House']
    if len(house) != 0:
        print('House:')
        print(house[abs(house['Margin']) < 5].sort_values(by=['Margin']))
    
    gov = df[df['Type']=='Gov']
    if len(gov) != 0:
        print('Gov:')
        print(gov[abs(gov['Margin']) < 5].sort_values(by=['Margin']))