import tkinter as tk
import Convert as C
import geopandas as gp

def load():
    if fileName.get().strip() != '':
        try:
            C.gdf = gp.read_file(fileName.get().strip())
            loaded.set(True)
            print('Loaded')
        except:
            print('Loading Error')
    else:
        print('FileName can not be empty')

def convert():
    if loaded.get():
        if (tag.get().strip() != '') or (type_.get().strip()):
            C.export(type_.get().strip(), tag.get().strip())
        else:
            print('Tag/Type can not be empty')
    else:
        print('File not Loaded')

def majority():
    if loaded.get():
        try:
            C.majority()
        except:
            print('Error')
    else:
        print('File not Loaded')

def drop():
    if loaded.get():
        if col.get().strip() != '':
            try:
                C.gdf = C.gdf.drop(columns=[col.get().strip()])
                print('Dropped')
            except:
                print('Error')
        else:
            print('Col can not be empty')
    else:
        print('File not Loaded')
    
root = tk.Tk()
root.title('Convert')

fileName = tk.StringVar()
tag = tk.StringVar(value='Export')
type_ = tk.StringVar()
col = tk.StringVar()
loaded = tk.BooleanVar()

tk.Label(root, text='File Name').grid(row=0, column=0)
tk.Entry(root, textvariable=fileName).grid(row=1,column=0)
tk.Button(root, text='Load', command=load).grid(row=2, column=0)
tk.Label(root, text='Tag').grid(row=3, column=0)
tk.Entry(root, textvariable=tag).grid(row=4,column=0)
tk.Button(root, text='Majority', command=majority).grid(row=5, column=0)
tk.Checkbutton(root, text='Loaded', variable=loaded, offvalue=False, onvalue=True, state='disabled').grid(row=6, column=0)

tk.Label(root, text='Type').grid(row=0, column=1)
tk.Radiobutton(root, variable=type_, text='GeoJson', value='GeoJson').grid(row=1, column=1)
tk.Radiobutton(root, variable=type_, text='ShapeFile', value='ShapeFile').grid(row=2, column=1)
tk.Radiobutton(root, variable=type_, text='GeoPackage', value='GeoPackage').grid(row=3, column=1)
tk.Radiobutton(root, variable=type_, text='CSV', value='CSV').grid(row=4, column=1)
tk.Radiobutton(root, variable=type_, text='Json', value='Json').grid(row=5, column=1)
tk.Radiobutton(root, variable=type_, text='HTML', value='HTML').grid(row=6, column=1)
tk.Button(root, text='Convert', command=convert).grid(row=7, column=1)

tk.Label(root, text='Col').grid(row=0, column=2)
tk.Entry(root, textvariable=col).grid(row=1, column=2)
tk.Button(root, text='Drop', command=drop).grid(row=2, column=2)

root.mainloop()