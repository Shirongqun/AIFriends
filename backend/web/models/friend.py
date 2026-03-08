from django.db import models
from django.utils.timezone import now, localtime

from web.models.character import Character
from web.models.user import UserProfile

# 好友
class Friend(models.Model):
    me = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    memory = models.TextField(default="", max_length=5000, blank=True, null=True)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.character.name} - {self.me.user.username} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}"

# 每轮对话
class Message(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    user_message = models.TextField(max_length=5000)  # 用户的消息
    input = models.TextField(max_length=5000)         # 给大模型的输入
    output = models.TextField(max_length=5000)        # 大模型的回复
    input_tokens = models.IntegerField(default=0)     # 输入的token数量
    output_tokens = models.IntegerField(default=0)    # 输出的token数量
    total_tokens = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.friend.character.name} - {self.friend.me.user.username} - {self.user_message[:50]} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}"