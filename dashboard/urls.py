from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('api/metrics/', views.get_metrics, name='metrics'),
    
    path('namespaces/', views.namespaces_view, name='namespaces'),
    path('namespaces/delete/<str:name>/', views.delete_namespace, name='delete_namespace'),
    
    path('deployments/', views.deployments_view, name='deployments'),
    path('deployments/delete/<str:namespace>/<str:name>/', views.delete_deployment, name='delete_deployment'),
    
    path('pods/', views.pods_view, name='pods'),
    path('pods/delete/<str:namespace>/<str:name>/', views.delete_pod, name='delete_pod'),
    
    path('services/', views.services_view, name='services'),
    path('services/delete/<str:namespace>/<str:name>/', views.delete_service, name='delete_service'),
    
    path('pvcs/', views.pvcs_view, name='pvcs'),
    path('pvcs/delete/<str:namespace>/<str:name>/', views.delete_pvc, name='delete_pvc'),
    
    path('pvs/', views.pvs_view, name='pvs'),
    path('pvs/delete/<str:name>/', views.delete_pv, name='delete_pv'),
    
    path('ingresses/', views.ingresses_view, name='ingresses'),
    path('ingresses/delete/<str:namespace>/<str:name>/', views.delete_ingress, name='delete_ingress'),
]
