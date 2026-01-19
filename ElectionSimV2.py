import csv
import random as r
import matplotlib.pyplot as plt
# Meant for a unformated CSV

def shifter(dict, shift_amount, group = ""):
    demA, demB, totalA, totalB = 0, 0, 0, 0
    for d in dict:
        totalA += dict[d]['Expected']
        if dict[d]['Margin'] > 0:
            demA += 1
        ajusted = shift_amount
        match group:
            case 'White':
                ajusted *= dict[d]['WhitePct']
            case 'Black':
                ajusted *= dict[d]['BlackPct']
            case 'Hispanic':
                ajusted *= dict[d]['HispanicPct']
            case 'Asian':
                ajusted *= dict[d]['AsianPct']
            case 'Native':
                ajusted *= dict[d]['NativePct']
            case _:
                ajusted *= 1
        dict[d]['Margin'] += ajusted
        dict[d]['Expected'] = expected(dict[d]['Margin'])
        totalB += dict[d]['Expected']
        if dict[d]['Margin'] > 0:
            demB += 1
    print(f"Before Shift: (D: {demA}, R: {len(dict) - demA}, E: {totalA:.2f})")
    print(f"After Shift: (D: {demB},R: {len(dict) - demB}, E: {totalB:.2f}) with {demB - demA} flipped seats")

print("Election Shifter")
print("+ numbers for Democrats, - numbers for Republicans")
filename = input("Filename (csv file only): ")
type = input("0 for Simulator, 1 for Uniform Shifter, 2 for Tipping Point: , 3 for Coalition Builder: ")
data = {}
expected = lambda n: min(max((1 + 10* n) / 2, 0), 1)

with open(filename, newline='') as csvfile:
    districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in districtreader:
        d_expected = expected(float(row['Margin']))
        data[i] = {"Margin": float(row['Margin']), "Expected": d_expected, "MinorityPct": float(row['MinorityPct']), "WhitePct": float(row['WhitePct']), "BlackPct": float(row['BlackPct']), "HispanicPct": float(row['HispanicPct']), "AsianPct": float(row['AsianPct']), "NativePct": float(row['NativePct'])}
        i += 1

while True:
    match type:
        case "0":
                trails = int(input('How many Times? '))
                results = {}
                total = 0
                wins = 0
                for i in range(trails):
                    trail_total = 0
                    for d in data:
                        n = r.random()
                        if n < data[d]['Expected']:
                            total += 1
                            trail_total += 1
                    results[trail_total] = results.get(trail_total, 0) + 1
                    # print(f"{i + 1}th trail: (D: {trail_total}, R: {len(data) - trail_total})")
                    if trail_total > (len(data) - trail_total):
                        wins += 1
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
            sd = sorted(data.values(), key=lambda n: n['Margin'])
            half = len(data) // 2
            print(f'Tipping Point Seat Margin: {sd[half]['Margin']:.2%}')
            type = input("Again? ")
        case "3":
            group = input("Racial Group (White, Black, Hispanic, Asian, Native): ")
            shift_amount = float(input("Shift Amount (As Decmial): "))
            shifter(data, shift_amount, group)
            type = input("Again? ")
        case _:
            print("End")
            break