from django.urls import path
from .views import BlogListCreateView, BlogRetrieveUpdateDestroyView

urlpatterns = [
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogRetrieveUpdateDestroyView.as_view(), name='blog-detail'),
]
