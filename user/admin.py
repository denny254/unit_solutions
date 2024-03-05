# Register your models here.
from django.contrib import admin
from .models import User, Project, Task, Writer, Client


admin.site.register(Project),
admin.site.register(Task),
admin.site.register(Writer),
admin.site.register(User),
admin.site.register(Client),
