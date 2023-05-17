from django.contrib import admin
from django.urls import path, include
from objectDetection import views, apiTextDetection
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("objectDetection/", views.objectDetection, name="objectDetection"),
    path("textDetection/", views.textDetection, name="textDetection"),
    path("googleTextDetection/", views.googleTextDetection, name="googleTextDetection"),
    path("voiceDetection/", views.voiceDetection, name="voiceDetection"),
    path("members/", include("django.contrib.auth.urls")),
    path("members/", include("members.urls")),
    path("upload-image/", views.uploadFile, name="uploadFile"),
    path("api-text-detection/", views.APITextDetection, name="api-text-detection"),
    path("update-comment/", views.commentUpdate, name="update-comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
