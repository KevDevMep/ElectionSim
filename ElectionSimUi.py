import csv
import random as r
import matplotlib.pyplot as plt
import geopandas as gp
import district
import tkinter as tk

data = []

def load():
    try:
        with open(preset.get().strip(), 'r', encoding="utf-8") as f:
            filetype = f.readline().strip()
            filename = f.readline().strip()
            district.safe_point = float(f.readline().strip())
            if filetype == '0':
                dataset = f.readline().strip()
        

        match filetype:
            case '0':
                with open(filename, newline='') as csvfile:
                    districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
                    for row in districtreader:
                        cd = f"{row['State']}-{row['Id']}"
                        d = district.District(cd, float(row[dataset]), float(row['WhitePct']), float(row['MinorityPct']), float(row['BlackPct']), float(row['HispanicPct']), float(row['PacificPct']), float(row['AsianPct']), float(row['NativePct']))
                        d.expected()
                        d.majority()
                        data.append(d)
            case '1':
                with open(filename, newline='') as csvfile:
                    districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
                    i = 0
                    for row in districtreader:
                        margin = float(row['DemPct']) - float(row['RepPct'])
                        d = district.District(i + 1, margin, float(row['WhitePct']), float(row['MinorityPct']), float(row['BlackPct']), float(row['HispanicPct']), float(row['PacificPct']), float(row['AsianPct']), float(row['NativePct']))
                        d.expected()
                        d.majority()
                        data.append(d)
                        i += 1
            case '2':
                gdf = gp.read_file(filename, use_arrow=True)
                seats = len(gdf)
                for i in range(seats):
                    margin = gdf['DemPct'][i] - gdf['RepPct'][i]
                    d = district.District(i + 1, margin, gdf['WhitePct'][i], gdf['MinorityPct'][i], gdf['BlackPct'][i], gdf['HispanicPct'][i], gdf['PacificPct'][i], gdf['AsianPct'][i], gdf['NativePct'][i])
                    d.expected()
                    d.majority()
                    data.append(d)
            case _:
                print('Incorrect Input')

        print('Loading Succesful')
    except:
        print('Loading Error')

def simulator():
    if data != []:
        nTrails = int(trails.get())
        results, districts = {}, {}
        seats = len(data)
        total, wins, d_safe = 0, 0, 0
        comp = []

        for d in data:
            if d.Expected == 1:
                d_safe += 1
            elif d.Expected != 0:
                comp.append(d)
                    
        with open('Results.csv', 'w', newline='') as csvfile:
            fieldnames = ['trail', 'd_seats', 'r_seats', 'winner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(nTrails):
                trail_total = d_safe
                total += d_safe
                for c in comp:
                    n = r.random()
                    if n < c.Expected:
                        total += 1
                        trail_total += 1
                        districts[c] = districts.get(c, 0) + 1
                results[trail_total] = results.get(trail_total, 0) + 1
                writer.writerow({'trail': i + 1, 'd_seats': trail_total, 'r_seats': seats - trail_total, 'winner': 1 if trail_total > (seats - trail_total) else 0})
                if trail_total > (seats - trail_total):
                    wins += 1

        with open('District Results.csv', 'w', newline='') as csvfile:
            fieldnames = ['CD', 'Margin', 'Expected', 'WhitePct', 'MinorityPct', 'BlackPct', 'HispanicPct', 'PacificPct', 'AsianPct', 'NativePct', 'Majority', 'Swing', 'd_wins', 'r_wins']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for d in districts:
                details = d.to_dict()
                details['d_wins'] = districts[d]
                details['r_wins'] = nTrails - districts[d]
                writer.writerow(details)

        print(f'average: {total / nTrails}, wins: (D: {wins}, R: {nTrails - wins})')
        plt.figure(figsize=(16, 10))
        plt.scatter(results.keys(), results.values())
        plt.xlabel('Number of D Seats')
        plt.ylabel('Count')
        plt.title('Simulator Results')
        plt.show()
        print('Sim Complete')
    else:
        print('Sim passed')
        pass

def shifter():
    if data != []:
        groups = ['', 'W', 'B', 'H', 'A', 'N', 'P']
        vals = [int(s1.get()) / 100.0, int(s2.get()) / 100.0, int(s3.get()) / 100.0, int(s4.get())/ 100.0, int(s5.get()) / 100.0, int(s6.get()) / 100.0, int(s7.get()) / 100.0]
        for i in range(len(groups)):
            for d in data:
                d.shift(vals[i], groups[i], print_=False)
        print('Shifted')
    else:
        print('data is empty')
        pass

def stats():
    if data != []:
        d_stats = {}
        total = 0
        for d in data:
            total += d.Expected
            if d.Margin > district.safe_point:
                d_stats['D_Safe'] = d_stats.get('D_Safe', 0) + 1
            elif d.Margin > 0:
                d_stats['D_Comp'] = d_stats.get('D_Comp', 0) + 1
            elif d.Margin < -district.safe_point:
                d_stats['R_Safe'] = d_stats.get('R_Safe', 0) + 1
            else:
                d_stats['R_Comp'] = d_stats.get('R_Comp', 0) + 1

            d_stats[d.Majority] = d_stats.get(d.Majority, 0) + 1

        print(f"Expected: {total}")
        print(f"D_Safe: {d_stats.get('D_Safe', 0)}, D_Comp: {d_stats.get('D_Comp', 0)}, R_Comp: {d_stats.get('R_Comp', 0)}, R_Safe: {d_stats.get('R_Safe', 0)}")
        print(f"White: {d_stats.get('White', 0)}, Black: {d_stats.get('Black', 0)}, Hispanic: {d_stats.get('Hispanic', 0)}, Asian: {d_stats.get('Asian', 0)}, Native: {d_stats.get('Native', 0)}, Pacific: {d_stats.get('Pacific', 0)}, Minority: {d_stats['Minority']}")
    else:
        print('data is empty')
        pass

def median():
    sd = sorted(data, key=lambda n: n.Margin)
    print('Median Seat: ')
    sd[len(data) // 2].to_string()

def reset():
    for d in data:
        d.reset()
    print('reset')

def export():
    with open('Adjusted.csv', 'w', newline='') as csvfile:
        fieldnames = ['CD', 'Margin', 'Expected', 'WhitePct', 'MinorityPct', 'BlackPct', 'HispanicPct', 'PacificPct', 'AsianPct', 'NativePct', 'Majority', 'Swing']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in data:
            writer.writerow(d.to_dict())
    print('exported')

root = tk.Tk()
root.config(background='skyblue')
root.title('Election Simulator')
root.minsize(300, 300)

title1 = tk.Label(root, text='Preset').grid(row=0,column=2)
preset = tk.Entry(root)
preset.grid(row=1,column=2)
submit1 = tk.Button(root, text='Load', command=load).grid(row=1,column=3)

title2 = tk.Label(root, text='Trails').grid(row=2,column=2)
trails = tk.Spinbox(root, from_=1, to=1000)
trails.grid(row=3,column=2)
submit2 = tk.Button(root, text='Sim', command=simulator).grid(row=3,column=3)

submit3 = tk.Button(root, text='Stats', command=stats).grid(row=4,column=2)

title3 = tk.Label(root, text='Shifting').grid(row=0,column=0)
t1 = tk.Label(root, text='Baseline (%)').grid(row=1,column=0)
s1 = tk.Spinbox(root, from_=-100, to=100)
s1.grid(row=2,column=0)
t2 = tk.Label(root, text='White (%)').grid(row=3,column=0)
s2 = tk.Spinbox(root, from_=-100, to=100)
s2.grid(row=4,column=0)
t3 = tk.Label(root, text='Black (%)').grid(row=5,column=0)
s3 = tk.Spinbox(root, from_=-100, to=100)
s3.grid(row=6,column=0)
t4 = tk.Label(root, text='Hispanic (%)').grid(row=7,column=0)
s4 = tk.Spinbox(root, from_=-100, to=100)
s4.grid(row=8,column=0)
t5 = tk.Label(root, text='Asian (%)').grid(row=9,column=0)
s5 = tk.Spinbox(root, from_=-100, to=100)
s5.grid(row=10,column=0)
t6 = tk.Label(root, text='Native (%)').grid(row=11,column=0)
s6 = tk.Spinbox(root, from_=-100, to=100)
s6.grid(row=12,column=0)
t7 = tk.Label(root, text='Pacific (%)').grid(row=13,column=0)
s7 = tk.Spinbox(root, from_=-100, to=100)
s7.grid(row=14,column=0)
submit4 = tk.Button(root, text='Shift', command=shifter).grid(row=17,column=0)
submit5 = tk.Button(root, text='Median', command=median).grid(row=5,column=2)
submit6 = tk.Button(root, text='Export', command=export).grid(row=7,column=2)
submit7 = tk.Button(root, text='Reset', command=reset).grid(row=6,column=2)

root.mainloop()