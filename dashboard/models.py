from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    password_changed = models.BooleanField(default=False, verbose_name='密码已修改')
    first_login = models.BooleanField(default=True, verbose_name='首次登录')
    last_password_change = models.DateTimeField(null=True, blank=True, verbose_name='最后修改密码时间')
    
    class Meta:
        verbose_name = '用户配置'
        verbose_name_plural = '用户配置'
    
    def __str__(self):
        return f"{self.user.username} 的配置"