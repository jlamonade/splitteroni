from django.urls import path

from .views import BillCreateView, BillDetailView


urlpatterns = [
    path('new/', BillCreateView.as_view(), name='bill-create'),
    path('<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
]