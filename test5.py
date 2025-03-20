import cvxpy as cp
import numpy as np

# Định nghĩa các biến
x = cp.Variable()
y = cp.Variable()

# Định nghĩa hàm mục tiêu riêng biệt
cost = cp.abs(x) - 2 * cp.sqrt(y)

# Định nghĩa các ràng buộc
constraints = [
    2 >= cp.exp(x),  # Ràng buộc 2 >= e^x
    x + y == 5,      # Ràng buộc x + y = 5
    y >= 0           # y phải không âm vì là đối số của sqrt
]

# Định nghĩa bài toán tối ưu và truyền cost vào
prob = cp.Problem(cp.Minimize(cost), constraints)

# Giải bài toán
prob.solve()

# In kết quả
print("Optimal value of x:", x.value)
print("Optimal value of y:", y.value)
print("Optimal objective value:", prob.value)
