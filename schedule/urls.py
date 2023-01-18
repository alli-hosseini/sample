from django.urls import path
from . import views


urlpatterns = [
    path("create_schedule/", views.create_schedule),
    path("<str:vendor_id>/", views.get_schedule),
]
