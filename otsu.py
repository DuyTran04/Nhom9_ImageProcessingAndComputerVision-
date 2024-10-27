import cv2                # Thư viện xử lý ảnh OpenCV
import numpy as np        # Thư viện xử lý toán học, hỗ trợ mảng lớn

# Hàm otsu_threshold: Tìm ngưỡng tối ưu dựa trên phương pháp Otsu
def otsu_threshold(image):
    # Tính histogram và xác suất xuất hiện của mỗi mức xám
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])  # Đếm số pixel cho mỗi mức xám
    total_pixels = image.size                                   # Tổng số pixel trong ảnh
    p = hist / total_pixels                                     # Xác suất của mỗi mức xám

    # Tính moment tổng của ảnh và khởi tạo các biến hỗ trợ
    mg = np.dot(np.arange(256), p)      # Giá trị trung bình tổng của ảnh
    max_between_class_variance = 0      # Biến lưu phương sai lớn nhất giữa các lớp
    threshold_value = 0                 # Ngưỡng tối ưu
    m1 = m2 = 0                         # Trung bình của hai lớp (được cập nhật khi tìm ngưỡng tối ưu)
    weight_A = 0                        # Trọng số của lớp A (lớp tối)
    sum_A = 0                           # Tích lũy trung bình cho lớp A

    # Tìm ngưỡng tối ưu bằng cách thử từng mức xám từ 0 đến 255
    for k in range(256):
        weight_A += p[k]                # Cộng dồn xác suất để tính trọng số của lớp A
        if weight_A == 0:
            continue                    # Nếu lớp A chưa có pixel nào, bỏ qua
        weight_B = 1 - weight_A         # Trọng số của lớp B (lớp sáng)
        if weight_B == 0:
            break                       # Nếu không còn pixel nào cho lớp B, dừng lại

        # Cập nhật trung bình của lớp A và B
        sum_A += k * p[k]
        mean_A = sum_A / weight_A if weight_A != 0 else 0      # Trung bình của lớp A
        mean_B = (mg - sum_A) / weight_B if weight_B != 0 else 0  # Trung bình của lớp B

        # Tính phương sai giữa hai lớp tại ngưỡng k
        between_class_variance = weight_A * weight_B * (mean_A - mean_B) ** 2

        # Cập nhật ngưỡng tối ưu nếu phương sai giữa các lớp lớn hơn
        if between_class_variance > max_between_class_variance:
            max_between_class_variance = between_class_variance
            threshold_value = k         # Lưu lại ngưỡng k là ngưỡng tối ưu
            m1 = mean_A                 # Lưu trung bình của lớp A
            m2 = mean_B                 # Lưu trung bình của lớp B
    return threshold_value, mg, m1, m2  # Trả về ngưỡng tối ưu và các giá trị trung bình

# Hàm global_mean_threshold: Tính ngưỡng dựa trên trung bình toàn cục của ảnh
def global_mean_threshold(image):
    return np.mean(image)               # Trung bình tất cả các pixel trong ảnh

# Hàm multi_threshold: Tìm hai ngưỡng tối ưu để phân ảnh thành ba vùng
def multi_threshold(image):
    # Tính histogram của ảnh
    histogram, _ = np.histogram(image, bins=256, range=(0, 256))  # Đếm số pixel cho mỗi mức xám
    total_pixels = image.size
    max_variance = 0                       # Biến lưu phương sai lớn nhất giữa các lớp
    best_thresholds = (0, 0)               # Lưu hai ngưỡng tối ưu

    # Duyệt qua các giá trị ngưỡng t1 và t2 để tìm cặp ngưỡng tối ưu
    for t1 in range(1, 255):
        for t2 in range(t1 + 40, 256):     # t2 phải lớn hơn t1 ít nhất 40 để có khoảng cách
            # Tính trọng số của từng lớp
            w1 = np.sum(histogram[:t1])    # Trọng số lớp 1 (0 -> t1-1)
            w2 = np.sum(histogram[t1:t2])  # Trọng số lớp 2 (t1 -> t2-1)
            w3 = total_pixels - w1 - w2    # Trọng số lớp 3 (t2 -> 255)

            if w1 == 0 or w2 == 0 or w3 == 0:
                continue                    # Bỏ qua nếu lớp nào không có pixel

            # Tính trung bình của từng lớp
            m1 = np.sum(np.arange(t1) * histogram[:t1]) / w1  # Trung bình lớp 1
            m2 = np.sum(np.arange(t1, t2) * histogram[t1:t2]) / w2  # Trung bình lớp 2
            m3 = np.sum(np.arange(t2, 256) * histogram[t2:]) / w3  # Trung bình lớp 3

            # Tính phương sai giữa các lớp
            variance_between = (w1 * (m1 - (w1 + w2 + w3) / total_pixels) ** 2 +
                                w2 * (m2 - (w1 + w2 + w3) / total_pixels) ** 2 +
                                w3 * (m3 - (w1 + w2 + w3) / total_pixels) ** 2)

            # Cập nhật ngưỡng nếu tìm được phương sai lớn hơn
            if variance_between > max_variance:
                max_variance = variance_between
                best_thresholds = (t1, t2)  # Lưu cặp ngưỡng tối ưu
    return best_thresholds                 # Trả về hai ngưỡng tối ưu
