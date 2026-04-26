import pandas as pd
import tkinter as tk
import Shifter as S

def load():
    try:
        S.df = pd.read_csv(filename.get().strip())
        loaded.set(True)
        print('Loaded')
    except:
        print('Error')

def shifter():
    if loaded.get():
        S.shifter(shift.get(), senBefore.get(), govBefore.get())
        print('Shifted')
    else:
        print('File not Loaded')

def reset():
    if loaded.get():
        S.reset()
        print('Reset')
    else:
        print('File not Loaded')

def stats():
    if loaded.get():
        S.stats(senBefore.get(), govBefore.get())
    else:
        print('File not Loaded')

def pres():
    print(S.df[S.df['Type']=='Pres'])

def house():
    print(S.df[S.df['Type']=='House'])

def senate():
    print(S.df[S.df['Type']=='Senate'])

def gov():
    print(S.df[S.df['Type']=='Gov'])

root = tk.Tk()
root.title('Shifter')
filename = tk.StringVar()
loaded = tk.BooleanVar()
shift = tk.IntVar()
senBefore = tk.IntVar()
govBefore = tk.IntVar()

tk.Label(root, text='Filename').grid(row=0, column=0)
tk.Entry(root, textvariable=filename).grid(row=1, column=0)
tk.Button(root, text='Load', command=load).grid(row=1, column=1)
tk.Label(root, text='Margin (%)').grid(row=2, column=0)
tk.Spinbox(root, from_=-100, to_=100, textvariable=shift).grid(row=3, column=0)
tk.Button(root, text='Shift', command=shifter).grid(row=3, column=1)
tk.Button(root, text='Stats', command=stats).grid(row=4, column=0)
tk.Button(root, text='Reset', command=reset).grid(row=4, column=1)
tk.Checkbutton(root, variable=loaded, text='Loaded', onvalue=True, offvalue=False, state='disabled').grid(row=5, column=0)
tk.Label(root, text='Senate Comp').grid(row=6, column=0)
tk.Label(root, text='Gov Comp').grid(row=6, column=1)
tk.Spinbox(root, textvariable=senBefore, from_=0, to_=100).grid(row=7, column=0)
tk.Spinbox(root, textvariable=govBefore, from_=0, to_=50).grid(row=7, column=1)
tk.Button(root, text='President', command=pres).grid(row=0, column=3)
tk.Button(root, text='House', command=house).grid(row=1, column=3)
tk.Button(root, text='Senate', command=senate).grid(row=2, column=3)
tk.Button(root, text='Governor', command=gov).grid(row=3, column=3)
root.mainloop()