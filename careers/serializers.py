from rest_framework import serializers
from .models import Job, JobApplications

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('job_id',)        

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplications
        fields = ['id', 'job', 'full_name', 'phone_number', 'email', 'resume', 'address', 'linkedin_profile', 'github_profile', 'applied_at']