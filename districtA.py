import csv
import random as r
import matplotlib.pyplot as plt
import District

safe_point = .15
data = []

def expectedValue():
    total = 0
    for district in data:
        total += district.Expected
    return total

def load(file:str):
    with open(file, newline='') as csvfile:
        districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        i = 0
        for row in districtreader:
            margin = float(row['DemPct']) - float(row['RepPct'])
            d = District.District(i + 1, margin, float(row['WhitePct']), float(row['MinorityPct']), float(row['BlackPct']), float(row['HispanicPct']), float(row['PacificPct']), float(row['AsianPct']), float(row['NativePct']))
            d.expected(safe_point)
            d.majority()
            d.classify(safe_point)
            data.append(d)
            i += 1

def simulator(trails:int):
    if data != []:
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
            for i in range(trails):
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
            fieldnames = ['d_wins', 'r_wins', 'CD', 'Margin', 'Swing', 'Majority', 'WhitePct', 'MinorityPct', 'BlackPct', 'HispanicPct', 'AsianPct', 'NativePct', 'PacificPct']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for d in districts:
                details = d.to_dict()
                details['d_wins'] = districts[d]
                details['r_wins'] = trails - districts[d]
                writer.writerow(details)

        print(f'Average: {total / trails}, Wins: (D: {wins}, R: {trails - wins})')
        plt.scatter(results.keys(), results.values())
        plt.xlabel('Number of D Seats')
        plt.ylabel('Count')
        plt.title('Simulator Results')
        plt.show()

def shifter(groups:list[str], vals:list[float]):
    if data != []:
        for i in range(len(groups)):
            for d in data:
                d.shift(vals[i], groups[i])
        adjust()
    

def stats():
    if data != []:
        d_stats = {}
        total = 0
        env_ = env()
        n = len(data)
        base = n * (.5 + env_)
        for d in data:
            total += d.Expected
            d_stats[d.Class] = d_stats.get(d.Class, 0) + 1
            d_stats[d.Majority] = d_stats.get(d.Majority, 0) + 1
        diff = (total - base) / n

        print(f"Expected Value: {total}")
        print(f'Seat %: {(total / len(data)):.2%}')
        print(f"D_Safe: {d_stats.get('D', 0)}, D_Comp: {d_stats.get('D_Comp', 0)}, R_Comp: {d_stats.get('R_Comp', 0)}, R: {d_stats.get('R_Safe', 0)}")
        print(f"White: {d_stats.get('White', 0)}, Black: {d_stats.get('Black', 0)}, Hispanic: {d_stats.get('Hispanic', 0)}, Asian: {d_stats.get('Asian', 0)}, Native: {d_stats.get('Native', 0)}, Pacific: {d_stats.get('Pacific', 0)}, Minority: {d_stats['Minority']}")
        print(f'Environment: {env_:2%}')
        median()
        print(f'Proportionality: {1 - abs(diff):.2%}, Map Diff: {diff:.2%}')

def median():
    if data != []:
        sd = sorted(data, key=lambda n: n.Margin)
        print('Median Seat: ')
        print(sd[len(data) // 2].to_string())

def reset():
    if data != []:
        for d in data:
            d.reset()

def export():
    if data != []:
        with open('Adjusted.csv', 'w', newline='') as csvfile:
            fieldnames = ['CD', 'Margin', 'Swing', 'Majority', 'WhitePct', 'MinorityPct', 'BlackPct', 'HispanicPct', 'AsianPct', 'NativePct', 'PacificPct', 'Class']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for d in data:
                writer.writerow(d.to_dict())

def filter(selections:set[str], details:bool, class_:set[str]):
    if data != []:
        count = 0
        for d in data:
            if d.Majority in selections and d.Class in class_:
                if details:
                    print(d.to_string())
                count += 1
        print(f'Count: {count}')
        
def adjust():
    for d in data:
        d.expected(safe_point)
        d.classify(safe_point)

def env():
    total = 0.0
    for district in data:
        total += district.Margin
    return total / len(data)