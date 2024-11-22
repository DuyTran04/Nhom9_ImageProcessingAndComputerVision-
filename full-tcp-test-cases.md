| Test Case ID | Tên Test Case | Mô tả | Điều kiện tiên quyết | Các bước thực hiện | Kết quả mong đợi |
|--------------|---------------|--------|----------------------|-------------------|------------------|
| **I. Kiểm tra khởi động và dừng Server** |
| TC-01 | Khởi động server | Kiểm tra server khởi động với IP và cổng hợp lệ | Máy chủ có kết nối mạng | 1. Mở giao diện TCP Server<br>2. Nhập số cổng<br>3. Nhấn "Start Server" | Server khởi động thành công, hiển thị IP và trạng thái "Server is running" |
| TC-02 | Dừng server | Kiểm tra server có thể dừng khi đang chạy | Server đang chạy | 1. Nhấn "Stop Server" | Server dừng hoạt động, trạng thái chuyển về "Server stopped" |
| TC-03 | Lưu tệp | Kiểm tra chức năng lưu tệp vào thư mục chỉ định | Server đã khởi động | 1. Nhấn "Browse"<br>2. Chọn thư mục lưu tệp<br>3. Cho client gửi tệp | Tệp được lưu trong thư mục đã chọn với trạng thái "Completed" |
| TC-04 | Mất kết nối mạng (Server) | Kiểm tra server xử lý khi mất kết nối mạng | Server đang chạy | 1. Ngắt kết nối mạng của máy chủ | Hiển thị thông báo "Network connection lost". Server tự động dừng | 
| TC-05 | Khởi động server khi không có mạng | Kiểm tra xử lý khi không có kết nối mạng | Máy chủ không có kết nối mạng | 1. Ngắt kết nối mạng<br>2. Khởi động server | Hiển thị thông báo lỗi, không cho phép khởi động |
| TC-06 | Khởi động server với port đã dùng | Kiểm tra xử lý port bị trùng | Port đang được sử dụng | 1. Khởi động server với port đang được dùng | Hiển thị thông báo lỗi, không cho phép khởi động |

| **II. Kiểm tra kết nối Client** |
| TC-07 | Kết nối client thành công | Kiểm tra client kết nối với server | Server đang chạy | 1. Nhập IP và port server<br>2. Click "Connect" | Hiển thị "Connected to server" |
| TC-08 | Kết nối với IP không hợp lệ | Kiểm tra validation IP | Server đang chạy | 1. Nhập IP không hợp lệ<br>2. Click "Connect" | Hiển thị thông báo lỗi IP không hợp lệ |
| TC-09 | Kết nối với port không hợp lệ | Kiểm tra validation port | Server đang chạy | 1. Nhập port không hợp lệ<br>2. Click "Connect" | Hiển thị thông báo lỗi port không hợp lệ |
| TC-10 | Ngắt kết nối client | Kiểm tra ngắt kết nối từ client | Client đang kết nối | 1. Click "Disconnect" | Client ngắt kết nối, UI reset về trạng thái ban đầu |
| TC-11 | Mất kết nối mạng (Client) | Kiểm tra xử lý khi client mất mạng | Client đang kết nối | 1. Ngắt kết nối mạng của client | Hiển thị thông báo lỗi, tự động ngắt kết nối |
| TC-12 | Kết nối khi server không hoạt động | Kiểm tra kết nối tới server offline | Server không hoạt động | 1. Thử kết nối tới server | Hiển thị thông báo lỗi sau timeout |

| **III. Kiểm tra truyền file đơn lẻ** |
| TC-13 | Gửi file nhỏ | Kiểm tra gửi file dung lượng nhỏ | Client đã kết nối | 1. Chọn file < 1MB<br>2. Click "Send" | File được gửi và nhận thành công, hiển thị "Completed" |
| TC-14 | Gửi file lớn | Kiểm tra gửi file dung lượng lớn | Client đã kết nối | 1. Chọn file > 100MB<br>2. Click "Send" | File được gửi và nhận thành công, progress bar chính xác |
| TC-15 | Gửi file có ký tự đặc biệt | Kiểm tra xử lý tên file đặc biệt | Client đã kết nối | 1. Gửi file tên có ký tự @#$% | File được lưu với tên chính xác |
| TC-16 | File trùng tên | Kiểm tra xử lý file trùng tên | Client đã kết nối, có file trùng tên | 1. Gửi file trùng tên | File được lưu với tên mới (1) |
| TC-17 | Cancel transfer | Kiểm tra hủy transfer | Client đang gửi file | 1. Click "Cancel" khi đang gửi | Transfer dừng lại, file tạm bị xóa |
| TC-18 | Resume transfer | Kiểm tra tiếp tục transfer | Có transfer bị hủy | 1. Thử gửi lại file bị hủy | File được gửi từ đầu thành công |

| **IV. Kiểm tra truyền nhiều file** |
| TC-19 | Giới hạn file | Kiểm tra chức năng giới hạn số lượng file | Client đã kết nối | 1. Bật tính năng giới hạn<br>2. Chọn quá số lượng cho phép | Hiện thông báo cảnh báo |
| TC-20 | Gửi nhiều file | Kiểm tra gửi nhiều file cùng lúc | Client đã kết nối | 1. Chọn nhiều file<br>2. Click "Send" | Tất cả file được gửi thành công |
| TC-21 | Gửi nhiều định dạng | Kiểm tra gửi nhiều loại file | Client đã kết nối | 1. Gửi file .txt, .pdf, .jpg, .zip | Tất cả file được gửi và mở được |
| TC-22 | Queue file | Kiểm tra xử lý hàng đợi | Client đang gửi file | 1. Gửi thêm file khi đang transfer | File được đưa vào queue |

| **V. Kiểm tra nhiều Client** |
| TC-23 | Nhiều client kết nối | Kiểm tra server xử lý nhiều client | Server đang chạy | 1. Kết nối nhiều client | Server hiển thị danh sách client |
| TC-24 | Giới hạn client | Kiểm tra giới hạn số lượng client | Đã có nhiều client kết nối | 1. Kết nối thêm client | Từ chối kết nối khi quá giới hạn |
| TC-25 | Client list update | Kiểm tra cập nhật danh sách | Có nhiều client | 1. Client connect/disconnect | Client list cập nhật real-time |
| TC-26 | Gửi file đồng thời | Kiểm tra nhận file từ nhiều client | Nhiều client kết nối | 1. Các client cùng gửi file | Server nhận tất cả file thành công |

| **VI. Kiểm tra giao diện** |
| TC-27 | UI Responsive | Kiểm tra độ mượt của UI | Server nhận nhiều file | 1. Thao tác với UI khi đang nhận file | UI phản hồi mượt mà |
| TC-28 | Progress display | Kiểm tra hiển thị tiến trình | Client đang gửi file | 1. Quan sát progress bar | Progress bar và % chính xác |
| TC-29 | Status update | Kiểm tra cập nhật trạng thái | Server/Client hoạt động | 1. Thực hiện các thao tác | Status bar cập nhật chính xác |
| TC-30 | Window resize | Kiểm tra resize cửa sổ | Server/Client đang chạy | 1. Thay đổi kích thước cửa sổ | UI tự động điều chỉnh |

| **VII. Kiểm tra hiệu năng** |
| TC-31 | Memory usage | Kiểm tra sử dụng RAM | Server chạy lâu | 1. Để server chạy 24h+ | RAM sử dụng ổn định |
| TC-32 | CPU usage | Kiểm tra sử dụng CPU | Server nhận nhiều file | 1. Monitor CPU khi nhận file | CPU không quá tải |
| TC-33 | Disk space | Kiểm tra xử lý hết ổ cứng | Ổ cứng gần đầy | 1. Gửi file khi hết dung lượng | Thông báo lỗi phù hợp |
| TC-34 | Network bandwidth | Kiểm tra sử dụng băng thông | Client gửi file lớn | 1. Monitor network usage | Băng thông sử dụng hợp lý |

| **VIII. Kiểm tra Log và History** |
| TC-35 | Connection history | Kiểm tra lịch sử kết nối | Server có nhiều client | 1. Client connect/disconnect | History list cập nhật đầy đủ |
| TC-36 | Transfer history | Kiểm tra lịch sử truyền file | Có nhiều file được truyền | 1. Xem transfer history | Hiển thị đầy đủ thông tin |
| TC-37 | Clear history | Kiểm tra xóa lịch sử | Có dữ liệu history | 1. Xóa history | History được xóa sạch |
| TC-38 | Export history | Kiểm tra xuất history | Có dữ liệu history | 1. Export history | File xuất chứa đủ thông tin |

| **IX. Kiểm tra xử lý lỗi** |
| TC-39 | Network error | Kiểm tra xử lý lỗi mạng | Đang truyền file | 1. Ngắt mạng đột ngột | Hiển thị lỗi, cleanup đúng |
| TC-40 | Invalid file | Kiểm tra file không hợp lệ | Client đã kết nối | 1. Gửi file corrupted | Thông báo lỗi phù hợp |
| TC-41 | Permission error | Kiểm tra lỗi quyền truy cập | Server đang chạy | 1. Lưu file vào thư mục không có quyền | Thông báo lỗi permission |
| TC-42 | Recovery | Kiểm tra khôi phục sau lỗi | Xảy ra lỗi | 1. Thử lại operation | Hệ thống hoạt động lại bình thường |

| **X. Kiểm tra bảo mật** |
| TC-43 | File validation | Kiểm tra validate file | Client đã kết nối | 1. Gửi file độc hại | File bị từ chối |
| TC-44 | Connection security | Kiểm tra bảo mật kết nối | Server đang chạy | 1. Scan các port | Chỉ port được chỉ định mở |
| TC-45 | Access control | Kiểm tra phân quyền | Nhiều client kết nối | 1. Client thử truy cập file khác | Từ chối truy cập trái phép |
| TC-46 | DOS protection | Kiểm tra chống DOS | Server đang chạy | 1. Tạo nhiều kết nối/request | Server không bị quá tải |

