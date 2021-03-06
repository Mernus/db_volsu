from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from db_volsu.views import base_page, get_table, disconnect, change_data

urlpatterns = [
    path('', base_page, name='login_page'),
    path('database/disconnect/', disconnect, name='disconnect'),
    path('database/<str:table_name>/', get_table, name='get_table'),
    path('database/<str:table_name>/<str:operation>/', change_data, name='change_data'),
    path('admin/', admin.site.urls),
    path('api/', include('db_volsu.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
