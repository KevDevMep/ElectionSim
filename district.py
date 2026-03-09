safe_point = .15

expected = lambda n: min(max((1 + (1 / safe_point) * n) / 2.0, 0.0), 1.0)

class District:
    def __init__(self, cd, margin, whitePct, minorityPct, blackPct, hispanicPct, pacificPct, asianPct, nativePct):
        self.CD = cd
        self.Margin = margin
        self.Expected = 0
        self.Flipped = False
        self.WhitePct = whitePct
        self.MinorityPct = minorityPct
        self.BlackPct = blackPct
        self.HispanicPct = hispanicPct
        self.PacificPct = pacificPct
        self.AsianPct = asianPct
        self.NativePct = nativePct
        self.Majority = ""
        self.Swing = 0

    def to_string(self):
        print(f'CD: {self.CD}, Margin: {self.Margin:.2%}, Swing: {self.Swing:.2%}, Majority: {self.Majority}, WhitePct: {self.WhitePct:.2%}, MinorityPct: {self.MinorityPct:.2%}, BlackPct: {self.BlackPct:.2%}, HispanicPct: {self.HispanicPct:.2%}, AsianPct: {self.AsianPct:.2%}, NativePct: {self.NativePct:.2%}, PacificPct: {self.PacificPct:.2%}')

    def to_dict(self):
        return { 'CD': self.CD, 'Margin': self.Margin, 'Swing': self.Swing, 'Majority': self.Majority, 'WhitePct': self.WhitePct, 'MinorityPct': self.MinorityPct, 'BlackPct': self.BlackPct, 'HispanicPct': self.HispanicPct, 'AsianPct': self.AsianPct, 'NativePct': self.NativePct, 'PacificPct': self.PacificPct}

    def shift(self, shift_amount, group = "", print_ = True):
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
            if ajusted > 0 and print_:
                if self.Margin < 0 and -self.Margin < ajusted:
                    self.flip()
            else:
                if self.Margin > 0 and -self.Margin > ajusted:
                    self.flip()
            self.Margin = max(min((self.Margin + ajusted), 1), -1)
            self.expected()
            self.Swing += ajusted

    def flip(self):
        self.Flipped = not self.Flipped

    def expected(self):
        self.Expected = expected(self.Margin)

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

    def reset(self):
        self.Margin -= self.Swing
        self.Swing = 0