import pyomo.environ as pyo
class CashBackMachine():
    def __init__(self,c):
        self.model = pyo.ConcreteModel()
        self.model.c = pyo.Set(initialize= c)
        self.model.x = pyo.Var(range(1,len(c) + 1), domain= pyo.Binary)
        self.model.obj = pyo.Objective(expr= self.objective_func(), sense= pyo.maximize)

    def objective_func(self):
        return pyo.summation(self.model.c,self.model.x)

    def constraint(self,val):
        return pyo.summation(self.model.c,self.model.x) <= val

    def approximate(self,val):
        self.model.constr = pyo.Constraint(expr= self.constraint(val))
        opt = pyo.SolverFactory("cplex_direct")
        opt.solve(self.model)
        
        return (self.model,val)

c = list(map(float,input("Purchases: ").split()))
# c = list(map(float,"3527.50 2129.19 2677 3983.73 7710 6737 2137 1980.48 9300 7698.49 2499 12923 3196 1628.96 3434.91 2059 3246.59 3748.50 7178 11123 2200 1737.40 5400 5450 8136".split()))
sample = CashBackMachine(c)
model,expected_value = sample.approximate(float(input("Cashback Value: ")))
# model,expected_value = sample.approximate(13479.45)

print(f"Expected cash back value: {expected_value}")
print(f"Actual cashback value: {model.obj()}")
print(f"Difference: {round(expected_value - model.obj(),2)}")
_,used = zip(*(filter(lambda a: a[0] == 1.0,zip((model.x[i]() for i in model.x),c))))
print(f"Optimal Purchases set to recover cashback: {' '.join(map(str,used))}")

# 3569.68 1806.94 2079 3745 2134.08 1880.03 2052 2498.99 2045.51
# 7373.89