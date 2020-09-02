from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from main import models, forms
# Create your views here.

class MyFilesListView(ListView):
    context_object_name = 'files'
    template_name = 'my_files.html'

    def get_queryset(self):
        return models.File.objects.filter(owner = self.request.user)

class FileUpdateView(UpdateView):
   form_class = forms.FileForm
   template_name = 'add_file.html'
   success_url = '/'
   model = models.File
   
   def form_valid(self, form):
        file = form.save()
        document = models.Document.objects.create(
            url = form.cleaned_data['url'],
            markdown = form.cleaned_data['markdown'],
            docType = form.cleaned_data['docType']
        )
        fileVersion = models.FileVersion.objects.create(
            file = file,
            document = document
        )
        return HttpResponseRedirect(f'/file/{file.pk}')

class FileCreateView(CreateView):
    form_class = forms.FileForm
    template_name = 'add_file.html'
    success_url = '/'
    model = models.File
   
    def form_valid(self, form):
        file = form.save(commit = False)
        file.owner = self.request.user
        file.save()
        print(form.cleaned_data)
        document = models.Document.objects.create(
            url = form.cleaned_data['url'],
            markdown = form.cleaned_data['markdown'],
            docType = form.cleaned_data['docType']
        )
        fileVersion = models.FileVersion.objects.create(
            file = file,
            document = document
        )
        return HttpResponseRedirect(f'/file/{file.pk}')

class FileDetailView(PermissionRequiredMixin, DetailView):
    model = models.File
    permission_denied_message = 'You dont have permission to access this file'
    context_object_name = 'file'
    template_name = 'file.html'

    def has_permission(self):
        file = self.get_object()

        if file.owner.pk == self.request.user.id: return True

        fileUserPermission = models.FileUserPermission.objects.filter(user = self.request.user, file = file)
        if len(fileUserPermission): return True

        groups = self.request.user.group_set.all()
        fileGroupPermission = models.FileGroupPermission.filter(group__in = groups, file = file)
        if len(fileGroupPermission): return True

        return False    
