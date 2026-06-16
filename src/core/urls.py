from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('marking/', views.MarkingView.as_view(), name='marking'),
    path('quality-control/', views.QualityControlView.as_view(), name='quality_control'),
    path('labeling/', views.LabelingView.as_view(), name='labeling'),
    path('brands/', views.BrandsView.as_view(), name='brands'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]
