import csv
import random as r
import matplotlib.pyplot as plt
import geopandas as gp
import districtB as B
import tkinter as tk

data = []

def load():
    try:
        B.gdf = gp.read_file(filename.get().strip(), use_arrow=True)
        B.loading(not(label.get()))
        loaded.set(True)
        print('Loading Succesful')
    except:
        loaded.set(False)
        print('Loading Error')

def simulator():
    if loaded.get():
        nTrails = int(trails.get())
        B.simulator(nTrails)
        print('Sim Complete')
    else:
        print('File is not loaded')
        pass

def shifter():
    if loaded.get():
        groups = ['', 'W', 'B', 'H', 'A', 'N', 'P']
        vals = [a.get() / 100.0, b.get() / 100.0, c.get() / 100.0, d.get()/ 100.0, e.get() / 100.0, f.get() / 100.0, g.get() / 100.0]
        turnout = [to1.get() / 100.0, to2.get() / 100.0, to3.get() / 100.0, to4.get() / 100.0, to5.get() / 100.0, to6.get() / 100.0, to7.get() / 100.0]
        B.shifter(groups, vals, turnout)
        print('Shifted')
    else:
        print('File is not loaded')
        pass

def stats():
    if loaded.get():
        B.stats()
        B.prop(0.5 + (base.get() / 100.0))
    else:
        print('File is not loaded')
        pass

def reset():
    if loaded.get():
        B.reset()
        print('Reset')
        a.set(0)
        b.set(0)
        c.set(0)
        d.set(0)
        e.set(0)
        f.set(0)
        g.set(0)
        to1.set(1)
        to2.set(1)
        to3.set(1)
        to4.set(1)
        to5.set(1)
        to6.set(1)
        to7.set(1)
    else:
        print('File is not loaded')

def export():
    if loaded.get():
        try:
            map = B.gdf.drop(columns=['geometry', 'opacity', 'color'])
            match exportType.get():
                case 'GeoJson':
                    B.gdf.to_file('Export.geojson', use_arrow=True, driver='GeoJson')
                case 'CSV':
                    map.to_csv('Export.csv')
                case 'Json':
                    map.to_json('Export.json')
                case 'HTML':
                    map.to_html('Export.html')
            print('Exported')
        except:
            print('Export Error')
    else:
        print('File is not loaded')

def filter():
    if loaded.get():
        selections = set([white.get(), black.get(), hispanic.get(), asian.get(), native.get(), minority.get()])
        class_ = set([dem.get(), rep.get(), demComp.get(), repComp.get()])
        B.filter(selections, class_, details.get())
    else:
        print('File is not loaded')

def setSafePoint():
    B.safe_point = safe_point.get() / 100.0
    B.setExpected()
    B.classify()
    print('Set')

def map():
    if loaded.get():
        B.map(mapType.get())
    else:
        print('File not loaded')

root = tk.Tk()
root.config(background='skyblue')
root.title('Election Simulator')
print('+ for D, - for R')

# Vars
loaded = tk.BooleanVar()
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
details = tk.BooleanVar()
safe_point = tk.IntVar(value=15)
mapType = tk.StringVar(value='')
label = tk.BooleanVar()
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
exportType = tk.StringVar(value='GeoJson')
base = tk.DoubleVar(value=0.0)

# Middle Section
tk.Label(root, text='File').grid(row=0,column=3)
tk.Entry(root, textvariable=filename).grid(row=1,column=3)
tk.Button(root, text='Load', command=load).grid(row=1,column=4)
tk.Label(root, text='Safe Point (%)').grid(row=2, column=3)
tk.Spinbox(root, from_=0, to_=100, textvariable=safe_point).grid(row=3, column=3)
tk.Button(root, text='Set', command=setSafePoint).grid(row=3, column=4)
tk.Label(root, text='Trails').grid(row=4,column=3)
tk.Spinbox(root, textvariable=trails, from_=1, to=10000).grid(row=5,column=3)
tk.Button(root, text='Sim', command=simulator).grid(row=5,column=4)
tk.Label(root, text='Base Environment (%)').grid(row=6, column=3)
tk.Spinbox(root, textvariable=base, from_=-50, to=50).grid(row=7, column=3)
tk.Button(root, text='Stats', command=stats).grid(row=8,column=3)
tk.Button(root, text='Reset', command=reset).grid(row=9,column=3)
tk.Checkbutton(root, variable=loaded, text='Loaded', onvalue=True, offvalue=False, state='disabled').grid(row=10, column=4)
tk.Checkbutton(root, variable=details, text='Details', onvalue=True, offvalue=False).grid(row=10, column=3)
tk.Label(root, text='File Type').grid(row=11, column=3)
tk.Radiobutton(root, variable=label, text='National', value=False).grid(row=12, column=3)
tk.Radiobutton(root, variable=label, text='State', value=True).grid(row=13, column=3)

# Shifting Section
tk.Label(root, text='Shifting').grid(row=0,column=0)
tk.Label(root, text='Turnout (%)').grid(row=0,column=1)
tk.Label(root, text='Baseline (%)').grid(row=1,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=a).grid(row=2,column=0)
tk.Spinbox(root, from_= 0, to=200, textvariable=to1).grid(row=2,column=1)
tk.Label(root, text='White (%)').grid(row=3,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=b).grid(row=4,column=0)
tk.Spinbox(root, from_= 0, to=200, textvariable=to2).grid(row=4,column=1)
tk.Label(root, text='Black (%)').grid(row=5,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=c).grid(row=6,column=0)
tk.Spinbox(root, from_= 0, to=200, textvariable=to3).grid(row=6,column=1)
tk.Label(root, text='Hispanic (%)').grid(row=7,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=d).grid(row=8,column=0)
tk.Spinbox(root, from_= 0, to=200, textvariable=to4).grid(row=8,column=1)
tk.Label(root, text='Asian (%)').grid(row=9,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=e).grid(row=10,column=0)
tk.Spinbox(root, from_= 0, to=200, textvariable=to5).grid(row=10,column=1)
tk.Label(root, text='Native (%)').grid(row=11,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=f).grid(row=12,column=0)
tk.Spinbox(root, from_= 0, to=200, textvariable=to6).grid(row=12,column=1)
tk.Label(root, text='Pacific (%)').grid(row=13,column=0)
tk.Spinbox(root, from_=-100, to=100, textvariable=g).grid(row=14,column=0)
tk.Spinbox(root, from_= 0, to=200, textvariable=to7).grid(row=14,column=1)
tk.Button(root, text='Shift', command=shifter).grid(row=17,column=0)

# Filtering Section
tk.Label(root, text='Filters').grid(row=0, column=5)
tk.Checkbutton(root, variable=white, onvalue='White', offvalue='', text='White').grid(row=1, column=5)
tk.Checkbutton(root, variable=black, onvalue='Black', offvalue='',text='Black').grid(row=2, column=5)
tk.Checkbutton(root, variable=hispanic, onvalue='Hispanic', offvalue='', text='Hispanic').grid(row=3, column=5)
tk.Checkbutton(root, variable=asian, onvalue='Asian', offvalue='', text='Asian').grid(row=4, column=5)
tk.Checkbutton(root, variable=native, text='Native', onvalue='Native', offvalue='').grid(row=5, column=5)
tk.Checkbutton(root, variable=pacific, text='Pacific', onvalue='Pacific', offvalue='').grid(row=6, column=5)
tk.Checkbutton(root, variable=minority, text='Minority', onvalue='Minority', offvalue='').grid(row=7, column=5)
tk.Checkbutton(root, variable=dem, text='Dem', onvalue='D', offvalue='').grid(row=8, column=5)
tk.Checkbutton(root, variable=rep, text='Rep', onvalue='R', offvalue='').grid(row=9, column=5)
tk.Checkbutton(root, variable=demComp, text='Dem Comp', onvalue='D_Comp', offvalue='').grid(row=10, column=5)
tk.Checkbutton(root, variable=repComp, text='Rep Comp', onvalue='R_Comp', offvalue='').grid(row=11, column=5)
tk.Button(root, text='Filter', command=filter).grid(row=12, column=5)

# Mapping Section
tk.Label(root, text='Mapping').grid(row=0, column=6)
tk.Radiobutton(root, text='Margin', variable=mapType, value='Margin').grid(row=1, column=6)
tk.Radiobutton(root, text='Minority', variable=mapType, value='MinorityPct').grid(row=2, column=6)
tk.Radiobutton(root, text='Dem', variable=mapType, value='DemPct').grid(row=3, column=6)
tk.Radiobutton(root, text='Rep', variable=mapType, value='RepPct').grid(row=4, column=6)
tk.Radiobutton(root, text='Swing', variable=mapType, value='Swing').grid(row=5, column=6)
tk.Button(root, text='Map', command=map).grid(row=6, column=6)
tk.Label(root, text='Export Type').grid(row=8, column=6)
tk.Radiobutton(root, variable=exportType, text='Geojson', value='Geojson').grid(row=9, column=6)
tk.Radiobutton(root, variable=exportType, text='CSV', value='CSV').grid(row=10, column=6)
tk.Radiobutton(root, variable=exportType, text='Json', value='Json').grid(row=11, column=6)
tk.Radiobutton(root, variable=exportType, text='HTML', value='HTML').grid(row=12, column=6)
tk.Button(root, text='Export', command=export).grid(row=13,column=6)

root.mainloop()