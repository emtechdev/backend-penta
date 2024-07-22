from django.urls import path, include
from .views import RegisterAdminView, RegisterDoctorView, RegisterStaffView, LoginView, StaffLoginView
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('staff', views.StaffProfileViewSet)
router.register('room', views.RoomViewSet)
router.register('task', views.TaskViewSet)
router.register('assign', views.AssignViewSet)



urlpatterns = [
    path('register/admin/', RegisterAdminView.as_view(), name='register_admin'),
    path('register/doctor/', RegisterDoctorView.as_view(), name='register_doctor'),
    path('register/staff/', RegisterStaffView.as_view(), name='register_staff'),
    path('login/staff/', StaffLoginView.as_view(), name='staff-login'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),  

]