from django.urls import path
from .views import(
    RegistUserView,HomeView,UserLoginView,
    UserLogoutView,RegistAdminUserView,
    Users_list,approval_list,admin_approval_required,admin_approval
)

app_name = 'accounts'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name = 'regist'),
    path('user_login/', UserLoginView.as_view(), name = 'user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('admin_regist/', RegistAdminUserView.as_view(), name = 'admin_regist'),
    path('user_list/', Users_list, name = 'user_list'),
    path('approval_list/', approval_list, name = 'approval_list'),
    path('admin_approval_required/', admin_approval_required, name = 'admin_approval_required'),
    path('admin_approval/<int:pk>/', admin_approval, name='admin_approval'),
]