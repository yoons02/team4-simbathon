from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Professor)
admin.site.register(Department)
admin.site.register(Major)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)