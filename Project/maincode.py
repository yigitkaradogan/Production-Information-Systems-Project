import gurobipy as gp
from gurobipy import GRB
import DemandForecast

demand_data_air = DemandForecast.demand_data_air
demand_data_pro = DemandForecast.demand_data_pro

# Parameters
h_a = 0.25  # Inventory holding cost for MacBook Air at period t
h_p = 0.28  # Inventory holding cost for MacBook Pro at period t
pi_a = 0.5  # Back ordering cost for MacBook Air at period t
pi_p = 0.58  # Back ordering cost for MacBook Pro at period t
p_a = 1/20  # Production time for MacBook Air (in hours per unit)
p_p = 1/15  # Production time for MacBook Pro (in hours per unit)
o = 12.5  # Overtime cost per hour
p_f = 85  # Procurement cost from fast supplier per unit
p_s_1 = 78  # Procurement cost from slow supplier per unit in periods 1-4
p_s_2 = 67  # Procurement cost from slow supplier per unit in periods 5-13
tau_f = 0  # Lead time for fast supplier in weeks
tau_s = 2  # Lead time for slow supplier in weeks
w = 0.1  # Inventory holding cost for chips per unit

# Forecasted demand data
d_a = DemandForecast.compute_forecast(demand_data_air)
d_p = DemandForecast.compute_forecast(demand_data_pro)

m = gp.Model('IE 376 Project 1 / Macbook Production')

# Decision Variables
I_a = m.addVars(range(0, 14), lb=-1e20, name='I_a', vtype=GRB.INTEGER)  # Inventory level of MacBook Air in period t
I_p = m.addVars(range(0, 14), lb=-1e20, name='I_p', vtype=GRB.INTEGER)  # Inventory level of MacBook Pro in period t
I_a_plus = m.addVars(range(1, 14), lb=0, name='I_a_plus', vtype=GRB.INTEGER)  # Quantity of MacBook Air ordered in period t
I_a_minus = m.addVars(range(1, 14), lb=0, name='I_a_minus', vtype=GRB.INTEGER)   # Quantity of MacBook Air back ordered in period t
I_p_plus = m.addVars(range(1, 14), lb=0, name='I_p_plus', vtype=GRB.INTEGER)  # Quantity of MacBook Pro ordered in period t
I_p_minus = m.addVars(range(1, 14), lb=0, name='I_p_minus', vtype=GRB.INTEGER)  # Quantity of MacBook Pro back ordered in period t
P_a = m.addVars(range(1, 14), lb=0, name='P_a', vtype=GRB.INTEGER)   # Production quantity of MacBook Air in period t
P_p = m.addVars(range(1, 14), lb=0, name='P_p', vtype=GRB.INTEGER)  # Production quantity of MacBook Pro in period t
Q_f = m.addVars(range(1, 14), lb=0, name='Q_f', vtype=GRB.INTEGER)  # Quantity ordered from fast supplier in period t
Q_s = m.addVars(range(-1, 14), lb=0, name='Q_s', vtype=GRB.INTEGER)  # Quantity ordered from slow supplier in period t
S_t = m.addVars(range(0, 14), lb=0, name='S_t', vtype=GRB.INTEGER)  # Chip inventory level in period t
O_t = m.addVars(range(0, 14), lb=0, name='O_t', vtype=GRB.INTEGER)  # Overtime amount in period t
C_t = m.addVars(range(0, 14), lb=0, name='C_t', vtype=GRB.INTEGER)  # Amount of workforce in hours period t

# Objective Function
m.setObjective(
    gp.quicksum(h_a * I_a_plus[t] + h_p * I_p_plus[t] for t in range(1, 13)) +
    gp.quicksum(pi_a * I_a_minus[t] + pi_p * I_p_minus[t] for t in range(1, 13)) +
    gp.quicksum(O_t[t] * o + S_t[t] * w for t in range(1, 14)) +
    gp.quicksum(p_f * Q_f[t] for t in range(1, 14)) +
    gp.quicksum(p_s_1 * Q_s[t] if t < 5 else p_s_2 * Q_s[t] for t in range(1, 14)) +
    110 * I_a_minus[13] + 10 * I_a_plus[13] + 130 * I_p_minus[13] + 13 * I_p_plus[13],
    GRB.MINIMIZE)

for constraint, val in [(I_a[0], 1300), (I_p[0], 1900), (Q_s[-1], 106000), (Q_s[0], 106000), (S_t[0], 2000),
                (P_a[1], 47500), (P_p[1], 25000), (O_t[0], 0), (C_t[0], 0)]:
    m.addConstr(constraint == val)

for t in range(1, 14):
    m.addConstr(I_a[t] == I_a[t-1] + P_a[t] - d_a[t])
    m.addConstr(I_p[t] == I_p[t-1] + P_p[t] - d_p[t])
    m.addConstr(I_a[t] == I_a_plus[t] - I_a_minus[t])
    m.addConstr(I_p[t] == I_p_plus[t] - I_p_minus[t])
    m.addConstr(p_a * P_a[t] + p_p * P_p[t] <= C_t[t] + O_t[t])
    m.addConstr(S_t[t] == S_t[t - 1] + Q_f[t - tau_f] + Q_s[t - tau_s] - P_a[t] - P_p[t])
    m.addConstr(Q_s[t] <= 95000)

for t in range(1, 6):
    m.addConstr(C_t[t] <= 4275)
    m.addConstr(O_t[t] <= 2375)
for t in range(6, 14):
    m.addConstr(C_t[t] <= 4500)
    m.addConstr(O_t[t] <= 2500)

m.optimize()

if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print(f'{v.varName}: {v.x}')
else:
    print("Optimization did not succeed.")