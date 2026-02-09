import csv
import random as r
import matplotlib.pyplot as plt
# Meant for a unlabeled CSV

expected = lambda n: min(max((1 + (1 / safe_point) * n) / 2, 0), 1)

class district:
    def __init__(self,cd, margin, expected, whitePct, minorityPct, blackPct, hispanicPct, pacificPct, asianPct, nativePct):
        self.CD = cd
        self.Margin = margin
        self.Expected = expected
        self.Flipped = False
        self.WhitePct = whitePct
        self.MinorityPct = minorityPct
        self.BlackPct = blackPct
        self.HispanicPct = hispanicPct
        self.PacificPct = pacificPct
        self.AsianPct = asianPct
        self.NativePct = nativePct
        self.Majority = ""

    def to_string(self):
        print(f'CD: {self.CD}, Margin: {self.Margin:.2%}, WhitePct: {self.WhitePct:.2%}, MinorityPct: {self.MinorityPct:.2%}, BlackPct: {self.BlackPct:.2%}, HispanicPct: {self.HispanicPct:.2%}, PacificPct: {self.PacificPct:.2%}, NativePct: {self.NativePct:.2%}, Majority: {self.Majority}')

    def shift(self, shift_amount, group = ""):
        if shift_amount != 0:
            ajusted = shift_amount
            match group:
                case 'W':
                    ajusted *= self.WhitePct
                case 'B':
                    ajusted *= self.BlackPct
                case 'H':
                    ajusted *= self.HispanicPct
                case 'P':
                    ajusted *= self.PacificPct
                case 'A':
                    ajusted *= self.AsianPct
                case 'N':
                    ajusted *= self.NativePct
                case _:
                    ajusted *= 1
            if ajusted > 0:
                if self.Margin < 0 and -self.Margin < ajusted:
                    self.Flipped = True
            else:
                if self.Margin > 0 and -self.Margin > ajusted:
                    self.Flipped = True
            self.Margin = max(min((self.Margin + ajusted), 1), -1)
            self.Expected = expected(self.Margin)

    def flip(self):
        self.Flipped = not self.Flipped

    def majority(self):
        if self.WhitePct > .5:
            self.Majority = "White"
        elif self.HispanicPct > self.WhitePct and self.HispanicPct > self.BlackPct and self.HispanicPct > self.AsianPct and self.HispanicPct > self.NativePct and self.HispanicPct > self.PacificPct:
            self.Majority = "Hispanic"
        elif self.BlackPct > self.WhitePct and self.BlackPct > self.AsianPct and self.BlackPct > self.NativePct and self.BlackPct > self.PacificPct:
            self.Majority = "Black"
        elif self.AsianPct > self.WhitePct and self.AsianPct > self.NativePct and self.AsianPct > self.PacificPct:
            self.Majority = "Asian"
        elif self.NativePct > self.WhitePct and self.NativePct > self.PacificPct:
            self.Majority = "Native"
        elif self.PacificPct > self.WhitePct:
            self.Majority = "Pacific"
        else:
            self.Majority = "Minority"

def shifter(data, shift_amount, group = ""):
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
        if d.Margin > safe_point:
            d_stats['D_Safe'] = d_stats.get('D_Safe', 0) + 1
        elif d.Margin > 0:
            d_stats['D_Comp'] = d_stats.get('D_Comp', 0) + 1
        elif d.Margin < -safe_point:
            d_stats['R_Safe'] = d_stats.get('R_Safe', 0) + 1
        else:
            d_stats['R_Comp'] = d_stats.get('R_Comp', 0) + 1
        
        d_stats[d.Majority] = d_stats.get(d.Majority, 0) + 1

    print(f"Expected: {total}")
    print(f"D_Safe: {d_stats['D_Safe']}, D_Comp: {d_stats['D_Comp']}, R_Comp: {d_stats['R_Comp']}, R_Safe: {d_stats['R_Safe']}")
    print(f"White: {d_stats['White']}, Black: {d_stats['Black']}, Hispanic: {d_stats['Hispanic']}, Asian: {d_stats['Asian']}, Native: {d_stats.get('Native', 0)}, Pacific: {d_stats.get('Pacific', 0)}, Minority: {d_stats['Minority']}")

print("Election Shifter")
print("+ numbers for Democrats, - numbers for Republicans")
print("This version is for unlabeled data")

preload = input("Preload (Y/N)? ")

if preload == 'Y':
    settings = input("Settings File (txt file): ")
    with open(settings, 'r', encoding="utf-8") as f:
        filename = f.readline().strip()
        safe_point = float(f.readline().strip())
else:
    filename = input("Filename (csv file only): ")
    safe_point = float(input("Safe Point (Decmial): "))

data = []
with open(filename, newline='') as csvfile:
    districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in districtreader:
        d_expected = expected(float(row['Margin']))
        d = district(str(i), float(row['Margin']), float(d_expected), float(row['WhitePct']), float(row['MinorityPct']), float(row['BlackPct']), float(row['HispanicPct']), float(row['PacificPct']), float(row['AsianPct']), float(row['NativePct']))
        d.majority()
        data.append(d)
        i += 1

seats = len(data)
type = input("0 for Simulator, 1 for Uniform Shifter, 2 for Tipping Point: , 3 for Coalition Builder, 4 for Stats, 5 for Export: ")
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
                    elif d_expected != 0:
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
                                districts[c.CD] = districts.get(c.CD, 0) + 1
                        results[trail_total] = results.get(trail_total, 0) + 1
                        writer.writerow({'trail': i + 1, 'd_seats': trail_total, 'r_seats': seats - trail_total, 'winner': 1 if trail_total > (seats - trail_total) else 0})
                        if trail_total > (seats - trail_total):
                            wins += 1

                with open('District Results.csv', 'w', newline='') as csvfile:
                    fieldnames = ['CD', 'd_wins', 'r_wins']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for d in districts:
                        writer.writerow({'CD': d, 'd_wins': districts[d], 'r_wins': trails - districts[d]})

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
                    writer.writerow({ 'CD': d.CD, 'Margin': d.Margin,'Expected': d.Expected, 'WhitePct': d.WhitePct, 'MinorityPct': d.MinorityPct, 'BlackPct': d.BlackPct, 'HispanicPct': d.HispanicPct, 'PacificPct': d.PacificPct, 'AsianPct': d.AsianPct, 'NativePct': d.NativePct, 'Majority': d.Majority })
            type = input("Again? ")
        case _:
            print("End")
            break