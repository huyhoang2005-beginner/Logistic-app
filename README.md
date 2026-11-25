# Hệ thống quản lý kho vận & giao dịch

Dự án cá nhân thực hành lập trình Python theo phương pháp **Learning-by-Doing**. Ứng dụng sử dụng bài toán quản lý kho (nhập – xuất – tồn) làm bối cảnh để người học rèn luyện tư duy lập trình, xử lý dữ liệu, kiểm tra nghiệp vụ và phát triển phần mềm theo từng phiên bản.

> **Mục tiêu chính:** nâng cao năng lực lập trình thực tế thông qua việc xây dựng một sản phẩm xuyên suốt, không đặt mục tiêu trở thành phần mềm thương mại hoàn chỉnh.

## 1. Mục tiêu và định hướng

Dự án được phát triển từ ứng dụng dòng lệnh (CLI) đến ứng dụng web có dashboard. Qua từng phiên bản, người học từng bước thực hành:

- Cấu trúc dữ liệu Python: `list`, `dict`, `set`; xử lý chuỗi và chuẩn hóa tiếng Việt.
- Kiểm tra dữ liệu đầu vào, xử lý ngoại lệ và các ràng buộc nghiệp vụ.
- Đọc/ghi tệp JSON, CSV và xử lý thời gian.
- Lập trình hướng đối tượng, tổ chức mã nguồn thành các mô-đun và kiểm thử tự động.
- Phân tích dữ liệu, trực quan hóa và xuất báo cáo Excel.
- Xây dựng giao diện web bằng Streamlit.

### Nguyên tắc phát triển

1. **Phát triển tăng dần (Incremental):** hoàn thiện và kiểm tra từng phiên bản trước khi chuyển sang phiên bản tiếp theo.
2. **Vừa sức và có thể tự kiểm chứng:** sử dụng danh sách kiểm tra gồm 28 tình huống để đánh giá hành vi chương trình.
3. **Tự viết và hiểu mã nguồn:** ưu tiên hiểu rõ từng phần thay vì chỉ ghép các đoạn mã có sẵn.
4. **Đơn giản hóa có chủ đích:** dùng JSON/CSV phẳng thay vì cơ sở dữ liệu SQL; giữ chức năng sửa/xóa giao dịch để thực hành CRUD.
5. **Quản lý phiên bản:** sử dụng Git với commit có thông điệp rõ ràng và gắn tag khi phiên bản đạt yêu cầu kiểm thử.

## 2. Môi trường phát triển

| Thành phần | Công nghệ / phiên bản |
|---|---|
| Hệ điều hành | Windows 10 / Windows 11 |
| Ngôn ngữ | Python 3.12 |
| Môi trường ảo | `.venv` |
| Trình soạn thảo | Visual Studio Code |
| Quản lý mã nguồn | Git và GitHub |
| Giao diện ban đầu | CLI |
| Giao diện dự kiến | Streamlit |

## 3. Thiết kế dữ liệu và quy tắc nghiệp vụ

### 3.1. Lược đồ giao dịch

Hệ thống sử dụng thuật ngữ **Giao dịch (`GiaoDich`)** cho mọi bản ghi nhập và xuất kho. Mã định danh sử dụng tiền tố `GD`.

| Trường | Kiểu dữ liệu | Quy tắc |
|---|---|---|
| `id` | `str` | Chuẩn hóa bằng `strip().upper()`; bắt đầu bằng `GD`, phần sau chỉ gồm chữ số ASCII và không bắt đầu bằng 0. Ví dụ hợp lệ: `GD1`, `GD25`, `GD1000`. Mã phải duy nhất và không thay đổi sau khi tạo. |
| `ten_hang` | `str` | Chuẩn hóa Unicode NFC, loại bỏ khoảng trắng thừa và viết hoa chữ cái đầu theo `.title()`. Không chấp nhận tên rỗng. |
| `khoi_luong` | `float` | Đơn vị kg; phải là số hữu hạn, lớn hơn 0 và không vượt quá 1.000.000.000 kg. Làm tròn đến 3 chữ số thập phân và kiểm tra lại sau khi làm tròn. |
| `don_gia` | `int` | Đơn giá VND/kg; là số nguyên lớn hơn 0 và không vượt quá 10.000.000.000 VND/kg. |
| `loai_don` | `str` | Sau khi chuẩn hóa bằng `strip().lower()`, chỉ nhận `nhap` hoặc `xuat`. |
| `thoi_gian` | `str` | Định dạng `YYYY-MM-DD HH:MM:SS`; được bổ sung từ V2.0. |

`thanh_tien` được tính bằng `round(khoi_luong * don_gia)`, không lưu như dữ liệu gốc trong JSON để tránh sai lệch giữa các trường.

### 3.2. Quy tắc tồn kho

Tồn kho của một mặt hàng được tính bằng tổng khối lượng nhập trừ tổng khối lượng xuất:

`Tồn kho = Tổng nhập - Tổng xuất`

- Không cho phép giao dịch làm tồn kho của mặt hàng âm.
- Khi thêm đơn xuất, nếu khối lượng xuất vượt tồn khả dụng thì từ chối giao dịch và thông báo lượng tồn hiện tại.
- Khi sửa giao dịch, chỉ cho phép sửa `khoi_luong` và `don_gia`; không sửa mã, tên hàng, loại đơn hoặc thời gian.
- Khi xóa giao dịch, phải kiểm tra lại tính hợp lệ của toàn bộ lịch sử giao dịch.
- Việc kiểm tra phải duyệt giao dịch theo thứ tự phát sinh, không chỉ kiểm tra số tồn cuối cùng.
- Thao tác thêm, sửa và xóa chỉ được cập nhật dữ liệu thật sau khi dữ liệu mới vượt qua kiểm tra. Nếu không hợp lệ, dữ liệu ban đầu phải được giữ nguyên.
- Các phép so sánh tồn kho sử dụng `round(ton_kho, 3)` để hạn chế sai số số thực.

### 3.3. Quy tắc định giá và chỉ số tài chính

Dự án sử dụng phương pháp **đơn giá nhập bình quân gia quyền**, tính trên toàn bộ lịch sử giao dịch:

- Giá nhập bình quân = Tổng (khối lượng nhập × đơn giá nhập) / Tổng khối lượng nhập.
- Doanh thu = Tổng (khối lượng xuất × đơn giá bán).
- Giá vốn hàng xuất = Tổng khối lượng xuất × Giá nhập bình quân.
- Lợi nhuận gộp = Doanh thu − Giá vốn hàng xuất.
- Giá trị tồn kho = Tồn kho × Giá nhập bình quân.

Đơn giá của giao dịch xuất là giá bán. Các phép tính được thực hiện bằng số thực và chỉ làm tròn về số nguyên VND ở kết quả cuối. Do đây là bình quân gia quyền trên toàn bộ dữ liệu, giá vốn của các giao dịch xuất cũ có thể được tính lại khi phát sinh giao dịch nhập mới; đây là đơn giản hóa có chủ đích của dự án.

### 3.4. Các giới hạn có chủ đích

- Không sử dụng cơ sở dữ liệu SQL; tập trung thực hành File I/O với JSON và CSV.
- Tên hàng có dấu và không dấu, ví dụ `Khoai Mì` và `Khoai Mi`, được xem là hai tên khác nhau.
- Giữ chức năng sửa và xóa giao dịch để thực hành CRUD, không áp dụng mô hình sổ kế toán bất biến.

## 4. Kiến trúc dự kiến

Ứng dụng được chia thành các tầng trách nhiệm để có thể chuyển từ CLI sang web mà không phải viết lại phần xử lý nghiệp vụ.

| Tầng | Thành phần | Trách nhiệm |
|---|---|---|
| Giao diện | `main.py` (CLI) / `app_web.py` (Web) | Nhận dữ liệu đầu vào, gọi nghiệp vụ, hiển thị kết quả và thông báo lỗi; gọi lưu trữ sau mỗi thao tác thành công. |
| Nghiệp vụ | `KhoHang` | Quản lý giao dịch, kiểm tra mã trùng, kiểm soát tồn kho và tính các chỉ số tồn kho/tài chính. Không trực tiếp đọc hoặc ghi tệp. |
| Thực thể | `GiaoDich` | Kiểm tra và chuẩn hóa dữ liệu giao dịch; cung cấp thuộc tính tính toán `thanh_tien`. |
| Lưu trữ | `storage.py` | Đọc/ghi JSON an toàn và xuất dữ liệu CSV tương thích Excel tiếng Việt. |

Cấu trúc thư mục mục tiêu sau giai đoạn tái cấu trúc:

```text
Logistic-app/
├── main.py
├── models.py
├── storage.py
├── app_web.py
├── tests/
│   └── test_kho.py
├── data/
│   └── sample_inventory.json
├── reports/
├── requirements.txt
└── .gitignore
```

Các thư mục và tệp được bổ sung theo từng giai đoạn; đây là cấu trúc mục tiêu, không phải cam kết rằng toàn bộ đã có trong mã nguồn hiện tại.

## 5. Lộ trình phát triển

Lộ trình tổng thể:

`V1.0 → V1.1 → V2.0 → V3a → V3b → V3c → V4a → V4b → V4c → V5.0`

| Phiên bản | Trọng tâm | Nội dung chính |
|---|---|---|
| **V1.0** | Nền tảng CLI | Danh sách các dictionary trên RAM; hiển thị, kiểm tra mã, thêm và xóa giao dịch; vòng lặp menu. |
| **V1.1** | Hoàn thiện logic và Git | Chuẩn hóa mã/tên hàng, kiểm tra dữ liệu, kiểm soát tồn kho, sửa giao dịch, xử lý lỗi và thiết lập quy trình Git. |
| **V2.0** | Lưu trữ dữ liệu | Bổ sung thời gian giao dịch; đọc/ghi JSON; lưu an toàn bằng tệp tạm và `os.replace`; xử lý tệp thiếu, rỗng hoặc hỏng; xuất CSV. |
| **V3a** | Lớp `GiaoDich` | Đóng gói dữ liệu, setter kiểm tra hợp lệ, thuộc tính `thanh_tien`, `to_dict()` và `from_dict()`. |
| **V3b** | Lớp `KhoHang` | Quản lý giao dịch bằng dictionary; thực hiện CRUD, kiểm tra tồn kho và cung cấp các phương thức tính toán tài chính. |
| **V3c** | Tách mô-đun và kiểm thử | Tách giao diện, nghiệp vụ, thực thể và lưu trữ; chuyển các ca kiểm thử phù hợp sang `unittest`; kiểm tra hồi quy. |
| **V4a** | Phân tích dữ liệu | Dùng pandas tạo bảng tổng hợp nhập – xuất – tồn và các chỉ số tài chính; hiển thị trên Terminal. |
| **V4b** | Trực quan hóa | Dùng matplotlib tạo biểu đồ tồn kho theo mặt hàng và cơ cấu giá trị tồn kho. |
| **V4c** | Báo cáo Excel | Dùng openpyxl xuất nhật ký giao dịch và bảng tổng hợp nhập – xuất – tồn. |
| **V5.0** | Ứng dụng web | Dùng Streamlit xây dựng dashboard, biểu mẫu giao dịch, bảng dữ liệu, đồ thị và chức năng tải báo cáo. |

### Chi tiết định hướng theo giai đoạn

**V2.0 – Lưu trữ và CSV**
- Khi khởi động, xử lý tệp `inventory.tmp` còn sót từ lần ghi trước.
- Nếu chưa có `inventory.json`, tạo tệp chứa danh sách rỗng.
- Nếu JSON rỗng hoặc sai cú pháp, đổi tên tệp lỗi theo thời gian, cảnh báo người dùng và tạo tệp mới; không ghi đè dữ liệu lỗi.
- Giao dịch mới được gán thời gian bằng `datetime.now()`; dữ liệu đã lưu phải giữ nguyên thời gian khi nạp lại.
- Ghi JSON an toàn thông qua tệp tạm và `os.replace`; lưu ngay sau mỗi thao tác thành công.
- Xuất CSV có thể mở bằng Excel, giữ đúng tiếng Việt và định dạng số.

**V3.0 – OOP và kiểm thử**
- `GiaoDich`: quản lý dữ liệu và quy tắc xác thực của từng giao dịch.
- `KhoHang`: lưu giao dịch theo mã, kiểm tra tồn kho khi thêm/sửa/xóa và tính các chỉ số tài chính.
- Các phương thức nghiệp vụ ném `ValueError` khi dữ liệu hoặc thao tác không hợp lệ.
- Dùng `unittest` cho các ca kiểm thử không cần tương tác bàn phím; chạy lại checklist để bảo đảm hành vi không đổi sau tái cấu trúc.

**V4.0 – Phân tích và báo cáo**
- pandas tổng hợp dữ liệu theo mặt hàng và loại giao dịch.
- matplotlib tạo biểu đồ cột tồn kho và biểu đồ tròn cơ cấu giá trị tồn kho.
- openpyxl xuất tệp `reports/bao_cao_kho_chi_tiet.xlsx` gồm nhật ký giao dịch và bảng tổng hợp.

**V5.0 – Streamlit**
- Tái sử dụng `KhoHang` và `storage.py`; thay giao diện CLI bằng `app_web.py`.
- Hiển thị KPI: giá trị hàng tồn kho, doanh thu xuất bán, lợi nhuận gộp ước tính và tổng số giao dịch.
- Cung cấp bảng giao dịch, tìm kiếm/lọc, biểu mẫu nhập – xuất, cảnh báo xuất vượt tồn, đồ thị và tải CSV/Excel.

## 6. Kiểm thử chất lượng

Một phiên bản chỉ được xem là hoàn thành khi vượt qua toàn bộ ca kiểm thử áp dụng. Bản đặc tả xác định **28 ca kiểm thử**, chia thành các nhóm:

| Nhóm | Mã ca | Nội dung kiểm tra |
|---|---|---|
| Xác thực dữ liệu | T01–T10, T27 | Mã giao dịch, mã trùng, chuẩn hóa tên, tên rỗng, dữ liệu số, giá trị biên, làm tròn và giới hạn trên. |
| Logic kho | T11–T15, T28 | Xuất vượt tồn, sai số số thực, xóa/sửa làm tồn âm, kiểm tra theo thứ tự giao dịch và xử lý sửa dữ liệu giữa chừng. |
| Tài chính | T16–T18 | Giá nhập bình quân, doanh thu, giá vốn, lợi nhuận gộp và tính lại giá vốn khi có giao dịch nhập mới. |
| Lưu trữ | T19–T23 | JSON hỏng/rỗng, JSON sai nội dung, ghi tệp an toàn, đồng bộ sau khởi động lại và CSV tiếng Việt trên Excel. |
| Tái cấu trúc và báo cáo | T24–T26 | Kiểm thử hồi quy sau OOP, đối chiếu số liệu báo cáo và trường hợp chưa có giao dịch xuất. |

### Các ca kiểm thử áp dụng theo phiên bản

| Phiên bản | Yêu cầu |
|---|---|
| V1.1 | T01–T15, T27, T28 |
| V2.0 | Toàn bộ ca V1.1 và T19–T23 |
| V3.0 | Bổ sung T16–T18 và T24 |
| V4.0 | Bổ sung T25 và T26 |
| V5.0 | Toàn bộ checklist, trừ T07, T10 và T28 (các ca riêng cho CLI) |

## 7. Quy ước Git và quản lý tệp

### 7.1. Commit

Mỗi nhiệm vụ nhỏ nên được ghi nhận bằng một commit riêng, với thông điệp ngắn gọn theo dạng `<loại>: <nội dung>`.

| Tiền tố | Mục đích |
|---|---|
| `feat:` | Thêm tính năng |
| `fix:` | Sửa lỗi |
| `refactor:` | Tái cấu trúc mã nguồn, không chủ đích thay đổi hành vi |
| `test:` | Thêm hoặc sửa kiểm thử |
| `docs:` | Cập nhật tài liệu |
| `chore:` | Công việc cấu hình, không thay đổi hành vi chương trình |

### 7.2. Tag phiên bản

Gắn tag sau khi phiên bản vượt qua toàn bộ ca kiểm thử tương ứng: `v1.1`, `v2.0`, `v3.0`, `v4.0`, `v5.0`. Riêng `v1.0` là mốc lưu mã nguồn ban đầu, không đồng nghĩa với việc đã vượt qua checklist.

### 7.3. Các tệp không đưa lên Git

Tệp `.gitignore` cần loại trừ môi trường ảo, bộ nhớ đệm Python, dữ liệu thực, tệp tạm, báo cáo được sinh ra và cấu hình IDE cá nhân. Dữ liệu mẫu `data/sample_inventory.json` được quản lý trong Git để phục vụ kiểm thử; dữ liệu thực `data/inventory.json` không được commit.

## 8. Trạng thái và phạm vi tài liệu

Bản đặc tả gốc lần 4 được cập nhật ngày **17/10/2026** và ghi nhận V1.0, V1.1 đã hoàn thành, V2.0 đang triển khai tại thời điểm lập tài liệu.

README này hệ thống hóa mục tiêu, quy tắc nghiệp vụ, kiến trúc và lộ trình của dự án. Nội dung lộ trình là **định hướng phát triển**, không có nghĩa mọi tính năng đã được triển khai trong mã nguồn hiện tại. Trạng thái thực tế cần được đối chiếu với mã nguồn và các commit mới nhất trên nhánh chính.

---

*Dự án học tập cá nhân – Python 3.12.*
