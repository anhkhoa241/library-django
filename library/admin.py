from django.contrib import admin
from .models import (
    TheLoai, Ke, ThuVienLienKet, DocGia, NhanVien,
    Sach, The, PhieuNhap, PhieuMuon,ChiTietMuon, PhieuTra
)

# Dang ky all model
admin.site.register(TheLoai)
admin.site.register(Ke)
admin.site.register(ThuVienLienKet)
admin.site.register(DocGia)
admin.site.register(NhanVien)
admin.site.register(Sach)
admin.site.register(The)
admin.site.register(PhieuNhap)
admin.site.register(PhieuMuon)
admin.site.register(ChiTietMuon)
admin.site.register(PhieuTra)