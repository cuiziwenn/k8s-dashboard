from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeMiddleware:
    '''强制首次登录修改密码的中间件'''
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 允许访问的路径（不需要修改密码）
        allowed_paths = [
            reverse('login'),
            reverse('logout'),
            reverse('change_password'),
            '/admin/',
            '/static/',
        ]
        
        # 检查用户是否登录且需要修改密码
        if request.user.is_authenticated:
            # 检查用户是否有 profile
            if not hasattr(request.user, 'profile'):
                from .models import UserProfile
                UserProfile.objects.create(user=request.user, first_login=True)
            
            # 如果是首次登录且未修改密码，重定向到修改密码页面
            if request.user.profile.first_login and not request.user.profile.password_changed:
                current_path = request.path
                if not any(current_path.startswith(path) for path in allowed_paths):
                    return redirect('change_password')
        
        response = self.get_response(request)
        return response