from django.urls import path
from .views import JobListCreateView, JobRetrieveUpdateDestroyAPIView, JobApplicationListCreateView

urlpatterns = [
    # Job-related URLs
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<str:job_id>/', JobRetrieveUpdateDestroyAPIView.as_view(), name='job-detail'),
    
    # Job Application URL
    path('jobs/<str:job_id>/apply/', JobApplicationListCreateView.as_view(), name='job-application-create'),
]