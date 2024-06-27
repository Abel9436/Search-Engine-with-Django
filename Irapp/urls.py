# irapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.search, name='search'),
     path('document/<int:doc_id>/', views.view_document, name='view_document'),
]
