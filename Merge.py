import geopandas as gp
import tkinter as tk
import pyarrow

def geoMerge():
    if filename1.get().strip() == '' or filename2.get().strip() == '':
        print('Files can not be empty')
        pass
        
    try:
        gdf1 = gp.read_file(filename1.get().strip(), use_arrow=True)
        gdf2 = gp.read_file(filename2.get().strip(), use_arrow=True, columns=['id', 'DemPct', 'RepPct'])
        gdf2 = gdf2.rename(columns={'DemPct': 'DemPct2', 'RepPct': 'RepPct2'})
        merged = gdf1.merge(gdf2, on='id')
        merged = merged.drop(columns=['geometry_y'])
        merged = merged.rename(columns={'geometry_x':'geometry'})
        merged['Margin'] = merged['DemPct'] - merged['RepPct']
        merged['Margin2'] = merged['DemPct2'] - merged['RepPct2']
        merged['Swing'] = merged['Margin'] - merged['Margin2']
        merged.to_file('Merged.geojson', use_arrow=True, driver='GeoJson')
        print('Success')
    except:
        print('Error')

root = tk.Tk()
root.config(background='red')
filename1 = tk.StringVar(value='')
filename2 = tk.StringVar(value='')

t1 = tk.Label(root, text='File1').grid(row=0, column=0)
e1 = tk.Entry(root, textvariable=filename1).grid(row=1, column=0)
t2 = tk.Label(root, text='File2').grid(row=2, column=0)
e2 = tk.Entry(root, textvariable=filename2).grid(row=3, column=0)
submit = tk.Button(root, text='Merge', command=geoMerge).grid(row=4, column=0)

root.mainloop()