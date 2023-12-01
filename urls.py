"""projectName URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from .views import CompanyListCreateView, UserProfileListCreateView, FolderListCreateView, FileListCreateView, TaskListCreateView, FileUploadView, delete_file, FileDashboardView, assign_task 


from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets



# projectName/urls.py









# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('user-profiles/', UserProfileListCreateView.as_view(), name='user-profile-list-create'),
    path('file-upload/', FileUploadView.as_view(), name='file-upload'),
    path('file-dashboard/', FileDashboardView.as_view(), name='file-dashboard'),
    path('assign-task/<int:file_id>/', assign_task, name='assign-task'),
    path('delete-file/<int:file_id>/', delete_file, name='delete-file'),
    path('folders/', FolderListCreateView.as_view(), name='folder-list-create'),
    path('files/', FileListCreateView.as_view(), name='file-list-create'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    #path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
