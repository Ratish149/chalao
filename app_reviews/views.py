from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import AppReview
from rest_framework.response import Response
from .serializers import AppReviewSerializer
# Create your views here.
class AppReviewListCreateView(ListCreateAPIView):
    queryset = AppReview.objects.all()
    serializer_class = AppReviewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return AppReview.objects.all()

    def create(self, request, *args, **kwargs):
        user=request.user
        rating=request.data.get('rating')
        comment=request.data.get('comment')
        app_review = AppReview.objects.create(
            user=user,
            rating=rating,
            comment=comment
        )
        app_review.save()
        serializer = self.get_serializer(app_review)
        return Response(serializer.data)

class AppReviewRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = AppReview.objects.all()
    serializer_class = AppReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        review_id = self.kwargs.get('pk')
        return get_object_or_404(AppReview, id=review_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'Message': 'You are not authorized to update this review'}, status=status.HTTP_403_FORBIDDEN)
        
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        
        if rating is not None:
            instance.rating = rating
        if comment is not None:
            instance.comment = comment
        
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'Message': 'You are not authorized to delete this review'}, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        return Response({'Message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
