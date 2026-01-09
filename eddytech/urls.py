from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('work/', views.work, name='work'),
    path('contact/', views.contact, name='contact'),
    
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('support/', views.support, name='support'),
]