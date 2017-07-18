import math

class payment:
    def __init__(self, loan, maturity, grace, rate1, rate2, rate3, pay_period2, pay_period3, prepay, prepay_start, prepay_end):
        self.loan = loan
        self.maturity = maturity
        self.term = maturity * 12
        self.grace = grace
        self.rate1 = rate1
        self.rate2 = rate2
        self.rate3 = rate3
        self.pay_period2 = pay_period2
        self.pay_period3 = pay_period3
        self.prepay = prepay
        self.prepay_start = prepay_start
        self.prepay_end = prepay_end
        self.balance = [None] * (maturity * 12 + 1)
        self.prepay_balance = [None] * (maturity * 12 + 1)
        self.interest = [None] * (maturity * 12)
        self.prepay_interest = [None] * (maturity * 12)
        self.principal = [None] * (maturity * 12)
        self.prepay_principal = [None] * (maturity * 12)
        self.sum_interest = [None] * (maturity * 12)
        self.sum_principal = [None] * (maturity * 12)
        self.sum_prepay_interest = [None] * (maturity * 12)
        self.sum_prepay_principal = [None] * (maturity * 12)
        self.PMT = [None] * (maturity * 12)
        self.prepay_PMT = [None] * (maturity * 12)
        self.new_interest = [None] * maturity
        self.new_principal = [None] * maturity
        self.new_payment = [None] * maturity
        self.new_prepay_interest = [None] * maturity
        self.new_prepay_principal = [None] * maturity
        self.new_prepay_payment = [None] * maturity
        self.balance[0] = self.loan
        self.prepay_balance[0] = self.loan
        self.sum_period1 = 0.0
        self.sum_period2 = 0.0
        self.sum_period3 = 0.0
        self.sum_prepay_period1 = 0.0
        self.sum_prepay_period2 = 0.0
        self.sum_prepay_period3 = 0.0
        self.prepay_count = 0
        self.sumInterest = 0.0
        self.sumPrincipal = 0.0
        self.prepay_sumInterest = 0.0
        self.prepay_sumPrincipal = 0.0
        print("CHECK--> loan:", self.loan, "maturity:", self.maturity, "term:", self.term, "rate1:", self.rate1,
              "rate2:", self.rate2, "rate3:", self.rate3, "pay period2:", self.pay_period2, "pay period3", self.pay_period3,
              "prepay", self.prepay, "prepay_start", self.prepay_start, "prepay_end:", self.prepay_end)

    def PVAIF(self, term, rate):
        r = rate / 12.0
        return ((1.0 + r) ** term - 1.0) / (r * (1.0 + r) ** term )

    def CAM(self, balance, term, rate):

        return balance / self.PVAIF(term, rate)

    def calculate_wholeterm(self):
        outstanding = 0.0
        prepay_outstanding = 0.0
        r = 0.0
        n = 0.0

        for i in range(1,self.term + 1):
            # setting rates and term for different period
            if i == 1:
                r = self.rate1/100.0
                n = self.term
                outstanding = self.balance[0]
                prepay_outstanding = self.prepay_balance[0]
                print("in period 1!")

            if i == self.pay_period2 and self.pay_period2 != self.term:
                r = self.rate2/100.0
                n = self.term + 1 - self.pay_period2
                outstanding = self.balance[self.pay_period2 - 1]
                prepay_outstanding = self.prepay_balance[self.pay_period2 - 1]
                print("in period 2!")

            if i == self.pay_period3 and self.pay_period3 != self.term:
                r = self.rate3/100.0
                n = self.term + 1 - self.pay_period3
                outstanding = self.balance[self.pay_period3 - 1]
                prepay_outstanding = self.prepay_balance[self.pay_period3 - 1]
                print("in period 3!")

            if i == self.grace + 1:
                n = self.term - self.grace

            self.PMT[i-1] = self.CAM(outstanding, n, r)
            self.prepay_PMT[i-1] = self.CAM(prepay_outstanding, n, r)

            if i <= self.grace:
                self.PMT[i-1] = self.balance[i - 1] * r / 12.0
                self.prepay_PMT[i-1] = self.prepay_balance[i - 1] * r / 12.0

            # calculate total payment in different period
            self.interest[i - 1] = self.balance[i - 1] * r / 12.0
            self.sumInterest = self.sumInterest + self.interest[i - 1]
            self.sum_interest[i-1] = self.sumInterest
            self.principal[i-1] = self.PMT[i-1] - self.interest[i-1]
            self.sumPrincipal = self.sumPrincipal + self.principal[i-1]
            self.sum_principal[i-1] = self.sumPrincipal

            if i == self.pay_period2:
                self.sum_period1 = self.sum_interest[i-2] + self.sum_principal[i-2]
                self.sum_prepay_period1 = self.sum_prepay_interest[i-2] + self.sum_prepay_principal[i-2]

            if i == self.pay_period3:
                self.sum_period2 = self.sum_interest[i-2] + self.sum_principal[i-2] - self.sum_period1
                self.sum_prepay_period2 = self.sum_prepay_interest[i-2] + self.sum_prepay_principal[i-2] - self.sum_prepay_period1
            if i == self.term:
                self.sum_period3 = self.sum_interest[i-1] + self.sum_principal[i-1]  - self.sum_period2
                self.sum_prepay_period3 = self.sum_prepay_interest[i-2] + self.sum_prepay_principal[i-2] - self.sum_prepay_period2

            self.balance[i] = self.balance[i - 1] - self.PMT[i - 1] + self.interest[i - 1]

            if i < self.prepay_start and self.prepay != 0:
                self.prepay_interest[i-1] = self.interest[i-1]
                self.prepay_principal[i-1] = self.principal[i-1]
                self.prepay_balance[i] = self.balance[i]
                self.sum_prepay_interest[i-1] = self.sum_interest[i-1]
                self.sum_prepay_principal[i-1] = self.sum_principal[i-1]
                self.prepay_sumInterest = self.sumInterest
                self.prepay_sumPrincipal = self.sumPrincipal
                self.prepay_count += 1

            if i >= self.prepay_start and self.prepay_balance[i-1] > 0.0:
                if i > self.prepay_end:
                    self.prepay =0

                self.prepay_interest[i - 1] = self.prepay_balance[i - 1] * r / 12.0
                self.prepay_sumInterest = self.prepay_sumInterest + self.prepay_interest[i - 1]
                self.sum_prepay_interest[i-1] = self.prepay_sumInterest

                if self.prepay + self.prepay_PMT[i-1] - self.prepay_interest[i-1] > self.prepay_balance[i-1]:
                    self.prepay = self.prepay_balance[i-1] - self.prepay_PMT[i-1] + self.prepay_interest[i-1]

                self.prepay_principal[i-1] = self.prepay_PMT[i-1] - self.prepay_interest[i-1] + self.prepay
                self.prepay_sumPrincipal = self.prepay_sumPrincipal + self.prepay_principal[i-1]
                self.prepay_balance[i] = self.prepay_balance[i - 1] - self.prepay_principal[i-1]
                self.prepay_count += 1

            for count in range(self.prepay_count+1, self.term + 1):
                self.prepay_balance[count] = 0
                self.prepay_interest[count - 1] = 0
                self.prepay_principal[count - 1] = 0
                self.sum_prepay_interest[count - 1] = self.sum_prepay_interest[self.prepay_count - 1]
                self.sum_prepay_principal[count - 1] = self.prepay_balance[0]

            print("CHECK REGULAR balance:", self.balance[i], "interest:", self.interest[i-1], "sum interest:",
                  self.sum_interest[i-1], "principal", self.principal[i-1], "sum principal:", self.sum_principal[i-1], "PMT", self.PMT[i-1])

            print("CHECK PREPAY balance:", self.prepay_balance[i], "interest:", self.prepay_interest[i-1],
                  "sum interest:", self.sum_prepay_interest[i-1], "principal", self.prepay_principal[i-1],
                  "sum principal:", self.sum_prepay_principal[i-1], "PMT", self.prepay_PMT[i-1])

    def period_conversion(self, new_period, interest, principal, new_interest, new_principal, new_payment): ## CHECK!!!!
        sum_interest = 0.0
        sum_principal = 0.0
        for i in range(self.term):
            sum_interest = sum_interest + interest[i]
            sum_principal = sum_principal + principal[i]
            index = int(math.floor(i/new_period))
            if i % new_period == (new_period - 1):
                new_interest[index] = sum_interest
                new_principal[index] = sum_principal
                new_payment[index] = sum_interest + sum_principal
                sum_interest = 0
                sum_principal = 0

if __name__ == "__main__":
    sample1 = payment(10000000, 30, 1, 2, 3, 4, 20, 100, 10000, 30, 200)

    sample1.calculate_wholeterm()
