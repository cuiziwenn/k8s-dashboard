from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

class FirstLoginPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label='原密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '请输入原密码'
        })
    )
    new_password1 = forms.CharField(
        label='新密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '请输入新密码（至少8位）'
        }),
        min_length=8,
        help_text='密码至少8位，建议包含大小写字母、数字和特殊字符'
    )
    new_password2 = forms.CharField(
        label='确认新密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '请再次输入新密码'
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError('原密码错误')
        return old_password
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('两次输入的密码不一致')
        return password2
    
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        old_password = self.data.get('old_password')
        
        # 检查新密码不能与旧密码相同
        if password and old_password and password == old_password:
            raise ValidationError('新密码不能与原密码相同')
        
        # 密码强度检查
        if password:
            if len(password) < 8:
                raise ValidationError('密码长度至少8位')
            
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            
            if not (has_upper and has_lower and has_digit):
                raise ValidationError('密码必须包含大写字母、小写字母和数字')
        
        return password
    
    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()
        return self.user