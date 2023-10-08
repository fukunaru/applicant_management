from django import forms
from .models import Applicant
from accounts.models import Users



class ApplicantForm(forms.ModelForm):
       
    class Meta:
        model = Applicant
        user = forms.ModelChoiceField(queryset=Users.objects.all())

        # admin_user = forms.ModelChoiceField(queryset=AdminUser.objects.all(), required=False)
        fields = [
            'name',
            'age',
            'gender',
            'current_occupation',
            'current_salary',
            'qualifications_experience',
            'desired_salary',
            'desired_position_company',
            'features',
            'resume_file',
            'post_transition_salary',
            'post_transition_company',
            'interview_date_time',
            'status',
        ]
        labels = {
            'name': '名前',
            'age': '年齢',
            'gender': '性別',
            'current_occupation': '現在の職業',
            'current_salary': '現在の給与',
            'qualifications_experience': '資格と経験',
            'desired_salary': '希望給与',
            'desired_position_company': '希望職種・会社',
            'features': '特徴',
            'resume_file': '履歴書',
            'post_transition_salary': '転職後の給与',
            'post_transition_company': '転職後の会社',
            'interview_date_time': '面接日時',
            'status': '選考ステータス',
        }
        
        widgets = {
            'interview_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'qualifications_experience': forms.Textarea(attrs={'rows': 5}),
            'features': forms.Textarea(attrs={'rows': 5}),
        }
        
        
class ApplicantSearchForm(forms.Form):
    GENDER_CHOICES = [
        ('', 'すべて'),
        ('男性', '男性'),
        ('女性', '女性'),
    ]

    SELECTION_PROCESS_CHOICES = [
        ('', 'すべて'),
        ('選考中', '選考中'),
        ('面接中', '面接中'),
        ('内定', '内定'),
    ]

    name = forms.CharField(label='名前', required=False)
    age_min = forms.IntegerField(label='最小年齢', required=False)
    age_max = forms.IntegerField(label='最大年齢', required=False)
    gender = forms.ChoiceField(label='性別', choices=GENDER_CHOICES, required=False)
    current_occupation = forms.CharField(label='現職', required=False)
    current_salary_min = forms.IntegerField(label='最小年収', required=False)
    current_salary_max = forms.IntegerField(label='最大年収', required=False)
    qualifications_experience = forms.CharField(label='資格/経験', required=False)
    desired_salary_min = forms.IntegerField(label='最小希望年収', required=False)
    desired_salary_max = forms.IntegerField(label='最大希望年収', required=False)
    desired_position_company = forms.CharField(label='希望職種/希望企業', required=False)
    features = forms.CharField(label='特徴', required=False)
    post_transition_salary_min = forms.IntegerField(label='最小転職後年収', required=False)
    post_transition_salary_max = forms.IntegerField(label='最大転職後年収', required=False)
    post_transition_company = forms.CharField(label='転職後企業', required=False)
    interview_date_time_min = forms.DateTimeField(label='最小面接日時', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    interview_date_time_max = forms.DateTimeField(label='最大面接日時', required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(label='選考ステータス', choices=SELECTION_PROCESS_CHOICES, required=False)

    # 応募者が提出した履歴書を含む
    resume_file = forms.FileField(label='履歴書', required=False)

    def clean(self):
        cleaned_data = super().clean()
        age_min = cleaned_data.get('age_min')
        age_max = cleaned_data.get('age_max')
        current_salary_min = cleaned_data.get('current_salary_min')
        current_salary_max = cleaned_data.get('current_salary_max')
        desired_salary_min = cleaned_data.get('desired_salary_min')
        desired_salary_max = cleaned_data.get('desired_salary_max')
        post_transition_salary_min = cleaned_data.get('post_transition_salary_min')
        post_transition_salary_max = cleaned_data.get('post_transition_salary_max')
        interview_date_time_min = cleaned_data.get('interview_date_time_min')
        interview_date_time_max = cleaned_data.get('interview_date_time_max')

        if age_min is not None and age_max is not None and age_min > age_max:
            self.add_error('age_min', '最小年齢は最大年齢よりも小さくする必要があります。')
            self.add_error('age_max', '最大年齢は最小年齢よりも大きくする必要があります。')

        if current_salary_min is not None and current_salary_max is not None and current_salary_min > current_salary_max:
            self.add_error('current_salary_min', '最小年収は最大年収よりも小さくする必要があります。')
            self.add_error('current_salary_max', '最大年収は最小年収よりも大きくする必要があります。')

        if desired_salary_min is not None and desired_salary_max is not None and desired_salary_min > desired_salary_max:
            self.add_error('desired_salary_min', '最小希望年収は最大希望年収よりも小さくする必要があります。')
            self.add_error('desired_salary_max', '最大希望年収は最小希望年収よりも大きくする必要があります。')

        if post_transition_salary_min is not None and post_transition_salary_max is not None and post_transition_salary_min > post_transition_salary_max:
            self.add_error('post_transition_salary_min', '最小転職後年収は最大転職後年収よりも小さくする必要があります。')
            self.add_error('post_transition_salary_max', '最大転職後年収は最小転職後年収よりも大きくする必要があります。')

        if interview_date_time_min and interview_date_time_max and interview_date_time_min > interview_date_time_max:
            self.add_error('interview_date_time_min', '最小面接日時は最大面接日時よりも前の日付にする必要があります。')
            self.add_error('interview_date_time_max', '最大面接日時は最小面接日時よりも後の日付にする必要があります.')
