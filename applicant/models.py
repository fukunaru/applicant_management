from django.db import models
from accounts.models import Users


class ApplicantManager(models.Manager):
    
    def create_applicant(self, **kwargs):
        applicant = self.create(**kwargs)
        return applicant



class Applicant(models.Model):
     # 応募者情報
    GENDER_CHOICES = [
        ('男性', '男性'),
        ('女性', '女性'),
    ]
    SELECTION_PROCESS = [
        ('選考中', '選考中'),
        ('面接中', '面接中'),
        ('内定', '内定'),
    ]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    current_occupation = models.CharField(max_length=100)
    current_salary = models.IntegerField()
    qualifications_experience = models.CharField(max_length=200)
    desired_salary = models.IntegerField()
    desired_position_company = models.CharField(max_length=100)
    features = models.CharField(max_length=150)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    post_transition_salary = models.IntegerField(blank=True, null=True)
    post_transition_company = models.CharField(max_length=100, blank=True, null=True)
    interview_date_time = models.DateTimeField()
    status = models.CharField(max_length=15, choices=SELECTION_PROCESS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='applicants')
    
    objects = ApplicantManager()
    
    class Meta:
        db_table = 'applicant'
        app_label = 'schedule'

    