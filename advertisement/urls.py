from django.urls import path
from .views import AdvertisementListCreateView
urlpatterns = [
    path('advertisements/', AdvertisementListCreateView.as_view(), name='advertisement-list-create'),
]
