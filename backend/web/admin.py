from django.contrib import admin
from web.models.user import UserProfile
from web.models.character import Character, Voice
from web.models.friend import Friend, Message, SystemPrompt

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)  # 逗号千万不能删除！！！

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'voice')

# Voice没有外键，直接添加即可，不用定义class
admin.site.register(Voice)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ('me', 'character',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('friend',)

admin.site.register(SystemPrompt)
