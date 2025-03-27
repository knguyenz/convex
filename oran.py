import cvxpy as cp
import numpy as np

# Khởi tạo các tham số đầu vào
K = [0, 1, 2, 3, 4]  # 5 người dùng
I = [0, 1, 2]  # 3 RU
B = [[0, 1, 2], [0, 1], [0, 1, 2]]  # Danh sách các RB cho mỗi RU
Pmax = [10, 10, 10]  # Công suất tối đa của mỗi RU
RminK = {k: 1 for k in K}  # Tốc độ tối thiểu cho mỗi người dùng
Tmin = 10  # Throughput tối thiểu (Mbps)
BW = 18000  # Băng thông mỗi RB (Hz)
N0 = 1e-9  # Mật độ công suất tạp âm

# Giả sử kênh truyền (H) được nhập vào dưới dạng matrix
H = np.random.rand(len(K), len(I), len(B[0]))  # Sử dụng giá trị ngẫu nhiên để mô phỏng H

# Khởi tạo các biến quyết định
pi = { k : cp.Variable(name=f"pi_{k}", boolean=True) for k in K }
x = { (i, b, k): cp.Variable(name=f"x_{i}_{b}_{k}", boolean=True) for i in I for b in B[i] for k in K }
y = { (i, k): cp.Variable(name=f"y_{i}_{k}", boolean=True) for i in I for k in K }
p = { (i, b, k): cp.Variable(name=f"p_{i}_{b}_{k}", nonneg=True) for i in I for b in B[i] for k in K }
u = { (i, b, k): cp.Variable(name=f"u_{i}_{b}_{k}", nonneg=True) for i in I for b in B[i] for k in K }

# Biểu thức tính toán SINR và throughput
SINR = { (i, b, k): (u[(i, b, k)] * H[k][i][b]) / (BW * N0) 
         for i in I for b in B[i] for k in K }

dataRate = { 
    k: cp.sum([BW * cp.log1p(1 + SINR[(i, b, k)]) / np.log(2) 
               for i in I for b in B[i]]) 
    for k in K
}

# Danh sách ràng buộc
constraints = []

# Ràng buộc 1: Mỗi RB chỉ có thể gán cho một user
for i in I:
    for b in B[i]:
        constraints.append(cp.sum([x[(i, b, k)] for k in K]) <= 1)

# Ràng buộc 2: Đảm bảo tốc độ dữ liệu tối thiểu
for k in K:
    constraints.append(dataRate[k] >= RminK[k] * pi[k])

# Ràng buộc 3: Liên kết giữa x và y
for k in K:
    for i in I:
        constraints.append(cp.sum([x[(i, b, k)] for b in B[i]]) / len(B[i]) <= y[(i, k)])
        constraints.append(cp.sum([x[(i, b, k)] for b in B[i]]) / len(B[i]) + 1 - 1e-5 >= y[(i, k)])

# Ràng buộc 4: Liên kết giữa pi và y
for k in K:
    constraints.append(cp.sum([y[(i, k)] for i in I]) / len(I) <= pi[k])
    constraints.append(cp.sum([y[(i, k)] for i in I]) / len(I) + 1 - 1e-5 >= pi[k])

# Ràng buộc 5: Tổng công suất không vượt quá giới hạn của RU
for i in I:
    constraints.append(cp.sum([u[(i, b, k)] for b in B[i] for k in K]) <= Pmax[i])

# Ràng buộc 6: Liên kết giữa u, p, x
for k in K:
    for i in I:
        for b in B[i]:
            constraints.append(u[(i, b, k)] <= p[(i, b, k)])
            constraints.append(u[(i, b, k)] <= Pmax[i] * x[(i, b, k)])
            constraints.append(u[(i, b, k)] >= p[(i, b, k)] - Pmax[i] * x[(i, b, k)])
            constraints.append(p[(i, b, k)] <= Pmax[i] * x[(i, b, k)])

# Hàm mục tiêu: Tối đa throughput và số lát mạng được chấp nhận
objective = cp.Maximize(cp.sum([dataRate[k] + (1) * pi[k] for k in K]))

# Giải bài toán tối ưu
problem = cp.Problem(objective, constraints)

# Giải bài toán
problem.solve(solver=cp.MOSEK, verbose=True)

# In kết quả
print("Số người dùng được phục vụ:", sum(pi[k].value for k in K))
print("Giá trị mục tiêu:", problem.value)

# In kết quả phân bổ RB và các biến nhị phân
x_values = {(i, b, k): x[(i, b, k)].value for i in I for b in B[i] for k in K}
y_values = {(i, k): y[(i, k)].value for i in I for k in K}
print("Kết quả phân bổ RB (x):", x_values)
print("Kết quả phục vụ người dùng (y):", y_values)
