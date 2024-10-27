# Import các thư viện cần thiết
import cv2              # Xử lý ảnh
import numpy as np      # Tính toán số học
from tkinter import Tk, Button, Label, filedialog, Frame, StringVar  # Tạo giao diện
from PIL import Image, ImageTk   # Xử lý và hiển thị ảnh trong Tkinter

# Lớp chính để xử lý ảnh và tạo giao diện
class ImageProcessingApp:
    def __init__(self, root):
        # Cấu hình cửa sổ chính
        self.root = root
        self.root.title("010100086901-XỬ LÝ ẢNH VÀ THỊ GIÁC MÁY TÍNH-NHÓM 9")
        self.root.configure(bg='#e6f7ff')      # Màu nền xanh nhạt
        self.root.resizable(True, True)        # Cho phép thay đổi kích thước
        self.root.geometry("1200x600")         # Kích thước mặc định

        # Khởi tạo biến
        self.original_image = StringVar()       # Lưu đường dẫn ảnh gốc
        self.processed_title = StringVar()      # Lưu tiêu đề ảnh đã xử lý

        # Thiết lập giao diện
        self.setup_gui()

    def setup_gui(self):
        # Tạo khung chứa chính
        main_container = Frame(self.root, bg='#e6f7ff')
        main_container.pack(expand=True, fill='both', padx=20, pady=20)

        # Thiết lập các thành phần giao diện
        self.setup_titles(main_container)        # Phần tiêu đề
        self.create_button_panel(main_container) # Phần nút bấm
        self.create_image_panel(main_container)  # Phần hiển thị ảnh

    def setup_titles(self, parent):
        # Tạo khung chứa tiêu đề
        title_frame = Frame(parent, bg='#e6f7ff')
        title_frame.pack(fill='x', pady=(0, 20))

        # Tiêu đề chính - màu đỏ
        main_title = Label(title_frame,
                          text="XỬ LÝ ẢNH VÀ THỊ GIÁC MÁY TÍNH",
                          bg='#e6f7ff',
                          fg='#FF0000',  # Màu chữ đỏ
                          font=("Time New Romans", 28, 'bold'))
        main_title.pack()

        # Tiêu đề phụ - màu đỏ
        sub_title = Label(title_frame,
                         text="NHÓM 9",
                         bg='#e6f7ff',
                         fg='#FF0000',  # Màu chữ đỏ
                         font=("Arial", 28, 'bold'))
        sub_title.pack(pady=(5, 0))

    def create_button_panel(self, parent):
        # Tạo khung chứa các nút
        button_frame = Frame(parent, bg='#e6f7ff')
        button_frame.pack(fill='x', pady=(0, 20))

        # Định nghĩa các nút: (tên, lệnh, màu nền)
        buttons = [
            ("Chọn Hình Ảnh", self.select_image, '#66b3ff'),         # Nút chọn ảnh - màu xanh
            ("Xử lý Otsu", self.process_images_otsu, '#ffb3b3'),     # Nút Otsu
            ("Xử lý Global Mean", self.process_images_global_mean, '#ffb3b3'),  # Nút Global Mean
            ("Xử lý Đa ngưỡng", self.process_images_multi_threshold, '#ffb3b3'),# Nút Multi-threshold
            ("Xử lý Tất Cả", self.process_all_images, '#ffb3b3')     # Nút xử lý tất cả
        ]

        # Tạo và thêm các nút vào giao diện
        for text, command, color in buttons:
            btn = Button(button_frame, text=text, command=command,
                         bg=color, fg='white', font=("Arial", 19, 'bold'),
                         width=15, height=2)
            btn.pack(side='left', padx=5)

    def create_image_panel(self, parent):
        # Tạo container chứa ảnh gốc và ảnh đã xử lý
        self.image_container = Frame(parent, bg='#e6f7ff')
        self.image_container.pack(expand=True, fill='both')

        # Panel ảnh gốc (bên trái)
        original_frame = Frame(self.image_container, bg='#e6f7ff')
        original_frame.grid(row=0, column=0, padx=20, pady=20)
        self.original_title = Label(original_frame, text="", bg='#e6f7ff',
                                  fg='#FF0000', font=("Arial", 26, 'bold'))
        self.original_title.pack(pady=(0, 10))
        self.original_label = Label(original_frame, bg='#e6f7ff')
        self.original_label.pack()

        # Panel ảnh đã xử lý (bên phải)
        processed_frame = Frame(self.image_container, bg='#e6f7ff')
        processed_frame.grid(row=0, column=1, padx=20, pady=20)
        self.processed_title_label = Label(processed_frame,
                                         textvariable=self.processed_title,
                                         bg='#e6f7ff', fg='#FF0000',
                                         font=("Arial", 26, 'bold'))
        self.processed_title_label.pack(pady=(0, 10))
        self.processed_label = Label(processed_frame, bg='#e6f7ff')
        self.processed_label.pack()

    def select_image(self):
        # Mở hộp thoại chọn file ảnh
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            # Cập nhật và hiển thị ảnh đã chọn
            self.original_image.set(file_path)
            self.load_and_display_original(file_path)
            self.original_title.config(text="Ảnh Gốc")
            # Xóa ảnh đã xử lý trước đó
            self.processed_label.config(image='')
            self.processed_title.set('')

    def load_and_display_original(self, file_path):
        # Đọc ảnh dưới dạng ảnh xám
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            # Tính toán kích thước mới giữ nguyên tỷ lệ
            height, width = img.shape
            max_size = 600  # Kích thước tối đa cho phép
            ratio = min(max_size / width, max_size / height)
            new_size = (int(width * ratio), int(height * ratio))

            # Resize và hiển thị ảnh
            resized_img = cv2.resize(img, new_size)
            photo = ImageTk.PhotoImage(image=Image.fromarray(resized_img))
            self.original_label.config(image=photo)
            self.original_label.image = photo

    def display_processed_image(self, processed_img, title, max_size=600):
        # Tính toán kích thước mới giữ nguyên tỷ lệ
        height, width = processed_img.shape
        ratio = min(max_size / width, max_size / height)
        new_size = (int(width * ratio), int(height * ratio))

        # Resize và hiển thị ảnh đã xử lý
        resized = cv2.resize(processed_img, new_size)
        photo = ImageTk.PhotoImage(image=Image.fromarray(resized))
        self.processed_label.config(image=photo)
        self.processed_label.image = photo
        self.processed_title.set(title)

    def process_images_otsu(self):
        # Kiểm tra xem đã có ảnh được chọn chưa
        if not self.original_image.get():
            return
        # Đọc ảnh xám và xử lý
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            # Tính ngưỡng Otsu và phân ngưỡng ảnh
            threshold_value = self.otsu_threshold(img_array)[0]
            processed = (img_array >= threshold_value).astype(np.uint8) * 255
            # Hiển thị kết quả
            self.display_processed_image(processed, "Xử lý Otsu")

    def process_images_global_mean(self):
        # Kiểm tra xem đã có ảnh được chọn chưa
        if not self.original_image.get():
            return
        # Đọc và xử lý ảnh bằng phương pháp Global Mean
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            # Tính ngưỡng là giá trị trung bình của ảnh
            threshold = np.mean(img_array)
            processed = (img_array >= threshold).astype(np.uint8) * 255
            # Hiển thị kết quả
            self.display_processed_image(processed, "Xử lý Global Mean")

    def process_images_multi_threshold(self):
        # Kiểm tra xem đã có ảnh được chọn chưa
        if not self.original_image.get():
            return
        # Đọc và xử lý ảnh bằng phương pháp đa ngưỡng
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            # Tính hai ngưỡng và phân ảnh thành 3 vùng
            t1, t2 = self.multi_threshold(img_array)
            processed = np.zeros(img_array.shape, dtype=np.uint8)
            processed[img_array < t1] = 85          # Vùng tối
            processed[(img_array >= t1) & (img_array < t2)] = 170  # Vùng trung bình
            processed[img_array >= t2] = 255        # Vùng sáng
            # Hiển thị kết quả
            self.display_processed_image(processed, "Xử lý Đa ngưỡng")

    def process_all_images(self):
        # Kiểm tra xem đã có ảnh được chọn chưa
        if not self.original_image.get():
            return
        # Đọc ảnh xám
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            # Tạo ảnh kết quả với khoảng trắng giữa các ảnh
            height, width = img_array.shape
            spacing = 20  # Khoảng cách giữa các ảnh
            combined_result = np.zeros((height, width * 3 + spacing * 2), dtype=np.uint8)
            combined_result.fill(255)  # Đặt nền trắng

            # Xử lý Otsu
            threshold_value = self.otsu_threshold(img_array)[0]
            otsu_result = (img_array >= threshold_value).astype(np.uint8) * 255
            combined_result[:, 0:width] = otsu_result

            # Xử lý Global Mean
            threshold = np.mean(img_array)
            global_mean_result = (img_array >= threshold).astype(np.uint8) * 255
            combined_result[:, width + spacing:2 * width + spacing] = global_mean_result

            # Xử lý Multi-threshold
            t1, t2 = self.multi_threshold(img_array)
            multi_result = np.zeros(img_array.shape, dtype=np.uint8)
            multi_result[img_array < t1] = 85
            multi_result[(img_array >= t1) & (img_array < t2)] = 170
            multi_result[img_array >= t2] = 255
            combined_result[:, 2 * width + 2 * spacing:] = multi_result

            # Hiển thị kết quả với kích thước lớn
            self.display_processed_image(
                combined_result,
                "Kết quả: Otsu (trái) | Global Mean (giữa) | Multi-threshold (phải)",
                max_size=1200  # Tăng kích thước hiển thị cho ảnh tổng hợp
            )

    def otsu_threshold(self, image):
        # Thuật toán Otsu để tìm ngưỡng tối ưu
        # Bước 1: Tính histogram
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        total_pixels = image.size
        p = hist / total_pixels

        # Bước 2: Tính moment tích lũy bậc 0 và 1
        mg = np.dot(np.arange(256), p)
        max_between_class_variance = 0
        threshold_value = 0
        m1 = m2 = 0
        weight_A = 0
        sum_A = 0

        # Bước 3: Tìm ngưỡng tối ưu
        for k in range(256):
            # Tính trọng số của 2 lớp
            weight_A += p[k]
            if weight_A == 0:
                continue
            weight_B = 1 - weight_A
            if weight_B == 0:
                break

            # Tính giá trị trung bình của 2 lớp
            sum_A += k * p[k]
            mean_A = sum_A / weight_A if weight_A != 0 else 0
            mean_B = (mg - sum_A) / weight_B if weight_B != 0 else 0

            # Tính phương sai giữa 2 lớp
            between_class_variance = weight_A * weight_B * (mean_A - mean_B) ** 2

            # Cập nhật ngưỡng nếu tìm được phương sai lớn hơn
            if between_class_variance > max_between_class_variance:
                max_between_class_variance = between_class_variance
                threshold_value = k
                m1 = mean_A
                m2 = mean_B
        return threshold_value, mg, m1, m2

    def multi_threshold(self, image):
        # Thuật toán tìm đa ngưỡng
        # Bước 1: Tính histogram
        histogram, _ = np.histogram(image, bins=256, range=(0, 256))
        total_pixels = image.size
        max_variance = 0
        best_thresholds = (0, 0)

        # Bước 2: Tìm 2 ngưỡng tối ưu
        for t1 in range(1, 255):
            for t2 in range(t1 + 40, 256): # t2 phải lớn hơn t1 ít nhất 40 đơn vị
                # Tính trọng số của 3 lớp
                w1 = np.sum(histogram[:t1])     # Lớp 1: 0 -> t1-1
                w2 = np.sum(histogram[t1:t2])   # Lớp 2: t1 -> t2-1
                w3 = total_pixels - w1 - w2     # Lớp 3: t2 -> 255

                # Kiểm tra điều kiện hợp lệ
                if w1 == 0 or w2 == 0 or w3 == 0:
                    continue
                # Tính giá trị trung bình của 3 lớp
                m1 = np.sum(np.arange(t1) * histogram[:t1]) / w1
                m2 = np.sum(np.arange(t1, t2) * histogram[t1:t2]) / w2
                m3 = np.sum(np.arange(t2, 256) * histogram[t2:]) / w3

                # Tính phương sai giữa các lớp
                variance_between = (w1 * (m1 - (w1 + w2 + w3) / total_pixels) ** 2 +
                                    w2 * (m2 - (w1 + w2 + w3) / total_pixels) ** 2 +
                                    w3 * (m3 - (w1 + w2 + w3) / total_pixels) ** 2)

                # Cập nhật ngưỡng nếu tìm được phương sai lớn hơn
                if variance_between > max_variance:
                    max_variance = variance_between
                    best_thresholds = (t1, t2)
        return best_thresholds

# Hàm main để khởi chạy ứng dụng
def main():
    # Khởi tạo cửa sổ chính và chạy ứng dụng
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
# Chạy chương trình khi file được thực thi trực tiếp
if __name__ == '__main__':
    main()
