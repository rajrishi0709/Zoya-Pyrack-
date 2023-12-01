from django.contrib.auth.models import User, Group
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

class Folder(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class File(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='user_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_tasks')
    completed = models.BooleanField(default=False)


class DocumentTask(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_tasks')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_tasks')
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    task_description = models.TextField()

class SharedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
