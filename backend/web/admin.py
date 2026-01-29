from django.contrib import admin
from web.models.user import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('usr',)  # 逗号千万不能删除！！！
# Register your models here.
