from django.urls import path
from .views import(
    RegistUserView,HomeView,UserLoginView,
    UserLogoutView,RegistAdminUserView,UserListView,UserHomeView,
    approval_list,admin_approval_required,admin_approval,
)
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name = 'regist'),
    path('user_login/', UserLoginView.as_view(), name = 'user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('admin_regist/', RegistAdminUserView.as_view(), name = 'admin_regist'),
    path('user_list/', UserListView.as_view(), name = 'user_list'),
    path('user_home/<int:pk>/', UserHomeView.as_view(), name = 'user_home'),
    path('approval_list/', approval_list, name = 'approval_list'),
    path('admin_approval_required/', admin_approval_required, name = 'admin_approval_required'),
    path('admin_approval/<int:pk>/', admin_approval, name='admin_approval'),
        # パスワードリセットの開始
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # パスワードリセット完了
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # パスワードリセットの確認
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # パスワードリセット完了
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    
]