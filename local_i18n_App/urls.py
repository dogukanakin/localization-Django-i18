from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import post_list, category_list
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    # lang değişkenini yakalamak için <str> kullanın
    path('api/posts/', post_list, name='post-list'),
    path('api/categories/', views.category_list),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
