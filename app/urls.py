from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('update_item_detail/', views.updateItemDetail, name="update_item_detail"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('product/', views.product, name="product"),
    path('product_detail/<int:product_id>/', views.productDetail, name='product_detail'),
    path('profile/', views.profile, name="profile"),
    path('remove_from_cart/<int:cart_product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
