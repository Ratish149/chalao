
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Job,JobApplications
from .serializers import JobSerializer,JobApplicationSerializer
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filters = Q()

        job_title = request.query_params.get('job_title', None)
        remote_type = request.query_params.get('remote_type', None)

        if job_title:
            filters &= Q(job_title__icontains=job_title)

        if remote_type:
            filters &= Q(remote_type__icontains=remote_type)

        filtered_queryset = queryset.filter(filters)

        if not filtered_queryset.exists():
            return Response({'Message': 'No jobs found matching the provided filters'})

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        job_title=request.data.get('job_title')
        job_description=request.data.get('job_description')
        job_location=request.data.get('job_location')
        open_positions=request.data.get('open_positions')
        start_date=request.data.get('start_date')
        end_date=request.data.get('end_date')
        remote_type=request.data.get('remote_type')
        job = Job.objects.create(
            job_title=job_title,
            job_description=job_description,
            job_location=job_location,
            open_positions=open_positions,
            start_date=start_date,
            end_date=end_date,
            remote_type=remote_type
        )
        job.save()
        serializer = self.get_serializer(job)
        return Response({'Message': 'Booking Extended Successfully','data':serializer.data}, status=status.HTTP_201_CREATED)

class JobRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'job_id'

class JobApplicationListCreateView(generics.ListCreateAPIView):
    queryset = JobApplications.objects.all()
    serializer_class = JobApplicationSerializer

    def create(self, request, *args, **kwargs):
        job_id=self.kwargs.get('job_id')
        job=Job.objects.get(job_id=job_id)

        full_name=request.data.get('full_name')
        phone_number=request.data.get('phone_number')
        email=request.data.get('email')
        resume=request.data.get('resume')
        address=request.data.get('address')
        linkedin_profile=request.data.get('linkedin_profile')
        github_profile=request.data.get('github_profile')

        job_application = JobApplications.objects.create(
            job=job,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            resume=resume,
            address=address,
            linkedin_profile=linkedin_profile,
            github_profile=github_profile
        )
        job_application.save()
        self.send_email(job_application)
        serializer = self.get_serializer(job_application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def send_email(self,job_application):
        subject = f"Application Summary for {job_application.job.job_title} ({job_application.job.job_id})"
        message = (
            f"Thank you for applying to {job_application.job.job_title}.\n\n"
            f"Here is a summary of your job_application:\n"
            f"Full Name: {job_application.full_name}\n"
            f"Email: {job_application.email}\n"
            f"Phone: {job_application.phone_number}\n"
            f"Address: {job_application.address}\n"
            f"LinkedIn: {job_application.linkedin_profile}\n"
            f"GitHub: {job_application.github_profile}\n"
            f"\nBest of luck!\nChalao Team"
        )
        recipient_email = job_application.email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender's email, ensure you configure this in settings.py
            [recipient_email],
            fail_silently=False,
        )