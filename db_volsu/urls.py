from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from db_volsu.api import urls
from db_volsu.views import base_page, database

urlpatterns = [
    path('', base_page),
    path('database/', database),
    path('admin/', admin.site.urls),
    path('api/', urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
