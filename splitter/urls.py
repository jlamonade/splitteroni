from django.urls import path

from .views import BillCreateView, BillDetailView, PersonCreateView, PersonDeleteView


urlpatterns = [
    path('new/', BillCreateView.as_view(), name='bill-create'),
    path('<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('<int:pk>/add-person/', PersonCreateView.as_view(), name='person-create'),
    path('person/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),
]