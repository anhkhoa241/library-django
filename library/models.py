from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class TheLoai (models.Model):
    ten_the_loai = models.CharField(max_length=100, unique=True, verbose_name="Tên thể loại")
    mo_ta = models.CharField(max_length=300, blank=True, null=True, verbose_name="Mô tả")

    class Meta:
        db_table = 'TheLoai'
        verbose_name = 'Thể loại'
        verbose_name_plural = 'Thể loại'

    def __str__(self):
        return self.ten_the_loai

class Ke(models.Model):
    LOAI_KE_CHOICES = [
        ('Thuong', 'Thường'),
        ('Dac biet', 'Đặc biệt'),
        ('Tai lieu so', 'Tài liệu số'),
    ]
    loai_ke = models.CharField(max_length=30, choices=LOAI_KE_CHOICES, verbose_name="Loại kệ")
    vi_tri = models.CharField(max_length=100, verbose_name="Vị trí")
    suc_chua_toi_da = models.PositiveIntegerField(verbose_name="Sức chứa tối đa")
    so_luong_hien_tai = models.PositiveIntegerField(default=0, verbose_name="Số lượng hiện tại")

    class Meta:
        db_table = 'Ke'
        verbose_name = 'Kệ'
        verbose_name_plural = 'Kệ'

    def __str__(self):
        return f"{self.loai_ke} - {self.vi_tri}"

class ThuVienLienKet(models.Model):
    ten_thu_vien = models.CharField(max_length=200, verbose_name="Tên thư viện")
    dia_chi = models.CharField(max_length=300, blank=True, null=True, verbose_name="Địa chỉ")
    chinh_sach_muon = models.TextField(blank=True, null=True, verbose_name="Chính sách mượn")
    so_ngay_muon_toi_da = models.PositiveIntegerField(default=7, verbose_name="Số ngày mượn tối đa")
    dang_hoat_dong = models.BooleanField(default=True, verbose_name="Đang hoạt động")

    class Meta:
        db_table = 'ThuVienLienKet'
        verbose_name = 'Thư viện liên kết'
        verbose_name_plural = 'Thư viện liên kết'

    def __str__(self):
        return self.ten_thu_vien
    
class DocGia(models.Model):
    LOAI_DOC_GIA_CHOICES = [
        ('Sinh vien', 'Sinh viên'),
        ('Giang vien', 'Giảng viên'),
        ('Khach ben ngoai', 'Khách bên ngoài'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ho_ten = models.CharField(max_length=200, verbose_name="Họ tên")
    ngay_sinh = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    dia_chi = models.CharField(max_length=300, blank=True, null=True, verbose_name="Địa chỉ")
    email = models.EmailField(max_length=150, blank=True, null=True, verbose_name="Email")
    dien_thoai = models.CharField(max_length=10, blank=True, null=True, verbose_name="Điện thoại")
    loai_doc_gia = models.CharField(max_length=30, choices=LOAI_DOC_GIA_CHOICES, verbose_name="Loại độc giả")
    tien_coc = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Tiền cọc")
    ngay_tao = models.DateField(default=timezone.now, verbose_name="Ngày tạo")

    class Meta:
        db_table = 'DocGia'
        verbose_name = 'Độc giả'
        verbose_name_plural = 'Độc giả'

    def __str__(self):
        return self.ho_ten
    
class NhanVien(models.Model):
    BO_PHAN_CHOICES = [
        ('Thu thu', 'Thủ thư'),
        ('Nhap sach', 'Nhập sách'),
        ('Quan ly kho', 'Quản lý kho'),
    ]
    QUYEN_HAN_CHOICES = [
        ('Doc', 'Đọc'),
        ('Ghi', 'Ghi'),
        ('Quan tri', 'Quản trị'),
    ]
    ho_ten = models.CharField(max_length=200, verbose_name="Họ tên")
    bo_phan = models.CharField(max_length=50, choices=BO_PHAN_CHOICES, verbose_name="Bộ phận")
    quyen_han = models.CharField(max_length=30, choices=QUYEN_HAN_CHOICES, verbose_name="Quyền hạn")
    email = models.EmailField(max_length=150, blank=True, null=True, verbose_name="Email")
    dien_thoai = models.CharField(max_length=10, blank=True, null=True, verbose_name="Điện thoại")
    dang_lam_viec = models.BooleanField(default=True, verbose_name="Đang làm việc")

    class Meta:
        db_table = 'NhanVien'
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'

    def __str__(self):
        return self.ho_ten

class Sach(models.Model):
    HINH_THUC_NHAP_CHOICES = [
        ('Mua', 'Mua'),
        ('Tang', 'Tặng'),
        ('Lien ket', 'Liên kết'),
    ]
    LOAI_SACH_CHOICES = [
        ('Thuong', 'Thường'),
        ('Dac biet', 'Đặc biệt'),
        ('Tai lieu so', 'Tài liệu số'),
    ]
    ten_sach = models.CharField(max_length=300, verbose_name="Tên sách")
    tac_gia = models.CharField(max_length=200, verbose_name="Tác giả")
    ma_the_loai = models.ForeignKey(TheLoai, on_delete=models.PROTECT, verbose_name="Thể loại")
    nam_xuat_ban = models.PositiveIntegerField(blank=True, null=True, verbose_name="Năm xuất bản")
    nha_xuat_ban = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nhà xuất bản")
    so_luong = models.PositiveIntegerField(default=0, verbose_name="Số lượng")
    hinh_thuc_nhap = models.CharField(max_length=20, choices=HINH_THUC_NHAP_CHOICES, verbose_name="Hình thức nhập")
    loai_sach = models.CharField(max_length=20, choices=LOAI_SACH_CHOICES, verbose_name="Loại sách")
    ma_ke = models.ForeignKey(Ke, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Kệ")
    co_the_duoc_in = models.BooleanField(default=False, verbose_name="Có thể được in")
    ngay_tao = models.DateField(default=timezone.now, verbose_name="Ngày tạo")

    class Meta:
        db_table = 'Sach'
        verbose_name = 'Sách'
        verbose_name_plural = 'Sách'
    
    def __str__(self):
        return self.ten_sach

class The(models.Model):
    LOAI_THE_CHOICES = [
        ('Thuong', 'Thường'),
        ('VIP', 'VIP'),
        ('Lien ket', 'Liên kết'),
    ]
    TRANG_THAI_CHOICES = [
        ('Hop le', 'Hợp lệ'),
        ('Het han', 'Hết hạn'),
        ('Bi khoa', 'Bị khóa'),
    ]
    ma_doc_gia = models.OneToOneField(DocGia, on_delete=models.CASCADE, verbose_name="Độc giả")
    ngay_cap = models.DateField(default=timezone.now, verbose_name="Ngày cấp")
    ngay_het_han = models.DateField(verbose_name="Ngày hết hạn")
    loai_the = models.CharField(max_length=20, choices=LOAI_THE_CHOICES, verbose_name="Loại thẻ")
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='Hop le', verbose_name="Trạng thái")

    class Meta:
        db_table = 'The'
        verbose_name = 'Thẻ'
        verbose_name_plural = 'Thẻ'

    def __str__(self):
        return f"Thẻ {self.loai_the} của {self.ma_doc_gia.ho_ten}"

class PhieuNhap (models.Model): 
    HINH_THUC_NHAP_CHOICES = [
        ('Mua', 'Mua'),
        ('Tang', 'Tặng'),
        ('Lien ket', 'Liên kết'),
    ]
    ma_sach = models.ForeignKey(Sach, on_delete=models.PROTECT, verbose_name="Sách")
    hinh_thuc_nhap = models.CharField(max_length=20, choices=HINH_THUC_NHAP_CHOICES, verbose_name="Hình thức nhập")
    ngay_nhap = models.DateField(default=timezone.now, verbose_name="Ngày nhập")
    nha_cung_cap = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nhà cung cấp")
    ma_lien_ket = models.ForeignKey(ThuVienLienKet, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Thư viện liên kết")
    so_chung_tu = models.CharField(max_length=200, blank=True, null=True, verbose_name="Số chứng từ")
    so_luong_nhap = models.PositiveIntegerField(verbose_name="Số lượng nhập")
    ma_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Nhân viên nhập")
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    class Meta:
        db_table = 'PhieuNhap'
        verbose_name = 'Phiếu nhập'
        verbose_name_plural = 'Phiếu nhập'

    def __str__(self):
        return f"Phiếu nhập #{self.id} - {self.ma_sach.ten_sach}"
    
class PhieuMuon(models.Model):
    HINH_THUC_MUON_CHOICES = [
        ('Tai cho', 'Tại chỗ'),
        ('Mang ve', 'Mang về'),
        ('Online', 'Online'),
    ]
    TRANG_THAI_CHOICES = [
        ('Dang muon', 'Đang mượn'),
        ('Qua han', 'Quá hạn'),
        ('Da tra', 'Đã trả'),
    ]
    ma_doc_gia = models.ForeignKey(DocGia, on_delete=models.PROTECT, verbose_name="Độc giả")
    ngay_muon = models.DateField(default=timezone.now, verbose_name="Ngày mượn")
    ngay_tra_du_kien = models.DateField(verbose_name="Ngày trả dự kiến")
    hinh_thuc_muon = models.CharField(max_length=20, choices=HINH_THUC_MUON_CHOICES, verbose_name="Hình thức mượn")
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='Dang muon', verbose_name="Trạng thái")
    ma_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Nhân viên xử lý")
    ma_lien_ket = models.ForeignKey(ThuVienLienKet, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Thư viện liên kết")

    class Meta:
        db_table = 'PhieuMuon'
        verbose_name = 'Phiếu mượn'
        verbose_name_plural = 'Phiếu mượn'

    def __str__(self):
        return f"Phiếu mượn #{self.id} - {self.ma_doc_gia.ho_ten}"
    
class ChiTietMuon (models.Model):
    ma_phieu_muon = models.ForeignKey(PhieuMuon, on_delete=models.CASCADE, verbose_name="Phiếu mượn")
    ma_sach = models.ForeignKey(Sach, on_delete=models.PROTECT, verbose_name="Sách")
    so_luong = models.PositiveIntegerField(default=1, verbose_name="Số lượng")

    class Meta:
        db_table = 'ChiTietMuon'
        verbose_name = 'Chi tiết mượn'
        verbose_name_plural = 'Chi tiết mượn'
        unique_together = ('ma_phieu_muon', 'ma_sach')

    def __str__(self):
        return f"{self.ma_sach.ten_sach} (SL: {self.so_luong})"
    
class PhieuTra(models.Model):
    TINH_TRANG_CHOICES = [
        ('Binh thuong', 'Bình thường'),
        ('Hu hong', 'Hư hỏng'),
        ('Mat', 'Mất'),
    ]
    ma_phieu_muon = models.OneToOneField(PhieuMuon, on_delete=models.PROTECT, verbose_name="Phiếu mượn")
    ngay_tra = models.DateField(default=timezone.now, verbose_name="Ngày trả")
    tinh_trang_sach = models.CharField(max_length=20, choices=TINH_TRANG_CHOICES, verbose_name="Tình trạng sách")
    phi_tre_han = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Phí trễ hạn")
    phi_hu_hong = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Phí hư hỏng")
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    class Meta:
        db_table = 'PhieuTra'
        verbose_name = 'Phiếu trả'
        verbose_name_plural = 'Phiếu trả'

    def __str__(self):
        return f"Phiếu trả cho phiếu mượn #{self.ma_phieu_muon.id}"
