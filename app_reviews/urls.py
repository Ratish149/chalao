from django.urls import path
from .views import AppReviewListCreateView, AppReviewRetrieveUpdateDestroyView

urlpatterns = [
    path('reviews/', AppReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<str:review_id>/', AppReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
]