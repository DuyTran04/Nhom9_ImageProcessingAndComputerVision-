import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog, Frame, StringVar
from PIL import Image, ImageTk
from otsu import otsu_threshold, global_mean_threshold, multi_threshold  # Import các hàm thuật toán từ file algorithms


# Lớp ImageProcessingApp: Tạo giao diện xử lý ảnh
class ImageProcessingApp:
    def __init__(self, root):
        # Thiết lập các thuộc tính chính của cửa sổ
        self.root = root
        self.root.title("010100086901-XỬ LÝ ẢNH VÀ THỊ GIÁC MÁY TÍNH-NHÓM 9")
        self.root.configure(bg='#e6f7ff')  # Màu nền xanh nhạt
        self.root.resizable(True, True)  # Cho phép thay đổi kích thước
        self.root.geometry("1200x600")  # Kích thước mặc định

        # Khởi tạo các biến lưu đường dẫn ảnh và tiêu đề ảnh đã xử lý
        self.original_image = StringVar()  # Đường dẫn ảnh gốc
        self.processed_title = StringVar()  # Tiêu đề ảnh đã xử lý

        # Gọi hàm khởi tạo giao diện
        self.setup_gui()

    # Hàm tạo giao diện người dùng
    def setup_gui(self):
        # Tạo khung chứa chính và cấu hình giao diện
        main_container = Frame(self.root, bg='#e6f7ff')
        main_container.pack(expand=True, fill='both', padx=20, pady=20)
        self.setup_titles(main_container)  # Thêm phần tiêu đề
        self.create_button_panel(main_container)  # Thêm nút bấm điều khiển
        self.create_image_panel(main_container)  # Thêm khung chứa ảnh gốc và ảnh đã xử lý

    def setup_titles(self, parent):
        # Tạo tiêu đề và tiêu đề phụ trong giao diện
        title_frame = Frame(parent, bg='#e6f7ff')
        title_frame.pack(fill='x', pady=(0, 20))
        main_title = Label(title_frame, text="XỬ LÝ ẢNH VÀ THỊ GIÁC MÁY TÍNH", bg='#e6f7ff',
                           fg='#FF0000', font=("Time New Romans", 28, 'bold'))
        main_title.pack()
        sub_title = Label(title_frame, text="NHÓM 9", bg='#e6f7ff', fg='#FF0000', font=("Arial", 28, 'bold'))
        sub_title.pack(pady=(5, 0))

    def create_button_panel(self, parent):
        # Tạo khung chứa các nút chức năng
        button_frame = Frame(parent, bg='#e6f7ff')
        button_frame.pack(fill='x', pady=(0, 20))

        # Các nút chức năng để chọn và xử lý ảnh
        buttons = [
            ("Chọn Hình Ảnh", self.select_image, '#66b3ff'),  # Nút chọn ảnh
            ("Xử lý Otsu", self.process_images_otsu, '#ffb3b3'),  # Nút xử lý Otsu
            ("Xử lý Global Mean", self.process_images_global_mean, '#ffb3b3'),  # Xử lý Global Mean
            ("Xử lý Đa ngưỡng", self.process_images_multi_threshold, '#ffb3b3'),  # Xử lý Multi-threshold
            ("Xử lý Tất Cả", self.process_all_images, '#ffb3b3')  # Xử lý tất cả
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

        # Khung bên trái để hiển thị ảnh gốc
        original_frame = Frame(self.image_container, bg='#e6f7ff')
        original_frame.grid(row=0, column=0, padx=20, pady=20)
        self.original_title = Label(original_frame, text="", bg='#e6f7ff',
                                    fg='#FF0000', font=("Arial", 26, 'bold'))
        self.original_title.pack(pady=(0, 10))
        self.original_label = Label(original_frame, bg='#e6f7ff')
        self.original_label.pack()

        # Khung bên phải để hiển thị ảnh đã xử lý
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
        # Mở hộp thoại để người dùng chọn ảnh
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if file_path:
            # Lưu đường dẫn ảnh đã chọn và hiển thị ảnh
            self.original_image.set(file_path)
            self.load_and_display_original(file_path)
            self.original_title.config(text="Ảnh Gốc")
            self.processed_label.config(image='')
            self.processed_title.set('')

    def load_and_display_original(self, file_path):
        # Đọc ảnh xám từ đường dẫn và hiển thị
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            # Giữ nguyên tỷ lệ ảnh khi resize
            height, width = img.shape
            max_size = 600
            ratio = min(max_size / width, max_size / height)
            new_size = (int(width * ratio), int(height * ratio))
            resized_img = cv2.resize(img, new_size)
            photo = ImageTk.PhotoImage(image=Image.fromarray(resized_img))
            self.original_label.config(image=photo)
            self.original_label.image = photo

    def display_processed_image(self, processed_img, title, max_size=600):
        # Hiển thị ảnh đã xử lý và resize để giữ nguyên tỷ lệ
        height, width = processed_img.shape
        ratio = min(max_size / width, max_size / height)
        new_size = (int(width * ratio), int(height * ratio))
        resized = cv2.resize(processed_img, new_size)
        photo = ImageTk.PhotoImage(image=Image.fromarray(resized))
        self.processed_label.config(image=photo)
        self.processed_label.image = photo
        self.processed_title.set(title)

    def process_images_otsu(self):
        if not self.original_image.get():
            return
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            threshold_value = otsu_threshold(img_array)[0]
            processed = (img_array >= threshold_value).astype(np.uint8) * 255
            self.display_processed_image(processed, "Xử lý Otsu")

    def process_images_global_mean(self):
        if not self.original_image.get():
            return
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            threshold = global_mean_threshold(img_array)
            processed = (img_array >= threshold).astype(np.uint8) * 255
            self.display_processed_image(processed, "Xử lý Global Mean")

    def process_images_multi_threshold(self):
        if not self.original_image.get():
            return
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            t1, t2 = multi_threshold(img_array)
            processed = np.zeros(img_array.shape, dtype=np.uint8)
            processed[img_array < t1] = 85
            processed[(img_array >= t1) & (img_array < t2)] = 170
            processed[img_array >= t2] = 255
            self.display_processed_image(processed, "Xử lý Đa ngưỡng")

    def process_all_images(self):
        if not self.original_image.get():
            return
        img_array = cv2.imread(self.original_image.get(), cv2.IMREAD_GRAYSCALE)
        if img_array is not None:
            height, width = img_array.shape
            spacing = 20
            combined_result = np.zeros((height, width * 3 + spacing * 2), dtype=np.uint8)
            combined_result.fill(255)

            threshold_value = otsu_threshold(img_array)[0]
            otsu_result = (img_array >= threshold_value).astype(np.uint8) * 255
            combined_result[:, 0:width] = otsu_result

            threshold = global_mean_threshold(img_array)
            global_mean_result = (img_array >= threshold).astype(np.uint8) * 255
            combined_result[:, width + spacing:2 * width + spacing] = global_mean_result

            t1, t2 = multi_threshold(img_array)
            multi_result = np.zeros(img_array.shape, dtype=np.uint8)
            multi_result[img_array < t1] = 85
            multi_result[(img_array >= t1) & (img_array < t2)] = 170
            multi_result[img_array >= t2] = 255
            combined_result[:, 2 * width + 2 * spacing:] = multi_result

            self.display_processed_image(
                combined_result,
                "Kết quả: Otsu (trái) | Global Mean (giữa) | Multi-threshold (phải)",
                max_size=1200
            )


# Hàm main để khởi động ứng dụng
def main():
    root = Tk()
    app = ImageProcessingApp(root)
    root.mainloop()


# Kiểm tra nếu đây là file chính và chạy main
if __name__ == '__main__':
    main()
