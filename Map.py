import geopandas as gp
import pyarrow
import matplotlib.pyplot as plt
import tkinter as tk

def map():
    if filename.get().strip() == '':
        print('Filename can not be empty')
        pass
    try:
        gdf = gp.read_file(filename.get().strip(), use_arrow=True)
    except:
        print('Loading Error')
        pass
    match mapType.get().strip():
        case 'Margin':
            gdf.plot(column='Margin', cmap='RdBu', legend=True)
            plt.show()
        case 'MinorityPct':
            gdf.plot(column='MinorityPct', cmap='Greys', legend=True)
            plt.show()
        case 'DemPct':
            gdf.plot(column='Margin', cmap='Blues', legend=True)
            plt.show()
        case 'RepPct':
            gdf.plot(column='Margin', cmap='Reds', legend=True)
            plt.show()
    pass

root = tk.Tk()
root.config(background='blue')
filename = tk.StringVar(value='')
mapType = tk.StringVar(value='')

t1 = tk.Label(root, text='File').grid(row=0, column=0)
e1 = tk.Entry(root, textvariable=filename).grid(row=1, column=0)
t1 = tk.Label(root, text='Type').grid(row=0, column=1)
r1 = tk.Radiobutton(root, text='Margin', variable=mapType, value='Margin').grid(row=1, column=1)
r2 = tk.Radiobutton(root, text='Minority', variable=mapType, value='MinorityPct').grid(row=2, column=1)
r3 = tk.Radiobutton(root, text='Dem', variable=mapType, value='DemPct').grid(row=3, column=1)
r4 = tk.Radiobutton(root, text='Rep', variable=mapType, value='RepPct').grid(row=4, column=1)
submit = tk.Button(root, text='Map', command=map).grid(row=3, column=0)

root.mainloop()