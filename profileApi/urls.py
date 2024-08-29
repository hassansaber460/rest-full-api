from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('hello-viewSet', views.HelloViewSet, basename='hello-viewSet')
router.register('profile', views.UserProfileViewSet)
router.register(r'login', views.LoginViewSet, basename='login')
router.register('feed', views.UserProfileFeedViewSets)
urlpatterns = [
    path('hello-views/', views.HelloApiview.as_view(), name='Hello'),
    path('', include(router.urls))
]
