from django.urls import path

from main import views

urlpatterns = [
    path('', views.MyFilesListView.as_view()),
    path('file/<int:pk>', views.FileDetailView.as_view()),
    path('file/<int:pk>/edit', views.FileUpdateView.as_view()),
    path('file/new', views.FileCreateView.as_view())
]

