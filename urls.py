from django.urls import path
from . import views
from .views import PlanDelete,PlanDetail,WifiPlanViewSet,UserWifiPlanViewSet

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'wifi-plans', WifiPlanViewSet, basename='wifi-plan')
router.register(r'wifi-plans', views.WifiPlanViewSet)
router.register(r'user-wifi-plans', views.UserWifiPlanViewSet)

from django.urls import path
from .views import WifiPlanViewSet

wifi_plan_list = WifiPlanViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
wifi_plan_detail = WifiPlanViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})




urlpatterns = [
    path('plans/json/', wifi_plan_list, name='wifi_plans'),
    path('', views.wifi_plans_list, name='plan_list'),
    path('plan/<int:pk>/', PlanDetail.as_view(), name='plan_detail'),
    path('plan/new/', views.plan_create, name='plan_create'),
    path('plan/<int:pk>/delete/',PlanDelete.as_view(), name='plan_delete'),
     path('payment/', views.initiate_payment_view, name='initiate_payment'),
]



