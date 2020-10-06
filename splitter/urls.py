from django.urls import path

from .views import (
    BillCreateView,
    BillDetailView,
    PersonCreateView,
    PersonDeleteView,
    BillListView,
    ItemCreateView,
    ItemDeleteView,
)


urlpatterns = [
    path('new/', BillCreateView.as_view(), name='bill-create'),
    path('<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('<int:pk>/add-person/', PersonCreateView.as_view(), name='person-create'),
    path('person/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),
    path('archive/', BillListView.as_view(), name='bill-list'),
    path('<int:bill_id>/<int:person_id>/add-item/',
         ItemCreateView.as_view(),
         name='item-create'
         ),
    path('item/<int:pk>/item-delete', ItemDeleteView.as_view(), name='item-delete'),
]