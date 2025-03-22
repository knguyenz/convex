import cvxpy as cp
import numpy as np

# Dữ liệu đầu vào
order_widths = [14, 31, 36, 45]  # Các độ rộng đơn hàng
quantities = [211, 395, 610, 97]  # Số lượng yêu cầu cho từng độ rộng

# Định nghĩa các độ rộng cuộn có sẵn
roll_sizes = [14, 31, 36, 45]  # Các độ rộng cuộn có sẵn (inches)

# Tạo tất cả các kết hợp có thể của các cuộn sao cho tổng chiều dài không vượt quá 100 inch
patterns = []

# Tạo các mẫu cắt hợp lệ
for i in range(8):  # Số cuộn 14-inch có thể cắt
    for j in range(4):  # Số cuộn 31-inch có thể cắt
        for k in range(3):  # Số cuộn 36-inch có thể cắt
            for l in range(3):  # Số cuộn 45-inch có thể cắt
                total_length = i * 14 + j * 31 + k * 36 + l * 45
                if total_length <= 100:  # Nếu tổng chiều dài không vượt quá 100 inch
                    patterns.append([i, j, k, l])

# Chuyển mảng patterns thành một mảng NumPy
patterns = np.array(patterns)

# Tạo biến quyết định: số cuộn cắt theo mỗi mẫu
x = cp.Variable(len(patterns), integer=True)

# Mục tiêu: tối thiểu hóa tổng số cuộn cắt
objective = cp.Minimize(cp.sum(x))

# Ràng buộc: Đảm bảo đủ số lượng cuộn cho mỗi độ rộng
constraints = []  # Danh sách chứa các ràng buộc

# Lặp qua từng độ rộng đơn hàng
for i in range(len(order_widths)):
    total = 0  # Biến lưu tổng số cuộn cho độ rộng order_widths[i]
    
    # Lặp qua từng mẫu và tính tổng số cuộn cho độ rộng này
    for j in range(len(patterns)):
        total += patterns[j, i] * x[j]  # Tính số cuộn cho độ rộng i từ mẫu j
        
    # Thêm ràng buộc: Tổng số cuộn cho độ rộng này phải lớn hơn hoặc bằng yêu cầu
    constraints.append(total >= quantities[i])


# Mô hình tối ưu
problem = cp.Problem(objective, constraints)

# Giải quyết bài toán
problem.solve()

# In kết quả
print(f"Total rolls used: {np.sum(x.value):.0f}")

# In chi tiết các mẫu cắt được sử dụng
for j in range(len(patterns)):
    if x[j].value > 0:  # Chỉ in các mẫu cắt được sử dụng
        print(f"Pattern {j + 1}: {x[j].value:.0f} rolls")