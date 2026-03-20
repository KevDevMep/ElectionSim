import geopandas as gp
import tkinter as tk
import pyarrow

def add(gdf, prefix):
    for i in range(len(gdf)):
        gdf.iloc[i, 1] = prefix + str(gdf['id'][i])

def submit():
    if filename == '':
        print('Filename is Empty')
        pass
    try:
        gdf = gp.read_file(filename.get().strip(), use_arrow=True)
        prefix = type.get().strip() + '-'
        gdf['NAME'] = state.get().strip()
        add(gdf, prefix)
        gdf.to_file(('F_' + filename.get().strip()), use_arrow=True, driver='GeoJson')
        print('Success')
    except:
        print('Loading Error')

root = tk.Tk()
root.config(background='yellow')
filename = tk.StringVar(value='')
type = tk.StringVar(value='')
state = tk.StringVar(value='')

t1 = tk.Label(root, text='FileName').grid(row=0, column=0)
e1 = tk.Entry(root, textvariable=filename).grid(row=1, column=0)
t2 = tk.Label(root, text='State').grid(row=2, column=0)
e2 = tk.Entry(root, textvariable=state).grid(row=3, column=0)
t3 = tk.Label(root, text='Type').grid(row=0, column=1)
r1 = tk.Radiobutton(root, text='Congress', variable=type, value='CD').grid(row=1, column=1)
r2 = tk.Radiobutton(root, text='Senate', variable=type, value='SD').grid(row=2, column=1)
r3 = tk.Radiobutton(root, text='House', variable=type, value='HD').grid(row=3, column=1)

b1 = tk.Button(root, text='Format', command=submit).grid(row=4, column=0)

root.mainloop()