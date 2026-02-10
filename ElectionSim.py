import csv
import random as r
import matplotlib.pyplot as plt
import geopandas as gp
import district

def shifter(data, shift_amount, group = "",):
    demA, demB, totalA, totalB = 0, 0, 0, 0
    for d in data:
        totalA += d.Expected
        if d.Margin > 0:
            demA += 1
        d.shift(shift_amount, group)
        totalB += d.Expected
        if d.Margin > 0:
            demB += 1
    print(f"Before Shift: (D: {demA}, R: {len(data) - demA}, E: {totalA:.2f})")
    print(f"After Shift: (D: {demB},R: {len(data) - demB}, E: {totalB:.2f}) with {demB - demA} flipped seats")
    for d in data:
        if d.Flipped:
            d.to_string()
            d.flip()

def stats(data):
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

print("Election Shifter")
print("+ numbers for Democrats, - numbers for Republicans")

preload = input("Preload (Y/N)? ")
if preload == 'Y':
    settings = input("Settings File (txt file): ")
    with open(settings, 'r', encoding="utf-8") as f:
        filetype = f.readline().strip()
        filename = f.readline().strip()
        district.safe_point = float(f.readline().strip())
        if filetype == '0':
            dataset = f.readline().strip()
else:
    filetype = input("File Type (0 for labeled, 1 for unlabeled, 2 for geojson): ")
    filename = input("Filename: ")
    if filetype == '0':
        dataset = input("Dataset name: ")
    district.safe_point = float(input("Safe Point (Decmial): "))

data = []
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

seats = len(data)
type = input("0 for Simulator, 1 for Uniform Shifter, 2 for Tipping Point, 3 for Coalition Builder, 4 for Stats, 5 for Export, 6 for Reset: ")
while True:
    match type:
        case "0":
                trails = int(input('How many Times? '))
                results, districts = {}, {}
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
                    fieldnames = ['CD', 'Margin', 'Expected', 'WhitePct', 'MinorityPct', 'BlackPct', 'HispanicPct', 'PacificPct', 'AsianPct', 'NativePct', 'Majority', 'd_wins', 'r_wins']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for d in districts:
                        details = d.to_dict()
                        details['d_wins'] = districts[d]
                        details['r_wins'] = trails - districts[d]
                        writer.writerow(details)

                print(f'average: {total / trails}, wins: (D: {wins}, R: {trails - wins})')
                plt.figure(figsize=(16, 10))
                plt.scatter(results.keys(), results.values())
                plt.xlabel('Number of D Seats')
                plt.ylabel('Trails')
                plt.title('Simulator Results')
                plt.grid(True)
                plt.show()
                type = input("Again? ")
        case "1":
            shift_amount = float(input("Shift Amount (As Decmial): "))
            shifter(data, shift_amount)
            type = input("Again? ")
        case "2":
            sd = sorted(data, key=lambda n: n.Margin)
            half = seats // 2
            sd[half].to_string()
            type = input("Again? ")
        case "3":
            group = input("Racial Group (W: White, B: Black, H: Hispanic, P: Pacific, A: Asian, N: Native): ")
            shift_amount = float(input("Shift Amount (As Decmial): "))
            shifter(data, shift_amount, group)
            type = input("Again? ")
        case "4":
            stats(data)
            type = input("Again? ")
        case "5":
            with open('Adjusted.csv', 'w', newline='') as csvfile:
                fieldnames = ['CD', 'Margin', 'Expected', 'WhitePct', 'MinorityPct', 'BlackPct', 'HispanicPct', 'PacificPct', 'AsianPct', 'NativePct', 'Majority']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for d in data:
                    writer.writerow(d.to_dict())
            type = input("Again? ")
        case "6":
            for d in data:
                d.reset()
            type = input("Again? ")
        case _:
            print("End")
            break