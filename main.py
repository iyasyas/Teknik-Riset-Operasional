# ========================================
# OPTIMASI TRANSPORTASI PT LOGISTIK PRIMA
# Menggunakan Linear Programming (PuLP)
# ========================================

import pulp

# Data
supply = {'W1':1614, 'W2':1883, 'W3':1270, 'W4':1188, 'W5':1082, 'W6':1112}
demand = {'S1':882, 'S2':1073, 'S3':818, 'S4':877, 'S5':821, 'S6':782, 'S7':813, 'S8':811, 'S9':814, 'S10':801, 'S11':824, 'S12':843}

costs = {
    'W1': [8.7]*12,
    'W2': [7.9]*12,
    'W3': [8.5]*12,
    'W4': [7.8]*12,
    'W5': [7.3]*12,
    'W6': [8.6]*12
}

# Inisialisasi problem minimisasi
model = pulp.LpProblem("Optimasi_Distribusi_PT_Logistik_Prima", pulp.LpMinimize)

# Variabel keputusan x[i][j]
x = pulp.LpVariable.dicts("x", ((i, j) for i in supply for j in demand), lowBound=0, cat='Continuous')

# Fungsi tujuan
model += pulp.lpSum(costs[i][list(demand.keys()).index(j)] * x[(i, j)] for i in supply for j in demand)

# Kendala supply
for i in supply:
    model += pulp.lpSum(x[(i, j)] for j in demand) <= supply[i], f"Supply_{i}"

# Kendala demand
for j in demand:
    model += pulp.lpSum(x[(i, j)] for i in supply) == demand[j], f"Demand_{j}"

# Jalankan solver
model.solve(pulp.PULP_CBC_CMD(msg=False))

# Cetak hasil
print("Status:", pulp.LpStatus[model.status])
print("\nDistribusi Optimal:")
for i in supply:
    for j in demand:
        if x[(i, j)].value() > 0:
            print(f"{i} -> {j}: {x[(i, j)].value():.2f} unit")

total_cost = pulp.value(model.objective)
print(f"\nTotal Biaya Minimum: Rp {total_cost:,.2f} ribu")
