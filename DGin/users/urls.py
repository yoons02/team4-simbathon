from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = "users"
urlpatterns = [
  path('mypage/', mypage, name="mypage"),
  path('mypage_new/', mypage_new, name="mypage_new"),
  path('mypage_create/', mypage_create, name="mypage_create"),
  path('mypage_edit/', mypage_edit, name="mypage_edit"),
  path('mypage_update/', mypage_update,name="mypage_update"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
