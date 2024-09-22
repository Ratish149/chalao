from django.db import models
import uuid
# Create your models here.

class Job(models.Model):
    REMOTE_CHOICES={
        ('Hybrid','Hybrid'),
        ('Onsite','Onsite'),
        ('Remote','Remote'),
    }
    job_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    job_location = models.CharField(max_length=100)
    open_positions = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    remote_type=models.CharField(max_length=100,choices=REMOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.job_id:
            self.job_id = self.generate_job_id()
        super().save(*args, **kwargs)

    def generate_job_id(self):
        random_id = uuid.uuid4().int >> 64  # Get a large random integer from UUID
        return f'JR-{str(random_id)[:7].zfill(7)}'  # Format it like JR-XXXXXXX

    def __str__(self):
        return f"{self.job_title} ({self.job_id})"
    
class JobApplications(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone_number=models.IntegerField()
    resume=models.FileField(upload_to='resume')
    address=models.CharField(max_length=100)
    linkedin_profile=models.URLField(blank=True,null=True)
    github_profile = models.URLField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.job.job_title}"