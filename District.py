expected = lambda n, safe_point: min(max((1 + (1 / safe_point) * n) / 2.0, 0.0), 1.0)

class District:
    def __init__(self, cd, demPct, repPct, whitePct, minorityPct, blackPct, hispanicPct, pacificPct, asianPct, nativePct):
        self.CD = cd
        self.DemPct = demPct
        self.RepPct = repPct
        self.Expected = 0
        self.WhitePct = whitePct
        self.MinorityPct = minorityPct
        self.BlackPct = blackPct
        self.HispanicPct = hispanicPct
        self.PacificPct = pacificPct
        self.AsianPct = asianPct
        self.NativePct = nativePct
        self.Margin = 0.0
        self.Majority = ''
        self.Class = ''

    def to_string(self):
        return(f'CD: {self.CD}, Margin: {self.Margin:.2%}, Majority: {self.Majority}, WhitePct: {self.WhitePct:.2%}, MinorityPct: {self.MinorityPct:.2%}, BlackPct: {self.BlackPct:.2%}, HispanicPct: {self.HispanicPct:.2%}, AsianPct: {self.AsianPct:.2%}, NativePct: {self.NativePct:.2%}, PacificPct: {self.PacificPct:.2%}')

    def to_dict(self):
        return { 'CD': self.CD, 'Margin': self.Margin, 'Majority': self.Majority, 'WhitePct': self.WhitePct, 'MinorityPct': self.MinorityPct, 'BlackPct': self.BlackPct, 'HispanicPct': self.HispanicPct, 'AsianPct': self.AsianPct, 'NativePct': self.NativePct, 'PacificPct': self.PacificPct}

    def shift(self, shift_amount, group = ''):
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
            self.Margin = max(min((self.Margin + ajusted), 1), -1)

    def expected(self, safe_point):
        self.Expected = expected(self.Margin, safe_point)

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

    def classify(self, safe_point: float):
        if self.Margin > safe_point:
            self.Class = 'D'
        elif self.Margin < -safe_point:
            self.Class = 'R'
        else:
            self.Class = 'Comp'

    def reset(self):
        self.Margin = self.DemPct - self.RepPct