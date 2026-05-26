import pandas as pd
import SenReader as SR
import tkinter as tk

def yearSet():
    try:
        if year.get() < 1976 or year.get() > 2020 or year.get() % 2 == 1:
            print('Year must be even and in bounds')
        else:
            SR.df = pd.read_csv('1976-2020-senate.csv')
            SR.df = SR.setUp(SR.df, year.get())
            set_.set(True)
            print('Set')
    except:
        print('Error')

def export():
    if set_.get():
        if tag.get().strip():
            try:
                SR.toForm(SR.df, tag.get().strip(), floor.get())
                print('Export')
            except:
                print('Error')
        else:
            print('Tag can not be Empty')
    else:
        print('Not Set')

root = tk.Tk()
root.title('SenReader')
floor = tk.DoubleVar(value=5.0)
tag = tk.StringVar(value='Export')
year = tk.IntVar(value=2020)
set_ = tk.BooleanVar()

tk.Label(root, text='Year').grid(row=0, column=0)
tk.Spinbox(root, textvariable=year, from_=1976, to_=2020, increment=2).grid(row=1, column=0)
tk.Button(root, text='Set', command=yearSet).grid(row=1, column=1)
tk.Label(root, text='Tag').grid(row=2, column=0)
tk.Entry(root, textvariable=tag).grid(row=3, column=0)
tk.Label(root, text='Floor').grid(row=2, column=1)
tk.Spinbox(root, textvariable=floor, from_=0, to_=10).grid(row=3, column=1)
tk.Button(root, text='Export', command=export).grid(row=4, column=0)
tk.Checkbutton(root, text='Set', variable=set_, onvalue=True, offvalue=False, state='disabled').grid(row=4, column=1)

root.mainloop()