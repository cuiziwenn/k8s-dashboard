import os
import django  # pyright: ignore[reportMissingImports]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'k8sui.settings')
django.setup()

from django.contrib.auth import get_user_model  # pyright: ignore[reportMissingImports]
from dashboard.models import UserProfile

User = get_user_model()

# 从环境变量读取管理员信息
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'c302894887@163.com')
password = os.environ.get('ADMIN_PASSWORD', 'Admin@123456')

# 检查用户是否已存在
if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    # 创建用户配置，标记为首次登录
    UserProfile.objects.create(
        user=user,
        first_login=True,
        password_changed=False
    )
    print(f"✅ 超级用户 '{username}' 创建成功！")
    print(f"   默认密码: {password}")
    print(f"   首次登录将要求修改密码")
else:
    print(f"ℹ️  超级用户 '{username}' 已存在")
    # 确保已存在的用户有 profile
    user = User.objects.get(username=username)
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(
            user=user,
            first_login=False,
            password_changed=True
        )
        print(f"   已为用户创建配置文件")