from rest_framework import serializers
from .models import AppReview

class AppReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppReview
        fields = '__all__'