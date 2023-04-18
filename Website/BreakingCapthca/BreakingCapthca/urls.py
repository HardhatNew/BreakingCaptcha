
from django.contrib import admin
from django.urls import path, include
from objectDetection import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls'))
]
