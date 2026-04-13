import geopandas as gp
import tkinter as tk
import pyarrow

def setName(gdf, prefix):
    for i in range(len(gdf)):
        gdf.loc[i, 'NAME'] = prefix + str(gdf['id'][i])

def setMargin(gdf):
    for i in range(len(gdf)):
        gdf.loc[i, 'Margin'] = gdf['DemPct'][i] - gdf['RepPct'][i]

def submit():
    if filename == '':
        print('Filename is Empty')
        pass
    try:
        gdf = gp.read_file(filename.get().strip(), use_arrow=True)
        prefix = state.get().strip() + '-'
        setName(gdf, prefix)
        setMargin(gdf)
        gdf.to_file(('F_' + filename.get().strip()), driver='GeoJson')
        print('Success')
    except:
        print('Loading Error')

root = tk.Tk()
root.config(background='yellow')
root.title('Format')
filename = tk.StringVar()
state = tk.StringVar()

tk.Label(root, text='FileName').grid(row=0, column=0)
tk.Entry(root, textvariable=filename).grid(row=1, column=0)
tk.Label(root, text='State').grid(row=2, column=0)
tk.Entry(root, textvariable=state).grid(row=3, column=0)
tk.Button(root, text='Format', command=submit).grid(row=5, column=0)

root.mainloop()