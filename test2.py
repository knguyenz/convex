import cvxpy as cp
import numpy as np

# Tạo dữ liệu ngẫu nhiên cho A, b, và c (giả sử đã có các giá trị này từ bài toán thực tế)
n = 10  # số lượng sản phẩm
m = 15  # số thành phần (tài nguyên)

# Giả sử A, b và c được tạo ngẫu nhiên (hoặc được cung cấp từ bài toán thực tế)
A = np.random.randn(m, n)  # Ma trận A có kích thước (m x n)
b = np.random.randn(m)  # Vector b có kích thước m
c = np.random.randn(n)  # Vector c có kích thước n

# Định nghĩa biến quyết định
x = cp.Variable(n)  # Vector các biến quyết định (số lượng sản phẩm cần sản xuất)

# Định nghĩa hàm mục tiêu: tối thiểu hóa c^T * x
cost = c.T @ x

# Định nghĩa ràng buộc: A * x <= b
constraints = [A @ x <= b]

# Định nghĩa bài toán tối ưu
prob = cp.Problem(cp.Minimize(cost), constraints)

# Giải bài toán
prob.solve()

# In kết quả
print("The optimal value is", prob.value)  # In giá trị tối ưu của hàm mục tiêu
print("The optimal x is", x.value)  # In các giá trị tối ưu của biến quyết định
