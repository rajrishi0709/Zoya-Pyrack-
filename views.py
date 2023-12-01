from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Company, UserProfile, Folder, File, Task
from .serializers import CompanySerializer, UserProfileSerializer, FolderSerializer, FileSerializer, TaskSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


# projectName/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .forms import FileUploadForm, DocumentTaskForm
from .models import File, DocumentTask, SharedFile



@method_decorator(login_required, name='dispatch')
class FileDashboardView(View):
    template_name = 'file_dashboard.html'

    def get(self, request):
        user_files = File.objects.filter(user=request.user)
        shared_files = SharedFile.objects.filter(user=request.user)
        return render(request, self.template_name, {'user_files': user_files, 'shared_files': shared_files})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.user = request.user
            new_file.save()
            return redirect('file-dashboard')
        else:
            return render(request, self.template_name, {'form': form})

@login_required
def delete_file(request, file_id):
    file = File.objects.get(pk=file_id)
    file.delete()
    return redirect('file-dashboard')

@login_required
def assign_task(request, file_id):
    file = File.objects.get(pk=file_id)

    if request.method == 'POST':
        form = DocumentTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.sender = request.user
            task.file = file
            task.save()
            return redirect('file-dashboard')
    else:
        form = DocumentTaskForm()

    return render(request, 'assign_task.html', {'form': form, 'file': file})






@method_decorator(login_required, name='dispatch')
class FileUploadView(View):
    template_name = 'file_upload.html'

    def get(self, request):
        form = FileUploadForm()
        files = File.objects.filter(user=request.user)
        return render(request, self.template_name, {'form': form, 'files': files})

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.user = request.user
            new_file.save()
            return redirect('file-upload')
        else:
            files = File.objects.filter(user=request.user)
            return render(request, self.template_name, {'form': form, 'files': files})

@login_required
def delete_file(request, file_id):
    file = File.objects.get(pk=file_id)
    file.delete()
    return redirect('file-upload')


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    def post(self, request, *args, **kwargs):
        # Ensure the user is an Owner before creating a new UserProfile
        if not request.user.groups.filter(name='Owner').exists():
            return Response({'error': 'Only Owners can add staff members.'}, status=status.HTTP_403_FORBIDDEN)

        # Validate and create new UserProfile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class FolderListCreateView(generics.ListCreateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

class FileListCreateView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

