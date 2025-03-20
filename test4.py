import cvxpy as cp 
import numpy as np

np.random.seed(1)
x1 = cp.Variable()
x2 = cp.Variable()

cost = 0.06*x1 + 0.08*x2

constraints = [
    x1 + x2 == 100000,  # Tổng ngân sách
    0.10 * x1 + 0.15 * x2 <= 12000,  # Rủi ro tối đa
    x1 >= 0,  # Không thể đầu tư số âm vào tài sản 1
    x2 >= 0  # Không thể đầu tư số âm vào tài sản 2
]

prob = cp.Problem(cp.Maximize(cost),constraints)
prob.solve()

print("Optimal expected return:", prob.value)
print("Optimal investment in asset 1:", x1.value)
print("Optimal investment in asset 2:", x2.value)

# In giá trị dual solution (Lagrange multipliers)
print("Dual solutions (Lagrange multipliers):")
for i, cons in enumerate(prob.constraints):
    print(f"Constraint {i + 1}: λ = {cons.dual_value}")