from django.urls import path

from .views import (
    BillCreateView,
    BillDetailView,
    PersonCreateView,
    PersonDeleteView,
    BillListView,
    ItemCreateView,
    ItemDeleteView,
    SharedItemCreateView,
    BillUpdateView,
)


urlpatterns = [
    # Bill links
    path('new/', BillCreateView.as_view(), name='bill-create'),
    path('<uuid:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('archive/', BillListView.as_view(), name='bill-list'),
    path('<uuid:pk>/update/', BillUpdateView.as_view(), name='bill-update'),

    # Person links
    path('<uuid:pk>/add-person/', PersonCreateView.as_view(), name='person-create'),
    path('person/<int:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),

    # Item links
    path('<uuid:bill_id>/<int:person_id>/add-item/',
         ItemCreateView.as_view(),
         name='item-create'
         ),
    path('<uuid:bill_id>/add-shared-item/',
         SharedItemCreateView.as_view(),
         name='shared-item-create'
         ),
    path('item/<int:pk>/item-delete/', ItemDeleteView.as_view(), name='item-delete'),
]