from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from .k8s_client import K8sClient
from .models import UserProfile
from .forms import FirstLoginPasswordChangeForm
import json
from kubernetes import client

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # 记住密码选项
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            
            # 处理"记住我"功能
            if remember_me:
                # 设置 session 过期时间为 30 天
                request.session.set_expiry(2592000)  # 30天的秒数
            else:
                # 浏览器关闭时清除 session
                request.session.set_expiry(0)
            
            # 确保用户有 profile
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
            
            # 检查是否需要修改密码
            if user.profile.first_login and not user.profile.password_changed:
                messages.warning(request, '首次登录，请修改密码！')
                return redirect('change_password')
            
            return redirect('dashboard')
        
        return render(request, 'login.html', {'error': '用户名或密码错误'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def change_password_view(request):
    user = request.user
    
    # 确保用户有 profile
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(user=user)
    
    is_first_login = user.profile.first_login and not user.profile.password_changed
    
    if request.method == 'POST':
        form = FirstLoginPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            
            # 更新用户配置
            user.profile.password_changed = True
            user.profile.first_login = False
            user.profile.last_password_change = timezone.now()
            user.profile.save()
            
            # 更新 session 避免用户被登出
            update_session_auth_hash(request, user)
            
            messages.success(request, '密码修改成功！')
            return redirect('dashboard')
    else:
        form = FirstLoginPasswordChangeForm(user)
    
    return render(request, 'change_password.html', {
        'form': form,
        'is_first_login': is_first_login
    })

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def get_metrics(request):
    k8s = K8sClient()
    metrics = k8s.get_cluster_metrics()
    return JsonResponse(metrics)


@login_required
def namespaces_view(request):
    k8s = K8sClient()
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            k8s.create_namespace(name)
            messages.success(request, f'命名空间 {name} 创建成功！')
            return redirect('namespaces')
        except Exception as e:
            messages.error(request, f'创建失败: {str(e)}')
    
    namespaces = k8s.list_namespaces()
    return render(request, 'namespaces.html', {'namespaces': namespaces})

@login_required
def delete_namespace(request, name):
    k8s = K8sClient()
    try:
        k8s.delete_namespace(name)
        messages.success(request, f'命名空间 {name} 删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')
    return redirect('namespaces')

@login_required
def deployments_view(request):
    k8s = K8sClient()
    namespace = request.GET.get('namespace', 'default')
    deployments = k8s.list_deployments(namespace)
    namespaces = k8s.list_namespaces()
    return render(request, 'deployments.html', {
        'deployments': deployments,
        'namespaces': namespaces,
        'current_namespace': namespace
    })

@login_required
def delete_deployment(request, namespace, name):
    k8s = K8sClient()
    try:
        k8s.delete_deployment(name, namespace)
        messages.success(request, f'Deployment {name} 删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')
    return redirect(f'/deployments/?namespace={namespace}')

@login_required
def pods_view(request):
    k8s = K8sClient()
    namespace = request.GET.get('namespace', 'default')
    pods = k8s.list_pods(namespace)
    namespaces = k8s.list_namespaces()
    return render(request, 'pods.html', {
        'pods': pods,
        'namespaces': namespaces,
        'current_namespace': namespace
    })

@login_required
def delete_pod(request, namespace, name):
    k8s = K8sClient()
    try:
        k8s.delete_pod(name, namespace)
        messages.success(request, f'Pod {name} 删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')
    return redirect(f'/pods/?namespace={namespace}')

@login_required
def services_view(request):
    k8s = K8sClient()
    namespace = request.GET.get('namespace', 'default')
    services = k8s.list_services(namespace)
    namespaces = k8s.list_namespaces()
    return render(request, 'services.html', {
        'services': services,
        'namespaces': namespaces,
        'current_namespace': namespace
    })

@login_required
def delete_service(request, namespace, name):
    k8s = K8sClient()
    try:
        k8s.delete_service(name, namespace)
        messages.success(request, f'Service {name} 删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')
    return redirect(f'/services/?namespace={namespace}')

@login_required
def pvcs_view(request):
    k8s = K8sClient()
    namespace = request.GET.get('namespace', 'default')
    pvcs = k8s.list_pvcs(namespace)
    namespaces = k8s.list_namespaces()
    return render(request, 'pvcs.html', {
        'pvcs': pvcs,
        'namespaces': namespaces,
        'current_namespace': namespace
    })

@login_required
def delete_pvc(request, namespace, name):
    k8s = K8sClient()
    try:
        k8s.delete_pvc(name, namespace)
        messages.success(request, f'PVC {name} 删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')
    return redirect(f'/pvcs/?namespace={namespace}')

@login_required
def pvs_view(request):
    k8s = K8sClient()
    pvs = k8s.list_pvs()
    return render(request, 'pvs.html', {'pvs': pvs})

@login_required
def delete_pv(request, name):
    k8s = K8sClient()
    try:
        k8s.delete_pv(name)
        messages.success(request, f'PV {name} 删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')
    return redirect('pvs')

@login_required
def ingresses_view(request):
    k8s = K8sClient()
    namespace = request.GET.get('namespace', 'default')
    ingresses = k8s.list_ingresses(namespace)
    namespaces = k8s.list_namespaces()
    return render(request, 'ingresses.html', {
        'ingresses': ingresses,
        'namespaces': namespaces,
        'current_namespace': namespace
    })

@login_required
def delete_ingress(request, namespace, name):
    k8s = K8sClient()
    try:
        k8s.delete_ingress(name, namespace)
        messages.success(request, f'Ingress {name} 删除成功！')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')
    return redirect(f'/ingresses/?namespace={namespace}')