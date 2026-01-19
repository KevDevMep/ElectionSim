import csv
import random as r
import matplotlib.pyplot as plt
# Meant for a unlabeled CSV

def shifter(data, shift_amount, group = ""):
    demA, demB, totalA, totalB = 0, 0, 0, 0
    for d in data:
        totalA += data[d]['Expected']
        if data[d]['Margin'] > 0:
            demA += 1
        ajusted = shift_amount
        match group:
            case 'W':
                ajusted *= data[d]['WhitePct']
            case 'B':
                ajusted *= data[d]['BlackPct']
            case 'H':
                ajusted *= data[d]['HispanicPct']
            case 'P':
                ajusted *= data[d]['PacificPct']
            case 'A':
                ajusted *= data[d]['AsianPct']
            case 'N':
                ajusted *= data[d]['NativePct']
            case _:
                ajusted *= 1
        data[d]['Margin'] += ajusted
        data[d]['Expected'] = expected(data[d]['Margin'])
        totalB += data[d]['Expected']
        if data[d]['Margin'] > 0:
            demB += 1
    print(f"Before Shift: (D: {demA}, R: {len(data) - demA}, E: {totalA:.2f})")
    print(f"After Shift: (D: {demB},R: {len(data) - demB}, E: {totalB:.2f}) with {demB - demA} flipped seats")

print("Election Shifter")
print("+ numbers for Democrats, - numbers for Republicans")
print("This version is for unlabeled data")

filename = input("Filename (csv file only): ")
expected = lambda n: min(max((1 + 10* n) / 2, 0), 1)
data = {}
with open(filename, newline='') as csvfile:
    districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in districtreader:
        d_expected = expected(float(row['Margin']))
        data[i] = {"Margin": float(row['Margin']), "Expected": d_expected, "WhitePct": float(row['WhitePct']), "MinorityPct": float(row['MinorityPct']), "BlackPct": float(row['BlackPct']), "HispanicPct": float(row['HispanicPct']), "PacificPct":float(row['PacificPct']), "AsianPct": float(row['AsianPct']), "NativePct": float(row['NativePct'])}
        i += 1

seats = len(data)
type = input("0 for Simulator, 1 for Uniform Shifter, 2 for Tipping Point: , 3 for Coalition Builder: ")
while True:
    match type:
        case "0":
                trails = int(input('How many Times? '))
                results = {}
                total, wins = 0, 0
                with open('results.csv', 'w', newline='') as csvfile:
                    fieldnames = ['trail', 'd_seats', 'r_seats', 'winner']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for i in range(trails):
                        trail_total = 0
                        for d in data:
                            n = r.random()
                            if n < data[d]['Expected']:
                                total += 1
                                trail_total += 1
                        results[trail_total] = results.get(trail_total, 0) + 1
                        writer.writerow({'trail': i + 1, 'd_seats': trail_total, 'r_seats': seats - trail_total, 'winner': 1 if trail_total > (seats - trail_total) else 0})
                        if trail_total > (seats - trail_total):
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
            half = seats // 2
            print(f'Tipping Point Seat Margin: {sd[half]['Margin']:.2%}')
            type = input("Again? ")
        case "3":
            group = input("Racial Group (W: White, B: Black, H: Hispanic, P: Pacific, A: Asian, N: Native): ")
            shift_amount = float(input("Shift Amount (As Decmial): "))
            shifter(data, shift_amount, group)
            type = input("Again? ")
        case _:
            print("End")
            break