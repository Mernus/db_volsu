from django.contrib import admin
from django.urls import path, include
from db_volsu.views import base_page, database
from django.conf import settings

urlpatterns = [
    path('', base_page),
    path('database/', database),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
