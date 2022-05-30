from django.contrib import admin
from .models import access_group, dept_all, faculty_all, title_all, users_access_group, users_all, users_history

admin.site.register(access_group)
admin.site.register(dept_all)
admin.site.register(faculty_all)
admin.site.register(title_all)
admin.site.register(users_access_group)
admin.site.register(users_all)
admin.site.register(users_history)