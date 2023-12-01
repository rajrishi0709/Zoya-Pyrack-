from rest_framework import serializers
from .models import Company, UserProfile, Folder, File, Task
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta:
        model = UserProfile
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

