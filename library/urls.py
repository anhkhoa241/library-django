from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dang-ky/', views.register, name='register'),
    path('dang-nhap/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('dang-xuat/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Se them cac url khac sau 
    path('muon-sach/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('tra-sach/<int:phieu_id>/', views.return_book, name='return_book'),
    path('danh-sach-sach/', views.book_list, name='book_list'), # Dòng này cực kỳ quan trọng
    path('sach/<int:pk>/', views.book_detail, name='book_detail'),
    path('lich-su-muon/', views.borrow_history, name='borrow_history'),

]

