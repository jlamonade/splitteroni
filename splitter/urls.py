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
    BillUpdateTaxPercentView,
    BillUpdateTaxAmountView,
    BillDeleteView,
)


urlpatterns = [
    # Bill links
    path('new/', BillCreateView.as_view(), name='bill-create'),
    path('<uuid:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('archive/', BillListView.as_view(), name='bill-list'),
    path('<uuid:pk>/update/', BillUpdateView.as_view(), name='bill-update'),
    path('<uuid:pk>/update-tax-percent/',
         BillUpdateTaxPercentView.as_view(),
         name='bill-update-tax-percent'),
    path('<uuid:pk>/update-tax-amount/',
         BillUpdateTaxAmountView.as_view(),
         name='bill-update-tax-amount'),
    path('<uuid:pk>/delete/', BillDeleteView.as_view(), name='bill-delete'),

    # Person links
    path('<uuid:pk>/add-person/', PersonCreateView.as_view(), name='person-create'),
    path('person/<uuid:pk>/delete/', PersonDeleteView.as_view(), name='person-delete'),

    # Item links
    path('<uuid:bill_id>/<uuid:person_id>/add-item/',
         ItemCreateView.as_view(),
         name='item-create'
         ),
    path('<uuid:bill_id>/add-shared-item/',
         SharedItemCreateView.as_view(),
         name='shared-item-create'
         ),
    path('item/<uuid:pk>/item-delete/', ItemDeleteView.as_view(), name='item-delete'),
]