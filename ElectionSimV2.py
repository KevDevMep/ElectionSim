import csv
import random as r
import matplotlib.pyplot as plt
# Meant for a unlabeled CSV

expected = lambda n: min(max((1 + 10* n) / 2, 0), 1)

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

    def to_string(self):
        print(f'CD: {self.CD}, Margin: {self.Margin:.2%}, WhitePct: {self.WhitePct:.2%}, MinorityPct: {self.MinorityPct:.2%}, BlackPct: {self.BlackPct:.2%}, HispanicPct: {self.HispanicPct:.2%}, PacificPct: {self.PacificPct:.2%}, NativePct: {self.NativePct:.2%}')

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

print("Election Shifter")
print("+ numbers for Democrats, - numbers for Republicans")
print("This version is for unlabeled data")

filename = input("Filename (csv file only): ")
data = []
with open(filename, newline='') as csvfile:
    districtreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in districtreader:
        d_expected = expected(float(row['Margin']))
        d = district(str(i), float(row['Margin']), float(d_expected), float(row['WhitePct']), float(row['MinorityPct']), float(row['BlackPct']), float(row['HispanicPct']), float(row['PacificPct']), float(row['AsianPct']), float(row['NativePct']))
        data.append(d)
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
                            if n < d.Expected:
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
            sd = sorted(data, key=lambda n: n.Margin)
            half = seats // 2
            sd[half].to_string()
            type = input("Again? ")
        case "3":
            group = input("Racial Group (W: White, B: Black, H: Hispanic, P: Pacific, A: Asian, N: Native): ")
            shift_amount = float(input("Shift Amount (As Decmial): "))
            shifter(data, shift_amount, group)
            type = input("Again? ")
        case _:
            print("End")
            break