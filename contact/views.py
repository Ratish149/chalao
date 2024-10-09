from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from django.core.mail import send_mail  # Import send_mail
from django.conf import settings  # Import settings
# Create your views here.


class ContactView(ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        name=request.data.get('name')
        email=request.data.get('email')
        phone_number=request.data.get('phone_number')
        message=request.data.get('message')
        contact = Contact.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            message=message
        )
        
        contact.save()

        # New code to send an email with error handling
        try:
            send_mail(
                'Thank you for your message',  # Subject
                f'Hi {name},\n\nThank you for reaching out! We have received your message:\n\n"{message}"\n\nBest regards,\nYour Company',  # Message
                settings.DEFAULT_FROM_EMAIL,  # Use the default from email
                [email],  # Recipient email
                fail_silently=False,
            )
        except Exception as e:
            return Response({'Message': 'Failed to send message', 'Error': str(e)}, status=500)

        return Response({'Message': 'Message Send Successfully'})
