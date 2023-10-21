
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetView,PasswordContextMixin
from django.urls import reverse_lazy
from .forms import RegistForm, UserLoginForm, AdminRegistForm
from .models import Users
from applicant.models import Applicant
from django.http import JsonResponse
from django.db import transaction
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.views.generic.list import ListView
from datetime import datetime
from django.views.generic.edit import FormView





# ユーザーホーム画面
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_user_related_applicants(self):
        user_related_applicants = Applicant.objects.filter(user=self.request.user)
        return user_related_applicants

    def get_user_related_events(self):
        user_related_applicants = self.get_user_related_applicants()
        event_data = []
        for applicant in user_related_applicants:
            event_data.append({
                'title': applicant.name,
                'start': applicant.interview_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
                'url': reverse_lazy('applicant:applicant_detail', kwargs={'pk': applicant.pk}),
            })
        return event_data



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ユーザーの進捗情報を取得して統計情報を計算
        user_related_applicants = self.get_user_related_applicants()
        total_interviews = user_related_applicants.filter(status='面接中').count()
        total_selection_in_progress = user_related_applicants.filter(status='選考中').count()
        total_offers = user_related_applicants.filter(status='内定').count()

        context['interviews_in_progress'] = total_interviews
        context['selection_in_progress'] = total_selection_in_progress
        context['offers'] = total_offers

        # 今月の面談数を取得
        current_month = datetime.now().month
        interviews_this_month = user_related_applicants.filter(
            status='面接中',
            interview_date_time__month=current_month
        ).count()

        context['interviews_this_month'] = interviews_this_month

        # 今月中の面接中の申請者数を取得
        current_date = datetime.now()
        interviews_in_progress_this_month = user_related_applicants.filter(
            status='面接中',
            interview_date_time__month=current_date.month,
            interview_date_time__year=current_date.year
        ).count()

        # 今月中の選考中の申請者数を取得
        selection_in_progress_this_month = user_related_applicants.filter(
            status='選考中',
            interview_date_time__month=current_date.month,
            interview_date_time__year=current_date.year
        ).count()

        context['interviews_in_progress_this_month'] = interviews_in_progress_this_month
        context['selection_in_progress_this_month'] = selection_in_progress_this_month

        # カレンダーイベントを取得
        context['events'] = self.get_user_related_events()

        # 応募者情報もコンテキストに追加
        context['applicants'] = user_related_applicants

        # 追加の情報を取得
        selection_done_this_month = user_related_applicants.filter(
            status='内定',
            interview_date_time__month=current_month
        ).count()
        context['selection_done_this_month'] = selection_done_this_month

        selection_done_all = user_related_applicants.filter(status='内定').count()
        context['selection_done_all'] = selection_done_all

        interviews_in_progress_all = user_related_applicants.filter(status='面接中').count()
        context['interviews_in_progress_all'] = interviews_in_progress_all

        selection_in_progress_all = user_related_applicants.filter(status='選考中').count()
        context['selection_in_progress_all'] = selection_in_progress_all

        return context


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
    
    def form_valid(self, form):
        user = form.save(commit=False) 
        user.is_pending_approval = False
        user.save()
        self.success_url = reverse_lazy('accounts:user_login')
        return super().form_valid(form)
# 管理者ユーザー登録フォーム
class RegistAdminUserView(CreateView):
    template_name = 'admin_regist.html'
    form_class = AdminRegistForm
    
    def form_valid(self, form):
        user = form.save(commit=False)  
        user.is_admin = True  
        
        if not Users.objects.filter(is_first_admin=True).exists():
            user.is_first_admin = True 
            user.is_pending_approval = False
            
        else:
            user.is_first_admin = False
            user.is_pending_approval = True
            
            
        user.save()
        
        self.success_url = reverse_lazy('accounts:user_login')
  
        return super().form_valid(form)

    


# ユーザーログイン
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        user = form.get_user()

        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)
    


# ユーザーログアウト
class UserLogoutView(LogoutView):

  def dispatch(self, request):
    logout(request)
    request.session.flush()
    return redirect('accounts:user_login')


# ユーザー一覧View
class UserListView(ListView):

  template_name = 'user_list.html'

  def get_queryset(self):
    return Users.objects.filter(is_admin=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['users'] = self.get_queryset()
    return context

# 指定ユーザーホームView  

class UserHomeView(TemplateView):

  template_name = 'user_home.html'

  def get_context_data(self, **kwargs):

    user = get_object_or_404(Users, pk=kwargs['pk'])

    context = super().get_context_data(**kwargs)

    # カレンダーイベント取得
    context['events'] = self.get_calendar_events(user)  

    # 申請一覧取得
    context['applicants'] = Applicant.objects.filter(user=user)

    context['user'] = user
    
    current_month = datetime.now().month
    interviews_this_month = Applicant.objects.filter(
    status='面接中',
    interview_date_time__month=current_month
    ).count()
    context['interviews_this_month'] = interviews_this_month
    
    current_date = datetime.now()
    interviews_in_progress_this_month = Applicant.objects.filter(
    status='面接中',
    interview_date_time__month=current_date.month,
    interview_date_time__year=current_date.year
    ).count()
    context['interviews_in_progress_this_month'] = interviews_in_progress_this_month
    
    current_date = datetime.now()
    selection_in_progress_this_month = Applicant.objects.filter(
    status='選考中',
    interview_date_time__month=current_date.month,
    interview_date_time__year=current_date.year
    ).count()
    context['selection_in_progress_this_month'] = selection_in_progress_this_month

    current_date = datetime.now()
    selection_done_this_month = Applicant.objects.filter(
    status='内定',
    interview_date_time__month=current_date.month,
    interview_date_time__year=current_date.year
    ).count()
    context['selection_done_this_month'] = selection_done_this_month
    
    selection_done_all = Applicant.objects.filter(status='内定').count()
    context['selection_done_all'] = selection_done_all
    
    interviews_in_progress_all = Applicant.objects.filter(status='面接中').count()
    context['interviews_in_progress_all'] = interviews_in_progress_all
    
    selection_in_progress_all = Applicant.objects.filter(status='選考中').count()
    context['selection_in_progress_all'] = selection_in_progress_all




    return context

  def get_calendar_events(self, user):

    events = []

    applicants = Applicant.objects.filter(user=user)

    for applicant in applicants:

      events.append({
        'title': applicant.name,
        'start': applicant.interview_date_time,  
      })

    return events





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
        print("User saved") 
        print(user.is_pending_approval)
        print(Users.objects.get(pk=pk))
    return redirect('accounts:approval_list')
    

# ログインユーザーが承認待ちの場合のホーム画面
@login_required
def admin_approval_required(request):
    if request.user.is_pending_approval and request.user.is_admin:
        message = "承認が必要なアカウントです。管理者の承認をお待ちください。"
        return render(request, 'admin_approval_required.html', {'message': message})
    else:
        # 承認済みユーザーはホームページにリダイレクト
        return redirect('accounts:home')



