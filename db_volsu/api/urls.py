from django.urls import path

from db_volsu.api.views import update_defaults, clear_redis

urlpatterns = [
    path('def_update/', update_defaults),
    path('redis_clear/', clear_redis),
]
