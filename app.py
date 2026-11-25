import unicodedata
import math

MAX_KHOI_LUONG = 1_000_000_000.0  # 1 tỷ kg
MAX_DON_GIA = 10_000_000_000       # 10 tỷ VNĐ

danh_sach_hang = [
    {
        'id': 'GD1',
        'ten_hang': 'Khoai Mì',
        'khoi_luong': 369.0,
        'don_gia': 3470,
        'loai_don': 'nhap',
    },
    {
        'id': 'GD2',
        'ten_hang': 'Khoai Mì',
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


def kiem_tra_ma(ma_nhap, danh_sach):
    ma_chuan_hoa = ma_nhap.strip().upper()
    if not ma_hop_le(ma_chuan_hoa):
        print("Lỗi: Mã giao dịch phải bắt đầu bằng 'GD' và theo sau là số nguyên > 0 (ví dụ: GD1, GD25).")
        return None

    tap_hop_ma = {item['id'] for item in danh_sach}
    if ma_chuan_hoa in tap_hop_ma:
        print(f"Lỗi: Mã '{ma_chuan_hoa}' đã tồn tại trong hệ thống.")
        return None

    return ma_chuan_hoa


def xuly_khoi_luong_nhap(chuoi_nhap):
    try:
        val = float(chuoi_nhap)
        if not math.isfinite(val) or val <= 0 or val > MAX_KHOI_LUONG:
            print(f"Lỗi: Khối lượng phải là số hữu hạn lớn hơn 0 và không vượt quá {MAX_KHOI_LUONG:,.0f} kg.")
            return None
        val = round(val, 3)
        if val <= 0:
            print("Lỗi: Khối lượng sau làm tròn phải lớn hơn 0.")
            return None
        return val
    except ValueError:
        print("Lỗi: Khối lượng phải là số thực hợp lệ.")
        return None


def nhap_khoi_luong(prompt="Nhập khối lượng: "):
    return xuly_khoi_luong_nhap(input(prompt))


def xuly_don_gia_nhap(chuoi_nhap):
    try:
        val = int(chuoi_nhap)
        if val <= 0 or val > MAX_DON_GIA:
            print(f"Lỗi: Đơn giá phải là số nguyên dương và không vượt quá {MAX_DON_GIA:,.0f} VNĐ.")
            return None
        return val
    except ValueError:
        print("Lỗi: Đơn giá phải là số nguyên hợp lệ.")
        return None


def nhap_don_gia(prompt="Nhập đơn giá: "):
    return xuly_don_gia_nhap(input(prompt))


def kiem_tra_loai_don(loai_nhap):
    loai_sach = loai_nhap.strip().lower()
    if loai_sach not in ('nhap', 'xuat'):
        print("Lỗi: Loại đơn phải là 'nhap' hoặc 'xuat'.")
        return None
    return loai_sach


def kiem_tra_hang_ton_kho(danh_sach_gia_dinh):
    ton_kho = {}
    for item in danh_sach_gia_dinh:
        ten = item['ten_hang']
        luong = item['khoi_luong']

        if ten not in ton_kho:
            ton_kho[ten] = 0.0

        ton_kho_truoc = ton_kho[ten]

        if item['loai_don'] == 'nhap':
            ton_kho[ten] += luong
        elif item['loai_don'] == 'xuat':
            ton_kho[ten] -= luong

        ton_kho[ten] = round(ton_kho[ten], 3)

        if ton_kho[ten] < 0:
            print(
                f"Lỗi: Giao dịch '{item['id']}' làm tồn kho mặt hàng '{ten}' bị âm "
                f"(tồn kho khả dụng: {ton_kho_truoc} kg)."
            )
            return False

    return True


def hien_thi_danh_sach(danh_sach):
    print("\n=== DANH SÁCH HÀNG TỒN KHO ===")
    if not danh_sach:
        print("Danh sách hiện đang trống.")
        return

    for item in danh_sach:
        thanh_tien = round(item['khoi_luong'] * item['don_gia'])
        print(
            f"{item['id']} | {item['ten_hang']} | {item['khoi_luong']} kg | "
            f"{item['don_gia']:,} VNĐ | {item['loai_don']} | Thành tiền: {thanh_tien:,} VNĐ"
        )


def them_lo_hang(danh_sach):
    ma_moi = kiem_tra_ma(input("Nhập mã giao dịch: "), danh_sach)
    if not ma_moi:
        return

    ten_hang = chuan_hoa_ten_hang(input("Nhập tên hàng: "))
    if not ten_hang:
        return

    khoi_luong = nhap_khoi_luong()
    if khoi_luong is None:
        return

    don_gia = nhap_don_gia()
    if don_gia is None:
        return

    loai_don = kiem_tra_loai_don(input("Nhập loại đơn (nhap/xuat): "))
    if not loai_don:
        return

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


def xoa_lo_hang(danh_sach):
    ma_xoa = input("Nhập mã giao dịch cần xóa: ").strip().upper()
    for vi_tri, item in enumerate(danh_sach):
        if item['id'] == ma_xoa:
            danh_sach_moi = danh_sach[:vi_tri] + danh_sach[vi_tri + 1:]
            if not kiem_tra_hang_ton_kho(danh_sach_moi):
                print("Lỗi: Xóa giao dịch này sẽ dẫn đến tồn kho âm. Không thể xóa giao dịch.")
                return
            del danh_sach[vi_tri]
            print("Xóa thành công giao dịch!")
            return
    print("Không tìm thấy mã giao dịch.")


def sua_lo_hang(danh_sach):
    ma_sua = input("Nhập mã giao dịch cần sửa: ").strip().upper()
    for vi_tri, item in enumerate(danh_sach):
        if item['id'] == ma_sua:
            print(f"Đang sửa giao dịch {ma_sua} ({item['ten_hang']} - {item['loai_don']})")
            print("Nhập giá trị mới (hoặc nhấn Enter để giữ nguyên giá trị cũ):")

            khoi_luong_moi = item['khoi_luong']
            don_gia_moi = item['don_gia']

            kl_input = input(f"Khối lượng mới [{item['khoi_luong']}]: ").strip()
            if kl_input:
                val = xuly_khoi_luong_nhap(kl_input)
                if val is None:
                    return
                khoi_luong_moi = val

            dg_input = input(f"Đơn giá mới [{item['don_gia']}]: ").strip()
            if dg_input:
                val = xuly_don_gia_nhap(dg_input)
                if val is None:
                    return
                don_gia_moi = val

            lo_hang_sua = {
                **item,
                'khoi_luong': khoi_luong_moi,
                'don_gia': don_gia_moi,
            }

            danh_sach_moi = danh_sach[:vi_tri] + [lo_hang_sua] + danh_sach[vi_tri + 1:]
            if not kiem_tra_hang_ton_kho(danh_sach_moi):
                print("Hủy thao tác sửa do vi phạm tồn kho âm.")
                return

            danh_sach[vi_tri] = lo_hang_sua
            print("Cập nhật thông tin giao dịch thành công!")
            return

    print("Không tìm thấy mã giao dịch.")


def main():
    while True:
        print("\n--- MENU ---")
        print("1. Xem danh sách hàng tồn kho")
        print("2. Thêm giao dịch mới")
        print("3. Xóa giao dịch")
        print("4. Sửa giao dịch")
        print("0. Thoát chương trình")

        lua_chon = input("Nhập lựa chọn của bạn (0-4): ")
        if lua_chon == "1":
            hien_thi_danh_sach(danh_sach_hang)
        elif lua_chon == "2":
            them_lo_hang(danh_sach_hang)
        elif lua_chon == "3":
            xoa_lo_hang(danh_sach_hang)
        elif lua_chon == "4":
            sua_lo_hang(danh_sach_hang)
        elif lua_chon == "0":
            print("Đã đóng chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()