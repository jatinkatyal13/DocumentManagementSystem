from django.urls import path
from django.contrib.auth.decorators import login_required

from main import views

urlpatterns = [
    path('', login_required(views.MyFilesListView.as_view())),
    path('file/<int:pk>', login_required(views.FileDetailView.as_view())),
    path('file/<int:pk>/edit', login_required(views.FileUpdateView.as_view())),
    path('file/new', login_required(views.FileCreateView.as_view()))
]

