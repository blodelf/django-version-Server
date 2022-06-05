from django.contrib import admin
from .models import AccessGroup, DeptAll, FacultyAll, TitleAll, UsersAccessGroup, UsersAll, UsersHistory

admin.site.register(AccessGroup)
admin.site.register(DeptAll)
admin.site.register(FacultyAll)
admin.site.register(TitleAll)
admin.site.register(UsersAccessGroup)
admin.site.register(UsersAll)
admin.site.register(UsersHistory)