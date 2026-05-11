import geopandas as gp
import districtB as B
import tkinter as tk
import districtA as A
import matplotlib.pyplot as plt
import numpy as np

def load():
    try:
        if fileType.get():
            B.gdf = gp.read_file(filename.get().strip(), use_arrow=True)
            B.loading()
        else:
            A.load(filename.get().strip())
        loaded.set(True)
        print('Loading Succesful')
    except:
        loaded.set(False)
        print('Loading Error')

def simulator():
    if loaded.get():
        nTrails = int(trails.get())
        if fileType.get():
            B.simulator(nTrails)
        else:
            A.simulator(nTrails)
        print('Sim Complete')
    else:
        print('File is not loaded')
        pass

def shifter():
    if loaded.get():
        groups = ['', 'W', 'B', 'H', 'A', 'N', 'P']
        vals = [a.get() / 100.0, b.get() / 100.0, c.get() / 100.0, d.get()/ 100.0, e.get() / 100.0, f.get() / 100.0, g.get() / 100.0]
        if fileType.get():
            B.shifter(groups, vals)
        else:
            A.shifter(groups, vals)
        print('Shifted')
    else:
        print('File is not loaded')
        pass

def stats():
    if loaded.get():
        if fileType.get():
            B.stats()
        else:
            A.stats()
    else:
        print('File is not loaded')

def reset():
    if loaded.get():
        if fileType.get():
            B.reset()
        else:
            A.reset()
        a.set(0)
        b.set(0)
        c.set(0)
        d.set(0)
        e.set(0)
        f.set(0)
        g.set(0)
        print('Reset')
    else:
        print('File is not loaded')

def export():
    if exportTag.get().strip() == '':
        print('Export Name can not be empty')
    elif loaded.get():
        try:
            if fileType.get():
                map = B.gdf.drop(columns=['geometry'])
                match exportType.get():
                    case 'GeoJson':
                        B.gdf.to_file(f'{exportTag.get().strip()}.geojson', use_arrow=True, driver='GeoJson')
                    case 'Shapefile':
                        B.gdf.to_file(f'{exportTag.get().strip()}.shp', use_arrow=True)
                    case 'Geo Package':
                        B.gdf.to_file(f'{exportTag.get().strip()}.gpkg', use_arrow=True, driver='GPKG')
                    case 'CSV':
                        map.to_csv(f'{exportTag.get().strip()}.csv')
                    case 'Json':
                        map.to_json(f'{exportTag.get().strip()}.json')
                    case 'HTML':
                        map.to_html(f'{exportTag.get().strip()}.html')
            else:
                A.export(exportTag.get().strip())
            print('Exported')
        except:
            print('Export Error')
    else:
        print('File is not loaded')

def filter():
    if loaded.get():
        selections = set([white.get(), black.get(), hispanic.get(), asian.get(), native.get(), minority.get()])
        class_ = set([dem.get(), rep.get(), demComp.get(), repComp.get()])
        if fileType.get():
            B.filter(selections, class_, details.get())
        else:
            A.filter(selections, details.get(), class_)
    else:
        print('File is not loaded')

def setSafePoint():
    if fileType.get():
        B.safe_point = safe_point.get() / 100.0
        if loaded.get():
            B.adjust(False)
    else:
        A.safe_point = safe_point.get() / 100.0
        if loaded.get():
            A.adjust()
    print('Set')

def map():
    if loaded.get():
        if fileType.get():
            B.map(mapType.get())
            print(f'{mapType.get()} Mapped')
        else:
            print('Mapping is not available for CSV')
    else:
        print('File not loaded')

def web_map():
    if loaded.get():
        if fileType.get():
            B.web_map(mapType.get())
            print(f'{mapType.get()} Web Mapped')
        else:
            print('Mapping is not available for CSV')
    else:
        print('File not loaded')

def advanced():
    if loaded.get():
        results = {}
        shift = -10
        if fileType.get():
            B.shifter([''], [-0.1], print_=False)
            results[shift] = (B.gdf['Expected'].sum() / len(B.gdf)) * 100
            while shift < 10:
                shift += 1
                B.shifter([''], [0.01], print_=False)
                results[shift] = (B.gdf['Expected'].sum() / len(B.gdf)) * 100
            B.shifter([''], [-0.1], print_=False)
            env = B.gdf['Margin'].mean() * 100
        else:
            A.shifter([''], [-0.1])
            results[shift] = (A.expectedValue() / len(A.data)) * 100
            while shift < 10:
                shift += 1
                A.shifter([''], [0.01])
                results[shift] = (A.expectedValue() / len(A.data)) * 100
            A.shifter([''], [-0.1])
            env = A.env() * 100
        
        x = np.linspace(-10, 10, 20)
        y = np.linspace(50 + env - 10, 50 + env + 10, 20)
        plt.plot(x, y, label='Fair', color='g')
        plt.scatter(results.keys(), results.values(), label='Actual')
        plt.title('Seat-Vote Curve')
        plt.xlabel('Shift %')
        plt.ylabel('Seat %')
        plt.legend()
        plt.show()
    else:
        print('File is not loaded')

def equalize():
    if loaded.get():
        if fileType.get():
            B.shifter([''], [-B.gdf['Margin'].mean()])
        else:
            print('Geojson Only')
    else:
        print('File not loaded')

def selectNone():
    white.set('')
    black.set('')
    hispanic.set('')
    asian.set('')
    native.set('')
    pacific.set('')
    minority.set('')
    dem.set('')
    demComp.set('')
    rep.set('')
    repComp.set('')

def selectAll():
    white.set('White')
    black.set('Black')
    hispanic.set('Hispanic')
    asian.set('Asian')
    native.set('Native')
    pacific.set('Pacific')
    minority.set('Minority')
    dem.set('D')
    demComp.set('D_Comp')
    rep.set('R')
    repComp.set('R_Comp')

def drop():
    if loaded.get():
        if fileType.get():
            if col.get().strip() != '':
                try:
                    B.gdf = B.gdf.drop(columns=[col.get().strip()])
                    print(f'{col.get().strip()} Dropped')
                except:
                    print('Error')
            else:
                print('Col is empty')
        else:
            print('Not available for CSV')
    else:
        print('File not Loaded')

def columns():
    if loaded.get():
        if fileType.get():
            print(B.gdf.columns)
        else:
            print('Not available for CSV')
    else:
        print('File not Loaded')

root = tk.Tk()
root.config(background='skyblue')
root.title('Election Simulator')
print('+ for D, - for R')

# Vars
loaded = tk.BooleanVar()
details = tk.BooleanVar()
fileType = tk.BooleanVar(value=True) # True = Geo, False = CSV
white = tk.StringVar()
black = tk.StringVar()
hispanic = tk.StringVar()
asian = tk.StringVar()
native = tk.StringVar()
pacific = tk.StringVar()
minority = tk.StringVar()
filename = tk.StringVar()
dem = tk.StringVar()
rep = tk.StringVar()
demComp = tk.StringVar()
repComp = tk.StringVar()
exportType = tk.StringVar(value='GeoJson')
exportTag = tk.StringVar(value='Export')
mapType = tk.StringVar()
col = tk.StringVar()
safe_point = tk.IntVar(value=15)
a = tk.IntVar(value=0)
b = tk.IntVar(value=0)
c = tk.IntVar(value=0)
d = tk.IntVar(value=0)
e = tk.IntVar(value=0)
f = tk.IntVar(value=0)
g = tk.IntVar(value=0)
to1 = tk.IntVar(value=100)
to2 = tk.IntVar(value=100)
to3 = tk.IntVar(value=100)
to4 = tk.IntVar(value=100)
to5 = tk.IntVar(value=100)
to6 = tk.IntVar(value=100)
to7 = tk.IntVar(value=100)
trails = tk.IntVar(value=1)
base = tk.DoubleVar(value=0.0)

# Middle Section
tk.Label(root, text='File').grid(row=0,column=1)
tk.Entry(root, textvariable=filename).grid(row=1,column=1)
tk.Button(root, text='Load', command=load).grid(row=1,column=2)
tk.Label(root, text='Safe Point (%)').grid(row=2, column=1)
tk.Spinbox(root, from_=1, to_=100, textvariable=safe_point).grid(row=3, column=1)
tk.Button(root, text='Set', command=setSafePoint).grid(row=3, column=2)
tk.Label(root, text='Trails').grid(row=4,column=1)
tk.Spinbox(root, textvariable=trails, from_=1, to=10000).grid(row=5,column=1)
tk.Button(root, text='Sim', command=simulator).grid(row=5,column=2)
tk.Button(root, text='Stats', command=stats).grid(row=6,column=1)
tk.Button(root, text='Advanced', command=advanced).grid(row=6,column=2)
tk.Button(root, text='Reset', command=reset).grid(row=7,column=1)
tk.Button(root, text='Equalize', command=equalize).grid(row=7,column=2)
tk.Checkbutton(root, variable=loaded, text='Loaded', onvalue=True, offvalue=False, state='disabled').grid(row=8, column=2)
tk.Label(root, text='FileType').grid(row=8, column=1)
tk.Checkbutton(root, variable=details, text='Details', onvalue=True, offvalue=False).grid(row=9, column=2)
tk.Radiobutton(root, text='Geo', variable=fileType, value=True).grid(row=9, column=1)
tk.Radiobutton(root, text='CSV', variable=fileType, value=False).grid(row=10, column=1)
tk.Button(root, text='Select All', command=selectAll).grid(row=12, column=1)
tk.Button(root, text='Select None', command=selectNone).grid(row=12, column=2)

# Shifting Section
tk.Label(root, text='Shifting').grid(row=0,column=0)
tk.Label(root, text='Baseline (%)').grid(row=1,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=a).grid(row=2,column=0)
tk.Label(root, text='White (%)').grid(row=3,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=b).grid(row=4,column=0)
tk.Label(root, text='Black (%)').grid(row=5,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=c).grid(row=6,column=0)
tk.Label(root, text='Hispanic (%)').grid(row=7,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=d).grid(row=8,column=0)
tk.Label(root, text='Asian (%)').grid(row=9,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=e).grid(row=10,column=0)
tk.Label(root, text='Native (%)').grid(row=11,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=f).grid(row=12,column=0)
tk.Label(root, text='Pacific (%)').grid(row=13,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=g).grid(row=14,column=0)
tk.Button(root, text='Shift', command=shifter).grid(row=15,column=0)

# Filtering Section
tk.Label(root, text='Filters').grid(row=0, column=3)
tk.Checkbutton(root, variable=white, onvalue='White', offvalue='', text='White').grid(row=1, column=3)
tk.Checkbutton(root, variable=black, onvalue='Black', offvalue='',text='Black').grid(row=2, column=3)
tk.Checkbutton(root, variable=hispanic, onvalue='Hispanic', offvalue='', text='Hispanic').grid(row=3, column=3)
tk.Checkbutton(root, variable=asian, onvalue='Asian', offvalue='', text='Asian').grid(row=4, column=3)
tk.Checkbutton(root, variable=native, text='Native', onvalue='Native', offvalue='').grid(row=5, column=3)
tk.Checkbutton(root, variable=pacific, text='Pacific', onvalue='Pacific', offvalue='').grid(row=6, column=3)
tk.Checkbutton(root, variable=minority, text='Minority', onvalue='Minority', offvalue='').grid(row=7, column=3)
tk.Checkbutton(root, variable=dem, text='Dem', onvalue='D', offvalue='').grid(row=8, column=3)
tk.Checkbutton(root, variable=demComp, text='Dem Comp', onvalue='D_Comp', offvalue='').grid(row=9, column=3)
tk.Checkbutton(root, variable=repComp, text='Rep Comp', onvalue='R_Comp', offvalue='').grid(row=10, column=3)
tk.Checkbutton(root, variable=rep, text='Rep', onvalue='R', offvalue='').grid(row=11, column=3)
tk.Button(root, text='Filter', command=filter).grid(row=12, column=3)

# Mapping Section
tk.Label(root, text='Mapping').grid(row=0, column=4)
tk.Radiobutton(root, text='Margin', variable=mapType, value='Margin').grid(row=1, column=4)
tk.Radiobutton(root, text='White', variable=mapType, value='White').grid(row=2, column=4)
tk.Radiobutton(root, text='Minority', variable=mapType, value='MinorityPct').grid(row=3, column=4)
tk.Radiobutton(root, text='Dem', variable=mapType, value='DemPct').grid(row=4, column=4)
tk.Radiobutton(root, text='Rep', variable=mapType, value='RepPct').grid(row=5, column=4)
tk.Button(root, text='Map', command=map).grid(row=6, column=4)
tk.Button(root, text='Web Map', command=web_map).grid(row=7, column=4)
tk.Label(root, text='Col').grid(row=9, column=4)
tk.Entry(root, textvariable=col).grid(row=10, column=4)
tk.Button(root, text='Drop', command=drop).grid(row=11, column=4)
tk.Button(root, text='Columns', command=columns).grid(row=12, column=4)

# Export Section
tk.Label(root, text='Export Type').grid(row=0, column=5)
tk.Radiobutton(root, variable=exportType, text='Geojson', value='Geojson').grid(row=1, column=5)
tk.Radiobutton(root, variable=exportType, text='Shapefile', value='Shapefile').grid(row=2, column=5)
tk.Radiobutton(root, variable=exportType, text='GeoPackage', value='GeoPackage').grid(row=3, column=5)
tk.Radiobutton(root, variable=exportType, text='CSV', value='CSV').grid(row=4, column=5)
tk.Radiobutton(root, variable=exportType, text='Json', value='Json').grid(row=5, column=5)
tk.Radiobutton(root, variable=exportType, text='HTML', value='HTML').grid(row=6, column=5)
tk.Button(root, text='Export', command=export).grid(row=7,column=5)
tk.Label(root, text='Export Tag').grid(row=9, column=5)
tk.Entry(root, textvariable=exportTag).grid(row=10, column=5)

root.mainloop()