from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'blog'

router = DefaultRouter()
router.register(r'blog', views.BlogViewSet, basename='blog')

urlpatterns = router.urls + [

]
