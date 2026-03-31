from django.urls import path

from . import views

urlpatterns = [
    path("", views.address_list, name="address_list"),
    path("delete/<int:pk>/", views.address_delete, name="address_delete"),
    path("find-urls/<int:pk>/", views.find_property_urls, name="find_property_urls"),
]
