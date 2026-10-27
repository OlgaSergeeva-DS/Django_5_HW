"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Импортируем debug_toolbar
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from employees import views as emp_views  # Импорт представлений

urlpatterns = [
    path("admin/", admin.site.urls),
    # Страница входа/выхода
    path("accounts/", include("django.contrib.auth.urls")),
    path("", emp_views.home, name="home"),
    path("employees/", emp_views.employee_list, name="employee_list"),
    path("employees/<int:pk>/", emp_views.employee_detail, name="employee_detail"),
    # Для DjDT дописываем строку
    path("__debug__/", include(debug_toolbar.urls)),
]

# Добавляем маршруты для медиа и статических файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
