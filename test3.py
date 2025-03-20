import cvxpy as cp 
import numpy as np

np.random.seed(1)
x1 = cp.Variable()
x2 = cp.Variable()

#Hàm mục tiêu
cost = 4*x1 + 5*x2

#các ràng buộc
constraints = [
    3*x1 + x2 <= 10,
    2*x1 + 2*x2 <= 8,
    x1 + 4*x2 <= 15,
    x1 >=  0,
    x2 >= 0
]

#Định nghĩa bài toán tối ưu 
prob = cp.Problem(cp.Maximize(cost), constraints)

prob.solve()

print("Optimal profit:", prob.value)
print("Optimal production of product 1:", x1.value)
print("Optimal production of product 2:", x2.value)

