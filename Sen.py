import pandas as pd
import tkinter as tk

def classify(df_):
    index, df_['Class'] = df_.index, ''
    
    for i in index:
        if df_['Margin'][i] > 0.05:
            df_.loc[i, 'Class'] = 'D'
        elif df_['Margin'][i] < -0.05:
            df_.loc[i, 'Class'] = 'R'
        else:
            df_.loc[i, 'Class'] = 'Comp'


def stats():
    try:
        df_ = df[df['State'] == state.get()]
        classify(df_)
        print(f'Median District Margin: {df_['Margin'].median():.2%}')
        print(df_['Class'].value_counts())
    except:
        print('Error')


root = tk.Tk()
df = pd.read_csv('Nat Sen.csv')
state = tk.StringVar()

root.title('Senate Stats')
tk.Label(text='State').grid(row=0)
tk.Entry(textvariable=state).grid(row=1)
tk.Button(text='Stats', command=stats).grid(row=2)

root.mainloop()