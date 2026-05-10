import pandas as pd

df = pd.DataFrame()
m1 = pd.DataFrame()
m2 = pd.DataFrame()

def setCD(df_: pd.DataFrame):
    index = df_.index
    for i in index:
        if df_.loc[i, 'district'] == 0:
            df_.loc[i, 'CD'] = df_.loc[i, 'state_po'] + '-AL'
        elif df_.loc[i, 'district'] < 10:
            df_.loc[i, 'CD'] = df_.loc[i, 'state_po'] + '-0' + str(df_.loc[i, 'district'])
        else:
            df_.loc[i, 'CD'] = df_.loc[i, 'state_po'] + '-' + str(df_.loc[i, 'district'])
    return df_

def toForm(tag: str, cutoff: float):
    data, district = {}, {}
    dfB = df[(df['Pct'] > cutoff) & (df['state_po'] != 'NY')]
    print(dfB)
    index = dfB.index
    print(index)
    prev = dfB.loc[index[0], 'CD']
    for i in index:
        if dfB.loc[i, 'CD'] != prev:
            data[prev] = district
            prev = dfB.loc[i, 'CD']
            district = {}
            district[dfB.loc[i, 'party']] = dfB.loc[i, 'Pct']
        else:
            district[dfB.loc[i, 'party']] = max(dfB.loc[i, 'Pct'], district.get(dfB.loc[i, 'party'], 0))
    data[prev] = district

    dataDF = pd.DataFrame(data)
    dataDF.transpose().to_csv(f'{tag}.csv')

def toFormB(tag: str):
    ny = df[df['state_po'] == 'NY']
    data, district = {}, {}
    index = ny.index
    prev = ny.loc[index[0], 'CD']
    for i in index:
        if ny.loc[i, 'CD'] != prev:
            data[prev] = district
            prev = ny.loc[i, 'CD']
            district = {}
            district[ny.loc[i, 'candidate']] = ny.loc[i, 'Pct']
        else:
            district[ny.loc[i, 'candidate']] = ny.loc[i, 'Pct'] + district.get(ny.loc[i, 'candidate'], 0)
    data[prev] = district

    dataDF = pd.DataFrame(data)
    dataDF.transpose().to_csv(f'{tag}_NY.csv')

def setUp(df_: pd.DataFrame, year: int):
    df_ = df_[(df_['year'] == year) & (df_['state_po'] != 'DC')].drop(columns=['state', 'state_fips', 'state_cen', 'state_ic', 'office', 'stage', 'runoff', 'special', 'writein', 'mode', 'unofficial', 'version', 'fusion_ticket']).dropna()
    df_ = setCD(df_)
    df_['Pct'] = (df_['candidatevotes'] / abs(df_['totalvotes'])) * 100
    return df_

def merge():
    merged = m1.merge(m2, on='id', how='outer')
    merged.to_csv('merged.csv')