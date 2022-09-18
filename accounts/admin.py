from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Users)
admin.site.register(models.users_token)
admin.site.register(models.student)
admin.site.register(models.student_token)
admin.site.register(models.libraians)
admin.site.register(models.librarians_token)
admin.site.register(models.Book_details)
admin.site.register(models.library_info)
