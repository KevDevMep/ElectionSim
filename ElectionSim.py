import csv
import random as r
import matplotlib.pyplot as plt

print("Election Shifter")
print("+ numbers for Democrats, - numbers for Republicans")
data = {}
type = input("0 for Simulator, 1 for Shifter, 2 for Tipping Point: ")
filename = input("Filename (csv file only): ")


with open(filename, newline='') as csvfile:
    districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in districtreader:
        cd = f"{row['State']}-{row['Id']}"
        data[cd] = {"Margin": float(row['24_Pres']), "Flipped": False, "Expected": float(row['24_Expected'])}

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
                    results[str(trail_total)] = results.get(str(trail_total), 0) + 1
                    # print(f"{i + 1}th trail: (D: {trail_total}, R: {len(data) - trail_total})")
                    if trail_total > (len(data) - trail_total):
                        wins += 1
                print(f'average: {total / trails}, wins: (D: {wins}, R: {trails - wins})')
                sorted_keys = sorted(results)
                sorted_vals = [results[k] for k in sorted_keys]
                plt.figure(figsize=(14, 10))
                plt.scatter(sorted_keys, sorted_vals)
                plt.xlabel('Number of D Seats')
                plt.ylabel('Trails')
                plt.title('Simulator Results')
                plt.grid(True)
                plt.show()
                type = input("Again? ")
        case "1":
            demA, demB, totalA, totalB = 0, 0, 0, 0
            expected = lambda n: min(max((1 + 10* n) / 2, 0), 1)
            shift = float(input("Shift Amount (As Decmial): "))
            for d in data:
                totalA += data[d]['Expected']
                if data[d]['Margin'] > 0:
                    demA += 1
                if shift > 0:
                    if data[d]['Margin'] < 0 and -data[d]['Margin'] < shift:
                        data[d]['Flipped'] = True
                elif shift < 0:
                    if data[d]['Margin'] > 0 and -data[d]['Margin'] > shift:
                        data[d]['Flipped'] = True
                data[d]['Margin'] += shift
                data[d]['Expected'] = expected(data[d]['Margin'])
                totalB += data[d]['Expected']
                if data[d]['Margin'] > 0:
                    demB += 1
            print(f"Before Shift: (D: {demA}, R: {len(data) - demA}, E: {totalA:.2f})")
            print(f"After Shift: (D: {demB},R: {len(data) - demB}, E: {totalB:.2f}) with {demB - demA} flipped seats")
            print("Flipped Seats: ")
            for d in data:
                if data[d]['Flipped']:
                    print(f"{d}: {data[d]['Margin']:.2%}")
                data[d]['Flipped'] = False
            type = input("Again? ")
        case "2":
            sd = sorted(data.values(), key=lambda n: n['Margin'])
            half = len(data) // 2
            print(f'Tipping Point Seat Margin: {sd[half]['Margin']:.2%}')
            type = input("Again? ")
        case _:
            print("End")
            break