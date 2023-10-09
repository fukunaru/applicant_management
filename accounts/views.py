
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import RegistForm, UserLoginForm, AdminRegistForm
from .models import Users
from django.http import JsonResponse
from django.db import transaction


# ユーザーホーム画面
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_user_related_applicants(self):
        user_related_applicants = Users.objects.filter(user=self.request.user)
        return user_related_applicants

    def get_user_related_events(self):
        user_related_applicants = self.get_user_related_applicants()
        event_data = []
        for applicant in user_related_applicants:
            event_data.append({
                'title': applicant.username,
                'start': applicant.interview_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'url': reverse_lazy('applicant:applicant_detail', kwargs={'pk': applicant.pk}),
            })
        return event_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicants'] = self.get_user_related_applicants()
        context['events'] = self.get_user_related_events()
        context['is_pending_approval'] = self.request.user.is_pending_approval
        return context

    @staticmethod
    def calendar_view(request):
        home_view = HomeView()
        events = home_view.get_user_related_events()
        return JsonResponse(events, safe=False)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                if not request.user.is_pending_approval:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    return redirect('accounts:admin_approval_required')
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('accounts:user_login')

# ユーザー登録フォーム
class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:user_login')

# 管理者ユーザー登録フォーム
class RegistAdminUserView(CreateView):
    template_name = 'admin_regist.html'
    form_class = AdminRegistForm
    success_url = reverse_lazy('accounts:user_login')

    def form_valid(self, form):
        user = form.save(commit=False)
        if user.is_admin:
            user.is_pending_approval = True
        user.save()
        return super().form_valid(form)

# ユーザーログイン
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

# ユーザーログイン
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        user = form.get_user()
        remember = form.cleaned_data['remember']
        
        if user.is_pending_approval:
            return redirect('accounts:admin_approval_required')

        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)


# ユーザーログアウト
class UserLogoutView(LogoutView):
    pass

# ユーザー一覧
@login_required
def Users_list(request):
    users = Users.objects.filter(is_pending_approval=True)
    context = {'users': users}
    return render(request, 'user_list.html', context)

# # 承認待ちユーザー一覧
@login_required
def approval_list(request,):
    users = Users.objects.filter(
        is_pending_approval=True,
        is_first_admin=False,
    )
    return render(request, 'approval_list.html', {'users': users})

# # ユーザー承認
@login_required
def admin_approval(request, pk):
    print('ビューが呼び出されました')
    user = get_object_or_404(Users, pk=pk)
    print(user.pk)
    if request.method == 'POST':
        print('POSTが呼び出されました')
        user.is_pending_approval = False
        print(user)
        print(user.is_pending_approval)
        user.save()
        transaction.commit()
        print(Users.objects.get(pk=pk))
    return redirect('accounts:approval_list')

# 管理者による承認
# @login_required
# def admin_approval(request, approvor_id):
#     print("admin_approval ビューが呼び出されました。")
#     user = get_object_or_404(Users,pk=approvor_id)
#     print(user)
#     if request.method == 'POST':
#             print("POSTリクエストが送信されました。")
#             print(user)
#             if user.is_pending_approval:
#                 print("is_pending_approval は True です。")
#                 user.is_pending_approval = False
#                 user.save()
#                 print("ユーザーが保存されました。")
#                 return redirect('accounts:approval_list')
#             else:
#                 # すでに承認済みの場合、メッセージを表示するか別の処理を実行する
#                 message = "このユーザーは既に承認されています。"
#                 return render(request, 'approval_list.html', {'message': message})
#     else:
#             return render(request, 'admin_approval.html', {'user': user})
# @login_required
# def admin_approval(request,approvor_id):
#     if request.method == 'POST':
#         approvor_id = request.POST.get('approvor_id')
#         user = get_object_or_404(Users, id=approvor_id, is_pending_approval=True)

#         # 承認処理を行う
#         user.is_pending_approval = False
#         user.save()

#         # 承認後、再度 approval_list ビューにリダイレクト
#         return redirect('accounts:approval_list')
    # else:
    #     # GETリクエストの場合の処理
    #     # フォームを送信しないで直接アクセスされた場合の対策
    #     return HttpResponseBadRequest("Bad Request")
    

# ログインユーザーが承認待ちの場合のホーム画面
def admin_approval_required(request):
    if request.user.is_pending_approval and request.user.is_admin:
        message = "承認が必要なアカウントです。管理者の承認をお待ちください。"
        return render(request, 'admin_approval_required.html', {'message': message})
    else:
        # 承認済みユーザーはホームページにリダイレクト
        return redirect('accounts:home')
