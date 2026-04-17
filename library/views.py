from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import DangKyForm
from .models import Sach, The, PhieuMuon, ChiTietMuon, DocGia, PhieuTra
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


def register(request):
    if request.method == 'POST':
        form = DangKyForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Tài khoản {user.username} đã được tạo thành công!")
            return redirect('home')
    else:
        form = DangKyForm()
    return render(request, 'registration/register.html',{'form': form})

def home(request):
    sach_moi = Sach.objects.order_by('-ngay_tao')[:8] # 8 cuon moi
    context = {'sach_moi': sach_moi}
    return render(request, 'library/home.html', context)

def book_list(request):
    query = request.GET.get('q','')
    sach_list = Sach.objects.all()
    if query:
        sach_list = sach_list.filter(
            Q(ten_sach__icontains=query) |
            Q(tac_gia__icontains=query) |
            Q(ma_the_loai__ten_the_loai__icontains=query)
        ).distinct()
    context = {'sach_list': sach_list, 'query': query}
    return render(request, 'library/book_list.html', context)

def book_detail(request, pk):
    sach = get_object_or_404(Sach, pk=pk)
    return render(request, 'library/book_detail.html', {'sach': sach})

@login_required
def borrow_book(request, book_id):
    sach = get_object_or_404(Sach, pk=book_id)
    user = request.user
    try:
        doc_gia = user.docgia
    except DocGia.DoesNotExist:
        messages.error(request, "Tài khoản của bạn chưa liên kết với độc giả. Vui lòng liên hệ thủ thư.")
        return redirect('book_detail', pk=book_id)
    
    # Kiem tra the
    try:
        the = The.objects.get(ma_doc_gia=doc_gia)
        if the.trang_thai != 'Hop le' or the.ngay_het_han < timezone.now().date():
            messages.error(request, "Thẻ thư viện của bạn không hợp lệ hoặc đã hết hạn.")
            return redirect('book_detail', pk=book_id)
    except The.DoesNotExist:
        messages.error(request, "Bạn chưa có thẻ thư viện.")
        return redirect('book_detail', pk=book_id)
    
    # Kiem tra sach
    if sach.so_luong < 1:
        messages.error(request, "Sách đã hết.")
        return redirect('book_detail', pk=book_id)
    
    # Kiem tra lai sach dac biet
    if sach.loai_sach == 'Dac biet':
        if the.loai_the != 'VIP' and doc_gia.loai_doc_gia != 'Giang vien':
            messages.error(request, "Sách đặc biệt chỉ dành cho thẻ VIP hoặc Giảng viên.")
            return redirect('book_detail', pk=book_id)
        
    # Kiem tra tai lieu so (mac dinh cho muon online, nhung ta co the 'de' form hon sau)
    # Tam thoi neu la tai lieu so, chi cho em online
    if sach.loai_sach == 'Tai lieu so':
        hinh_thuc_muon = 'Online'
    else:
        hinh_thuc_muon = 'Mang ve' # Co the cho chon sau
    
    # Tinh ngay tra du kien theo loai doc gia
    if doc_gia.loai_doc_gia == 'Giang vien':
        ngay_tra_du_kien = timezone.now().date() + timedelta(days=30)
    elif doc_gia.loai_doc_gia == 'Sinh vien':
        ngay_tra_du_kien = timezone.now().date() + timedelta(days=14)
    else:
        ngay_tra_du_kien = timezone.now().date() + timedelta(days=7)

    # Tao phieu muon
    phieu_muon = PhieuMuon.objects.create(
        ma_doc_gia = doc_gia,
        ngay_muon=timezone.now().date(),
        ngay_tra_du_kien=ngay_tra_du_kien,
        hinh_thuc_muon=hinh_thuc_muon,
        trang_thai='Dang muon',
    )

    ChiTietMuon.objects.create(
        ma_phieu_muon=phieu_muon,
        ma_sach=sach,
        so_luong=1
    )

    # Giam so luong sach
    sach.so_luong -= 1
    sach.save()

    messages.success(request, f"Bạn đã mượn thành công cuốn '{sach.ten_sach}'. Hạn trả: {ngay_tra_du_kien}")
    return redirect('borrow_history')

@login_required
def borrow_history(request):
    user = request.user
    try:
        doc_gia = user.docgia
    except DocGia.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin độc giả.")
        return redirect('home')
    
    phieu_muon = PhieuMuon.objects.filter(ma_doc_gia=doc_gia).order_by('-ngay_muon')
    return render(request, 'library/borrow_history.html', {'phieu_muon': phieu_muon})

@login_required
def return_book(request, phieu_id):
    phieu_muon = get_object_or_404(PhieuMuon, pk=phieu_id)
    # Dam bao chi docc gia so huu phieu hoac nhan vien moi duoc tra
    if not request.user.is_staff and request.user.docgia != phieu_muon.ma_doc_gia:
        messages.error(request, "Bạn không có quyền trả phiếu này.")
        return redirect('borrow_history')
    
    if phieu_muon.trang_thai == 'Da tra':
        messages.warning(request, "Phiếu này đã được trả.")
        return redirect('borrow_history')
    
    # Tinh phi tre han (gia su 5000 VND/ngay)
    today = timezone.now().date()
    phi_tre_han = 0
    if today > phieu_muon.ngay_tra_du_kien:
        so_ngay_tre = (today - phieu_muon.ngay_tra_du_kien).days
        phi_tre_han = so_ngay_tre * 5000

    # Tao phieu tra (Gia dinh sach binh thuong, co the cho chon trinh trang sau)

    phieu_tra = PhieuTra.objects.create(
        ma_phieu_muon=phieu_muon,
        ngay_tra=today,
        tinh_trang_sach='Binh thuong',
        phi_tre_han=phi_tre_han,
        phi_hu_hong=0,
        ghi_chu="Trả sách tự động"
    )

    # Cap nhat trang thai phieu muon
    phieu_muon.trang_thai = 'Da tra'
    phieu_muon.save()

    # Hoan kho sachz
    for ct in phieu_muon.chitietmuon_set.all():
        sach = ct.ma_sach
        sach.so_luong += ct.so_luong
        sach.save()

    messages.success(request, f"Trả sách thành công. Tổng phí: {phi_tre_han} VND")

    return redirect('borrow_history')

