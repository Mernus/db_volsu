from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from db_volsu.views import base_page, get_table

urlpatterns = [
    path('', base_page),
    path('database/', get_table),
    path('database/delete_row', get_table),
    path('admin/', admin.site.urls),
    path('api/', include('db_volsu.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
