from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DocGia

class DangKyForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    ho_ten = forms.CharField(max_length=200, label="Họ tên")
    ngay_sinh = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Ngày sinh")
    dia_chi = forms.CharField(max_length=300, required=False, label="Địa chỉ")
    dien_thoai = forms.CharField(max_length=10, required=False, label="Điện thoại")
    loai_doc_gia = forms.ChoiceField(choices=DocGia.LOAI_DOC_GIA_CHOICES, label="Loại độc giả")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Tao DocGia lien ket
            doc_gia = DocGia.objects.create(
                user=user,
                ho_ten=self.cleaned_data['ho_ten'],
                ngay_sinh = self.cleaned_data['ngay_sinh'],
                dia_chi = self.cleaned_data['dia_chi'],
                email=self.cleaned_data['email'],
                dien_thoai=self.cleaned_data['dien_thoai'],
                loai_doc_gia=self.cleaned_data['loai_doc_gia'],
            )
            # Tao the thu vien mac dinh (han 1 nam)
            from.models import The
            from datetime import date, timedelta
            The.objects.create(
                ma_doc_gia=doc_gia,
                ngay_cap=date.today(),
                ngay_het_han=date.today() + timedelta(days=365),
                loai_the='Thuong',
                trang_thai='Hop le'
            )
            return user