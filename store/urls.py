from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
	path('', portfolio, name="portfolio"),
	path('store/', store, name="store"),
	path('products/', products, name="products"),
	path('cart/', cart, name="cart"),
	path('checkout/', checkout, name="checkout"),

    path('update_item/', csrf_exempt(updateItem), name='update_item'),
    path('delete/<int:id>/', csrf_exempt(delete_item), name='delete'),
    path('login/', csrf_exempt(login_view), name='login'),
    path('register/', csrf_exempt(register), name='register'),
    path('logout/', logout_view, name='logout'),
    path('lebenslauf', show_pdf, name="lebenslauf"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="auth/reset_password.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"),
         name='password_reset_complete'),

]
