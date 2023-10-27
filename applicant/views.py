from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from applicant.models import Applicant
from .forms import ApplicantForm,ApplicantSearchForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import json

class ApplicantListView(LoginRequiredMixin,ListView):
    model = Applicant
    template_name = 'applicants/applicant_list.html'

    
    def get_queryset(self):
        # ログインユーザーに関連付けられた顧客のみをフィルタリング
        return Applicant.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # show_applicant_tabs をコンテキストに追加
        context['show_applicant_tabs'] = True  # 顧客リスト画面ではタブを表示する
        # 他のコンテキスト変数を追加できます
        return context


class ApplicantDetailView(DetailView):
    model = Applicant
    template_name = 'applicants/applicant_detail.html'
    context_object_name = 'applicant'
    
    def get(self, request, *args, **kwargs):
        # ブレークポイントを設定
        # import pdb; pdb.set_trace()

        # pkパラメータの値を取得
        applicant_pk = self.kwargs['pk']
        print("pk:", applicant_pk)

        # モデルから該当オブジェクトを取得
        applicant = get_object_or_404(Applicant, pk=applicant_pk)
        print("Applicant:", applicant)

        return super().get(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicant'] = self.get_object()  # ここでapplicantオブジェクトを追加
        return context
       

class ApplicantCreateView(CreateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'applicants/applicant_create.html'
    success_url = reverse_lazy('applicant:applicant_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # show_applicant_tabs をコンテキストに追加
        context['show_applicant_tabs'] = True  # 顧客リスト画面ではタブを表示する
        # 他のコンテキスト変数を追加できます
        return context
    

class ApplicantUpdateView(UpdateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'applicants/applicant_update.html'
    success_url = reverse_lazy('applicant:applicant_list')
    
    
class ApplicantDeleteView(DeleteView):
    model = Applicant
    template_name = 'applicants/applicant_confirm_delete.html'
    success_url = reverse_lazy('applicant:applicant_list')
    

class ApplicantSearchView(View):
    template_name = 'applicants/applicant_search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # show_applicant_tabs をコンテキストに追加
        context['show_applicant_tabs'] = True  # 顧客リスト画面ではタブを表示する
        # 他のコンテキスト変数を追加できます
        return context

    def get(self, request, *args, **kwargs):
        form = ApplicantSearchForm(request.GET)
        applicants = self.get_queryset(form)

        context = {'form': form, 'applicants': applicants}
        return render(request, self.template_name, context)

    def get_queryset(self, form=None):
        queryset = Applicant.objects.all()

        if form and form.is_valid():
            # フォームから送信されたデータを取得
            name = form.cleaned_data.get('name')
            age_min = form.cleaned_data.get('age_min')
            age_max = form.cleaned_data.get('age_max')
            gender = form.cleaned_data.get('gender')
            current_occupation = form.cleaned_data.get('current_occupation')
            current_salary_min = form.cleaned_data.get('current_salary_min')
            current_salary_max = form.cleaned_data.get('current_salary_max')
            qualifications_experience = form.cleaned_data.get('qualifications_experience')
            desired_salary_min = form.cleaned_data.get('desired_salary_min')
            desired_salary_max = form.cleaned_data.get('desired_salary_max')
            desired_position_company = form.cleaned_data.get('desired_position_company')
            features = form.cleaned_data.get('features')
            post_transition_salary_min = form.cleaned_data.get('post_transition_salary_min')
            post_transition_salary_max = form.cleaned_data.get('post_transition_salary_max')
            post_transition_company = form.cleaned_data.get('post_transition_company')
            interview_date_time_min = form.cleaned_data.get('interview_date_time_min')
            interview_date_time_max = form.cleaned_data.get('interview_date_time_max')
            status = form.cleaned_data.get('status')

            # フィルタリング条件を作成
            filters = {}

            if name:
                filters['name__icontains'] = name

            if age_min:
                filters['age__gte'] = age_min

            if age_max:
                filters['age__lte'] = age_max

            if gender:
                filters['gender'] = gender

            if current_occupation:
                filters['current_occupation__icontains'] = current_occupation

            if current_salary_min:
                filters['current_salary__gte'] = current_salary_min

            if current_salary_max:
                filters['current_salary__lte'] = current_salary_max

            if qualifications_experience:
                filters['qualifications_experience__icontains'] = qualifications_experience

            if desired_salary_min:
                filters['desired_salary__gte'] = desired_salary_min

            if desired_salary_max:
                filters['desired_salary__lte'] = desired_salary_max

            if desired_position_company:
                filters['desired_position_company__icontains'] = desired_position_company

            if features:
                filters['features__icontains'] = features

            if post_transition_salary_min:
                filters['post_transition_salary__gte'] = post_transition_salary_min

            if post_transition_salary_max:
                filters['post_transition_salary__lte'] = post_transition_salary_max

            if post_transition_company:
                filters['post_transition_company__icontains'] = post_transition_company

            if interview_date_time_min:
                filters['interview_date_time__gte'] = interview_date_time_min

            if interview_date_time_max:
                filters['interview_date_time__lte'] = interview_date_time_max

            if status:
                filters['status'] = status

            # クエリセットをフィルタリング
            queryset = queryset.filter(**filters)

        return queryset
    
    


def calendar_view(request):
    user = request.user  # ログインしているユーザーを取得
    applicants = Applicant.objects.filter(user=user)  # ユーザーに関連する応募者を取得
    events = []  # カレンダーに表示するイベントデータを格納するリスト

    # 応募者から面談日時と名前のデータを取得し、eventsリストに追加
    for applicant in applicants:

        event = {
            'title': applicant.name,
            'start': applicant.interview_date_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        events.append(event)

    # eventsデータをJSON形式に変換
    events_json = json.dumps(events)

    context = {'events_json': events_json, 'applicants': applicants }
    return render(request, 'calendar/calendar.html', context)