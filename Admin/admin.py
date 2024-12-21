
from django.contrib import admin
from .models import Students, FeeCategories, StudentFeesStatus,Roles


admin.site.register(Students)
admin.site.register(FeeCategories)
admin.site.register(StudentFeesStatus)
admin.site.register(Roles)

