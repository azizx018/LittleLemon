
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # 
    # ath('menu-items', views.MenuItemView.as_view()),
    path('category', views.CategoryView.as_view()),
    path('cart', views.CartView.as_view()),
    path('orders', views.OrderItemView.as_view()),
    path('orders/<int:id>/', views.single_order),
    # path('menu-items/<id>', views.SingleMenuItemView.as_view()),
    path('menu-items/', views.menu_items),
    path('menu-items/<int:id>/', views.single_item),
    path('secret/', views.secret),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
    path('groups/manager/users', views.managers),
    # path('category/', views.category),
    
]