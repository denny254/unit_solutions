# Register your models here.
from django.contrib import admin
from .models import User, Project, Task, Writers, Clients


admin.site.register(Project),
admin.site.register(Task),
admin.site.register(Writers),
admin.site.register(User),
admin.site.register(Clients),
