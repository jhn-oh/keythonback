from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Islands, SubGoals, Articles

# 모델 등록
admin.site.register(Islands)
admin.site.register(SubGoals)
admin.site.register(Articles)
