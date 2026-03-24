from django.urls import path

from . import views

urlpatterns = [
    path("", views.address_list, name="address_list"),
    path("delete/<int:pk>/", views.address_delete, name="address_delete"),
    path("scrape/<int:pk>/", views.scrape_property, name="scrape_property"),
]
