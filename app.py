danh_sach_hang = [
    {
        'id': 'LH01',
        'ten_hang': 'Khoai mi',
        'khoi_luong': 369.0,
        'don_gia': 3470,
        'loai_don': 'nhap',
    },
    {
        'id': 'LH02',
        'ten_hang': 'Khoai mi',
        'khoi_luong': 50.0,
        'don_gia': 4200,
        'loai_don': 'xuat',
    }
]


def kiem_tra_ma(ma_moi, danh_sach):
    if len(ma_moi) != 4 or not ma_moi.startswith("LH") or not ma_moi[2:].isdigit():
        print("Lỗi: Mã giao dịch phải gồm 4 ký tự (ví dụ: LH01).")
        return False
    for item in danh_sach:
        if item['id'] == ma_moi:
            print("Lỗi: Mã giao dịch đã tồn tại.")
            return False
    return True


def hien_thi_danh_sach(danh_sach):
    print("\n=== DANH SÁCH HÀNG TỒN KHO ===")
    for item in danh_sach:
        thanh_tien = item['khoi_luong'] * item['don_gia']
        print(f"{item['id']} | {item['ten_hang']} | {item['khoi_luong']} kg | {item['don_gia']} VNĐ | {item['loai_don']} | Thành tiền: {thanh_tien}")


def them_lo_hang(danh_sach):
    ma_moi = input("Nhập mã giao dịch: ").strip().upper()
    if not kiem_tra_ma(ma_moi, danh_sach):
        return
    ten_hang = input("Nhập tên hàng: ")
    khoi_luong = float(input("Nhập khối lượng: "))
    don_gia = int(input("Nhập đơn giá: "))
    loai_don = input("Nhập loại đơn (nhap/xuat): ")
    danh_sach.append({
        'id': ma_moi,
        'ten_hang': ten_hang,
        'khoi_luong': khoi_luong,
        'don_gia': don_gia,
        'loai_don': loai_don,
    })
    print("Đã thêm giao dịch thành công!")


def xoa_lo_hang(danh_sach):
    ma_xoa = input("Nhập mã giao dịch cần xóa: ").strip().upper()
    for i, item in enumerate(danh_sach):
        if item['id'] == ma_xoa:
            del danh_sach[i]
            print("Xóa thành công giao dịch!")
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