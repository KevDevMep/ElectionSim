import csv
import random as r
import matplotlib.pyplot as plt
import geopandas as gp
import districtB as B
import tkinter as tk

data = []

def load():
    try:
        with open(preset.get().strip(), 'r', encoding="utf-8") as f:
            filename = f.readline().strip()

        B.gdf = gp.read_file(filename, use_arrow=True)
        B.loading()
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
        B.shifter(groups, vals)
        print('Shifted')
    else:
        print('File is not loaded')
        pass

def stats():
    if loaded.get():
        B.stats()
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
    else:
        print('File is not loaded')

def export():
    if loaded.get():
        try:
            B.gdf.to_file('Export.geojson', use_arrow=True, driver='GeoJson')
            print('Exported')
        except:
            print('Export Error')
    else:
        print('File is not loaded')

def filter():
    if loaded.get():
        selections = set([white.get(), black.get(), hispanic.get(), asian.get(), native.get(), minority.get()])
        B.filter(selections, dem.get(), rep.get(), details.get())
    else:
        print('File is not loaded')

def setSafePoint():
    B.safe_point = safe_point.get()
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

# Vars
loaded = tk.BooleanVar()
white = tk.StringVar()
black = tk.StringVar()
hispanic = tk.StringVar()
asian = tk.StringVar()
native = tk.StringVar()
pacific = tk.StringVar()
minority = tk.StringVar()
dem = tk.BooleanVar(value=True)
rep = tk.BooleanVar(value=True)
details = tk.BooleanVar()
safe_point = tk.DoubleVar(value=.15)
mapType = tk.StringVar(value='')
a = tk.IntVar(value=0)
b = tk.IntVar(value=0)
c = tk.IntVar(value=0)
d = tk.IntVar(value=0)
e = tk.IntVar(value=0)
f = tk.IntVar(value=0)
g = tk.IntVar(value=0)

# Middle Section
title1 = tk.Label(root, text='File').grid(row=0,column=2)
preset = tk.Entry(root)
preset.grid(row=1,column=2)
submit1 = tk.Button(root, text='Load', command=load).grid(row=1,column=3)
title3 = tk.Label(root, text='Safe Point').grid(row=2, column=2)
s8 = tk.Spinbox(root, from_=0, to_=1, textvariable=safe_point, increment=.01).grid(row=3, column=2)
submit9 = tk.Button(root, text='Set', command=setSafePoint).grid(row=3, column=3)
title2 = tk.Label(root, text='Trails').grid(row=4,column=2)
trails = tk.Spinbox(root, from_=1, to=1000)
trails.grid(row=5,column=2)
submit2 = tk.Button(root, text='Sim', command=simulator).grid(row=5,column=3)
submit3 = tk.Button(root, text='Stats', command=stats).grid(row=6,column=2)
submit6 = tk.Button(root, text='Export', command=export).grid(row=8,column=2)
submit7 = tk.Button(root, text='Reset', command=reset).grid(row=7,column=2)
check = tk.Checkbutton(root, variable=loaded, text='Loaded', onvalue=True, offvalue=False, state='disabled').grid(row=8, column=2)

# Shifting Section
title3 = tk.Label(root, text='Shifting').grid(row=0,column=0)
t1 = tk.Label(root, text='Baseline (%)').grid(row=1,column=0)
s1 = tk.Spinbox(root, from_=-100, to=100, textvariable=a)
s1.grid(row=2,column=0)
t2 = tk.Label(root, text='White (%)').grid(row=3,column=0)
s2 = tk.Spinbox(root, from_=-100, to=100, textvariable=b)
s2.grid(row=4,column=0)
t3 = tk.Label(root, text='Black (%)').grid(row=5,column=0)
s3 = tk.Spinbox(root, from_=-100, to=100, textvariable=c)
s3.grid(row=6,column=0)
t4 = tk.Label(root, text='Hispanic (%)').grid(row=7,column=0)
s4 = tk.Spinbox(root, from_=-100, to=100, textvariable=d)
s4.grid(row=8,column=0)
t5 = tk.Label(root, text='Asian (%)').grid(row=9,column=0)
s5 = tk.Spinbox(root, from_=-100, to=100, textvariable=e)
s5.grid(row=10,column=0)
t6 = tk.Label(root, text='Native (%)').grid(row=11,column=0)
s6 = tk.Spinbox(root, from_=-100, to=100, textvariable=f)
s6.grid(row=12,column=0)
t7 = tk.Label(root, text='Pacific (%)').grid(row=13,column=0)
s7 = tk.Spinbox(root, from_=-100, to=100, textvariable=g)
s7.grid(row=14,column=0)
submit4 = tk.Button(root, text='Shift', command=shifter).grid(row=17,column=0)

# Filtering Section
title4 = tk.Label(root, text='Filters').grid(row=0, column=4)
check2 = tk.Checkbutton(root, variable=white, onvalue='White', offvalue='', text='White').grid(row=1, column=4)
check3 = tk.Checkbutton(root, variable=black, onvalue='Black', offvalue='',text='Black').grid(row=2, column=4)
check4 = tk.Checkbutton(root, variable=hispanic, onvalue='Hispanic', offvalue='', text='Hispanic').grid(row=3, column=4)
check5 = tk.Checkbutton(root, variable=asian, onvalue='Asian', offvalue='', text='Asian').grid(row=4, column=4)
check6 = tk.Checkbutton(root, variable=native, text='Native', onvalue='Native', offvalue='').grid(row=5, column=4)
check7 = tk.Checkbutton(root, variable=pacific, text='Pacific', onvalue='Pacific', offvalue='').grid(row=6, column=4)
check8 = tk.Checkbutton(root, variable=minority, text='Minority', onvalue='Minority', offvalue='').grid(row=7, column=4)
check9 = tk.Checkbutton(root, variable=dem, text='Dem', onvalue=True, offvalue=False).grid(row=8, column=4)
check10 = tk.Checkbutton(root, variable=rep, text='Rep', onvalue=True, offvalue=False).grid(row=9, column=4)
check11 = tk.Checkbutton(root, variable=details, text='Details', onvalue=True, offvalue=False).grid(row=9, column=2)
submit8 = tk.Button(root, text='Filter', command=filter).grid(row=10, column=4)

# Mapping Section
t1 = tk.Label(root, text='Mapping').grid(row=0, column=5)
r1 = tk.Radiobutton(root, text='Margin', variable=mapType, value='Margin').grid(row=1, column=5)
r2 = tk.Radiobutton(root, text='Minority', variable=mapType, value='MinorityPct').grid(row=2, column=5)
r3 = tk.Radiobutton(root, text='Dem', variable=mapType, value='DemPct').grid(row=3, column=5)
r4 = tk.Radiobutton(root, text='Rep', variable=mapType, value='RepPct').grid(row=4, column=5)
r5 = tk.Radiobutton(root, text='Swing', variable=mapType, value='Swing').grid(row=5, column=5)
submit = tk.Button(root, text='Map', command=map).grid(row=6, column=5)

root.mainloop()