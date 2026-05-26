import pandas as pd

df = pd.DataFrame()

def toForm(df: pd.DataFrame, tag: str, floor: int):
    dfB = df[df['Pct'] > floor]
    data, district, index = {}, {}, dfB.index
    prev = dfB.loc[index[0], 'state']
    for i in index:
        if dfB.loc[i, 'state'] != prev:
            if district.get('REPUBLICAN', 0) == 0:
                district['REPUBLICAN'] = 0
            if district.get('DEMOCRAT', 0) == 0:
                district['DEMOCRAT'] = 0
            data[prev] = district
            prev = dfB.loc[i, 'state']
            district = {}
            district[dfB.loc[i, 'party_simplified']] = dfB.loc[i, 'Pct']
        else:
            district[dfB.loc[i, 'party_simplified']] = max(district.get('party_simplified', 0), dfB.loc[i, 'Pct'])
    data[prev] = district

    dataDF = pd.DataFrame(data)
    dataDF.transpose().to_csv(f'{tag}.csv')

def setUp(df: pd.DataFrame, year: int):
    dfB = df[df['year'] == year]
    dfB['Pct'] = (dfB['candidatevotes'] * 100) / df['totalvotes']
    dfB = dfB[['state', 'party_simplified', 'Pct']].dropna()
    return dfB

def yearSet(df: pd.DataFrame, year: int):
    try:
        if year.get() < 1976 or year.get() > 2020 or year.get() % 2 == 1:
            print('Year must be even and in bounds')
        else:
            df = pd.read_csv('1976-2024-senate.csv')
            df = df[df['year'] == 2000]
            df['Pct'] = (df['candidatevotes'] * 100) / df['totalvotes']
            df = df[['state', 'party_simplified', 'Pct']].dropna()
            df = df[df['Pct'] > 5]
            print('Set')
    except:
        print('Error')