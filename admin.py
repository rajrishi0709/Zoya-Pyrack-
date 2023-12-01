# projectName/admin.py

from django.contrib import admin
from .models import Company, UserProfile, Folder, File, Task

admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Folder)
admin.site.register(File)
admin.site.register(Task)

