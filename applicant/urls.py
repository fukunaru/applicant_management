from django.urls import path
from .views import (ApplicantCreateView,ApplicantDeleteView,ApplicantDetailView,
                    ApplicantUpdateView,ApplicantListView,ApplicantSearchView,calendar_view
    
)

app_name = 'applicant'

urlpatterns = [
    path('applicant_list/', ApplicantListView.as_view(), name = 'applicant_list'),
    path('applicant_detail/<int:pk>/', ApplicantDetailView.as_view(), name = 'applicant_detail'),
    path('applicant_update/<int:pk>/', ApplicantUpdateView.as_view(), name = 'applicant_update'),
    path('applicant_delete/<int:pk>/', ApplicantDeleteView.as_view(), name = 'applicant_delete'),
    path('applicant_create/', ApplicantCreateView.as_view(), name = 'applicant_create'),
    path('applicant_search/', ApplicantSearchView.as_view(), name = 'applicant_search'),
    path('calendar/',calendar_view, name = 'calendar'),
    
]