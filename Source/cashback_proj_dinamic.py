class CashbackMachine():
    def __init__ (self,costList,cashbackValue):
        self.costs = list(filter(lambda a: a / 100 >= 0,map(lambda b: int(float(b) * 100),costList.split())))
        self.cashback = int(cashbackValue * 100)
    
    def getValuesApproximatingCashback(self):
        used = []
        # Подборка наиболее близкого числа к заданной величине cashback
        D = [[0 for j in range(len(self.costs) + 1)] for i in range(self.cashback + 1)]

        for j in range(1,len(self.costs) + 1):
            for w in range(1,self.cashback + 1):
                D[w][j] = D[w][j - 1]
                if self.costs[j - 1] <= w:
                    D[w][j] = max(D[w][j], D[w - self.costs[j - 1]][j - 1] + self.costs[j - 1])

        # Разложение наиболее близкой суммы к cashback по произведенным операциям
        i,j = (len(D) - 1, len(D[0]) - 1)
        while j - 1 >= 0:          
            if D[i][j - 1] != D[i][j]:
                used.append(float(self.costs[j - 1]) / 100)
                i -= self.costs[j - 1]
            j -= 1
        
        approximatedSum = sum(used)
        remainder = round((float(self.cashback) / 100 - approximatedSum),2)
        
        return (used,approximatedSum,remainder)

# Пример
cost_list = "3527.50 2129.19 2677 3983.73 7710 6737 2137 1980.48 9300 7698.49 2499 12923 3196 1628.96 3434.91 2059 3246.59 3748.50 7178 11123 2200 1737.40 5400 5450 8136"
cash_back = 13479.45

sample = CashbackMachine(cost_list,cash_back)
ans = sample.getValuesApproximatingCashback()

print(f"Expected cash back value: {cash_back}")
print(f"Actual cashback value: {ans[1]}")
print(f"Difference: {ans[2]}")
print(f"Optimal Purchases set to recover cashback: {' '.join(map(str,ans[0]))}")