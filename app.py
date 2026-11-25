import unicodedata
import math
MAX_KHOI_LUONG = 1_000_000_000.0  # 1 tỷ kg
MAX_DON_GIA = 10_000_000_000       # 10 tỷ VNĐ

danh_sach_hang = [
    {
        'id': 'GD01',
        'ten_hang': 'Khoai mì',
        'khoi_luong': 369.0,
        'don_gia': 3470,
        'loai_don': 'nhap',
    },
    {
        'id': 'GD02',
        'ten_hang': 'Khoai mì',
        'khoi_luong': 50.0,
        'don_gia': 4200,
        'loai_don': 'xuat',
    }
]

def chuan_hoa_ten_hang(ten_nhap):
    ten_sach = " ".join(unicodedata.normalize("NFC", ten_nhap).split()).title()
    if not ten_sach:
        print("Lỗi: Tên hàng không được để trống.")
        return None
    return ten_sach

def ma_hop_le(ma):
    duoi = ma[2:]
    return (ma.startswith("GD") and duoi.isascii()
            and duoi.isdigit() and not duoi.startswith("0"))

def kiem_tra_ma(ma_moi, danh_sach):
    tap_hop_ma = {item['id'] for item in danh_sach}
    if ma_moi in tap_hop_ma:
        print("Lỗi: Mã giao dịch đã tồn tại.")
        return None
    if not ma_hop_le(ma_moi):
        print("Lỗi: Mã giao dịch phải bắt đầu bằng 'GD' và theo sau là 2 chữ số (ví dụ: GD01).")
        return None
    return ma_moi

def xuly_khoi_luong_nhap(chuoi_nhap):
    try:
        val = float(chuoi_nhap)
        if not math.isfinite(val) or val <= 0 or val > MAX_KHOI_LUONG:
            print(f"Lỗi: Khối lượng phải lớn hơn 0 và không vượt quá {MAX_KHOI_LUONG} kg.")
            return None
        val = round(val, 3)  # Làm tròn đến 3 chữ số thập phân
        if val <= 0:
            print("Lỗi: Khối lượng phải lớn hơn 0.")
            return None
        return val
    except ValueError:
        print("Lỗi: Khối phải là một con số thực hợp lệ.")
        return None
def nhap_khoi_luong(prompt = "Nhập khối lượng: "):
    return xuly_khoi_luong_nhap(input(prompt))

def xuly_don_gia_nhap(chuoi_nhap):
    try:
        val = int(chuoi_nhap)
        if val <= 0 or val > MAX_DON_GIA:
            print(f"Lỗi: Đơn giá phải là số nguyên dương và không vượt quá {MAX_DON_GIA:,.0f} VNĐ.")
            return None
        return val
    except ValueError:
        print("Lỗi: Đơn giá phải là một số nguyên hợp lệ.")
        return None
def nhap_don_gia(prompt = "Nhập đơn giá: "):
    return xuly_don_gia_nhap(input(prompt))

def kiem_tra_loai_don(loai_nhap):
    loai_sach = loai_nhap.strip().lower()
    if loai_sach not in ['nhap', 'xuat']:
        print("Lỗi: Loại đơn phải là 'nhap' hoặc 'xuat'.")
        return None
    return loai_sach

def hien_thi_danh_sach(danh_sach):
    print("\n=== DANH SÁCH HÀNG TỒN KHO ===")
    for item in danh_sach:
        thanh_tien = round(item['khoi_luong'] * item['don_gia'], 3)
        print(f"{item['id']} | {item['ten_hang']} | {item['khoi_luong']} kg | {item['don_gia']} VNĐ | {item['loai_don']} | Thành tiền: {thanh_tien}")


def them_lo_hang(danh_sach):
    ma_input = input("Nhập mã giao dịch: ")
    ma_moi = kiem_tra_ma(ma_input, danh_sach)
    if not ma_moi:
        return  # Nếu mã không hợp lệ, thoát khỏi hàm
    ten_hang = chuan_hoa_ten_hang(input("Nhập tên hàng: "))
    if not ten_hang:
        return  # Nếu tên hàng không hợp lệ, thoát khỏi hàm
    khoi_luong = nhap_khoi_luong()
    if khoi_luong is None:
        return  # Nếu khối lượng không hợp lệ, thoát khỏi hàm
    don_gia = nhap_don_gia()
    if don_gia is None:
        return  # Nếu đơn giá không hợp lệ, thoát khỏi hàm
    loai_don = kiem_tra_loai_don(input("Nhập loại đơn (nhap/xuat): "))
    if not loai_don:
        return  # Nếu loại đơn không hợp lệ, thoát khỏi hàm

    lo_hang_moi = {
        'id': ma_moi,
        'ten_hang': ten_hang,
        'khoi_luong': khoi_luong,
        'don_gia': don_gia,
        'loai_don': loai_don,
    }
    danh_sach_moi = danh_sach + [lo_hang_moi]
    if not kiem_tra_hang_ton_kho(danh_sach_moi):
        print("Lỗi: Giao dịch này sẽ dẫn đến tồn kho âm. Không thể thêm giao dịch.")
        return

    danh_sach.append(lo_hang_moi)
    print("Thêm giao dịch thành công!")
        if ton_kho[ten] < 0:
            print(f"Cảnh báo: Hàng '{ten}' có tồn kho âm ({ton_kho[ten]} kg) sau giao dịch {item['id']}.")
            return False
    return True

def xoa_lo_hang(danh_sach):
    ma_xoa = input("Nhập mã giao dịch cần xóa: ").strip().upper()
    for i, item in enumerate(danh_sach):
        if item['id'] == ma_xoa:
            return
    print("Không tìm thấy mã giao dịch.")


while True:
    print("\n--- MENU ---")
    print("1. Xem danh sách hàng tồn kho")
    print("2. Thêm giao dịch mới")
    print("3. Xóa giao dịch")
    print("0. Thoát chương trình")
    lua_chon = input("Nhập lựa chọn của bạn (0-3): ")
    if lua_chon == "1":
        hien_thi_danh_sach(danh_sach_hang)
    elif lua_chon == "2":
        them_lo_hang(danh_sach_hang)
    elif lua_chon == "3":
        xoa_lo_hang(danh_sach_hang)
    elif lua_chon == "0":
        break
    else:
        print("Lựa chọn không hợp lệ!")