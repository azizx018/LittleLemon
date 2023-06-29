
from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('category', views.CategoryView.as_view()),
    path('cart', views.CartView.as_view()),
    # path('menu-items/<id>', views.SingleMenuItemView.as_view()),
    # path('menu-items/', views.menu_items),
    path('menu-items/<int:id>/', views.single_item),
    # path('category/', views.category),
    
]