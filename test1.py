# Import packages.
import cvxpy as cp
import numpy as np

# Generate data.
m = 20 #số lượng các điểm dữ liệu 
n = 15 #số lượng các đặc trưng (features)
np.random.seed(1) #thiết lập các hạt giống để tái tạo kết quả/ khi sử dụng hàm này thì mỗi khi chạy chương trình kết quả sẽ k đổi
A = np.random.randn(m, n)
b = np.random.randn(m)

# Define and solve the CVXPY problem.
x = cp.Variable(n) #biến quyết định x
cost = cp.sum_squares(A @ x - b)  #Hàm mục tiêu      
prob = cp.Problem(cp.Minimize(cost)) #tối thiểu hóa hàm mục tiêu 
prob.solve() #giải bài toán 

# Print result.
print("\nThe optimal value is", prob.value) #giá trị tối ưu của hàm mục tiêu
print("The optimal x is") #giá trị tối ưu của x
print(x.value)
print("The norm of the residual is ", cp.norm(A @ x - b, p=2).value)
