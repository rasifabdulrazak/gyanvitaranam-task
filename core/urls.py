from django.urls import path,include
from rest_framework import routers
from .views import ComapanyViewset,EmployeeViewset,ProfileView,UserRegistrationView,UserLoginView

router = routers.DefaultRouter()

router.register("company", ComapanyViewset, "company")
router.register("employee", EmployeeViewset, "company")
router.register("login", UserLoginView, "login")


urlpatterns = [
    path("",include(router.urls)),
    path('profile-image/',ProfileView.as_view(),name='profile'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    # path('login/',UserLoginView.as_view(),name='login'),
]