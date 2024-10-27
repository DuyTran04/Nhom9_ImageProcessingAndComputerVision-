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
        self.root.configure(bg='#e6f7ff')      # Đặt màu nền xanh nhạt
        self.root.resizable(True, True)        # Cho phép thay đổi kích thước
        self.root.geometry("1200x600")         # Kích thước mặc định

        # Khởi tạo biến để lưu trữ
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
                          fg='#FF0000',
                          font=("Time New Romans", 28, 'bold'))
        main_title.pack()

        # Tiêu đề phụ - màu đỏ
        sub_title = Label(title_frame,
                         text="NHÓM 9",
                         bg='#e6f7ff',
                         fg='#FF0000',
                         font=("Arial", 28, 'bold'))
        sub_title.pack(pady=(5, 0))

    def create_button_panel(self, parent):
        # Tạo khung chứa các nút
        button_frame = Frame(parent, bg='#e6f7ff')
        button_frame.pack(fill='x', pady=(0, 20))

        # Định nghĩa các nút: (tên, lệnh, màu nền)
        buttons = [
            ("Chọn Hình Ảnh", self.select_image, '#66b3ff'),       # Nút chọn ảnh - màu xanh
            ("Xử lý Otsu", self.process_images_otsu, '#ffb3b3'),   # Nút xử lý Otsu - màu hồng
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

# Hàm main để khởi chạy ứng dụng
def main():
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

# Chạy chương trình khi file được thực thi trực tiếp
if __name__ == '__main__':
    main()
