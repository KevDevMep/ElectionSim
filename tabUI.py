import tab as T
import pandas as pd
import tkinter as tk

def yearSet():
    try:
        if year.get() < 1976 or year.get() > 2024 or year.get() % 2 == 1:
            print('Year must be even and in bounds')
        else:
            T.df = pd.read_csv('1976-2024-house.tab', dtype={'runoff':str, 'special':str, 'writein':str, 'unofficial':str, 'fusion_ticket':str})
            T.df = T.setUp(T.df, year.get())
            set_.set(True)
            print('Set')
    except:
        print('Error')

def export():
    if set_.get():
        if tag.get().strip():
            try:
                T.toForm(tag.get().strip(), floor.get())
                T.toFormB(tag.get().strip())
                T.df.to_csv(f'house_{year.get()}.csv')
                print('Export')
            except:
                print('Error')
        else:
            print('Tag can not be Empty')
    else:
        print('Not Set')

def load():
    if f1.get().strip() and f2.get().strip():
        try:
            T.m1 = pd.read_csv(f1.get().strip())
            T.m2 = pd.read_csv(f2.get().strip())
            loaded.set(True)
            print('Loaded')
        except:
            print('Loading Error')
    else:
        print('Filenames can not be empty')

def merge():
    if loaded.get():
        try:
            T.merge()
            print('Merged')
        except:
            print('Error')
    else:
        print('File not loaded')

root = tk.Tk()
root.title('Tab')
floor = tk.DoubleVar(value=10.0)
tag = tk.StringVar(value='Export')
f1 = tk.StringVar()
f2 = tk.StringVar()
year = tk.IntVar(value=2024)
set_ = tk.BooleanVar()
loaded = tk.BooleanVar()

tk.Label(root, text='Year').grid(row=0, column=0)
tk.Spinbox(root, textvariable=year, from_=1976, to_=2024, increment=2).grid(row=1, column=0)
tk.Button(root, text='Set', command=yearSet).grid(row=1, column=1)
tk.Label(root, text='Tag').grid(row=2, column=0)
tk.Entry(root, textvariable=tag).grid(row=3, column=0)
tk.Label(root, text='Floor').grid(row=2, column=1)
tk.Spinbox(root, textvariable=floor, from_=0, to_=10).grid(row=3, column=1)
tk.Button(root, text='Export', command=export).grid(row=4, column=0)
tk.Checkbutton(root, text='Set', variable=set_, onvalue=True, offvalue=False, state='disabled').grid(row=4, column=1)
tk.Checkbutton(root, text='Loaded', variable=loaded, onvalue=True, offvalue=False, state='disabled').grid(row=5, column=1)

tk.Label(root, text='Merge').grid(row=0, column=2)
tk.Label(root, text='F1').grid(row=1, column=2)
tk.Entry(root, textvariable=f1).grid(row=2, column=2)
tk.Label(root, text='F2').grid(row=3, column=2)
tk.Entry(root, textvariable=f2).grid(row=4, column=2)
tk.Button(root, text='Load', command=load).grid(row=5, column=2)
tk.Button(root, text='Merge', command=merge).grid(row=6, column=2)

root.mainloop()