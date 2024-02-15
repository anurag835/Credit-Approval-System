from django.urls import path

from . import views

urlpatterns = [
    path(
        "register",
        views.CustomerRegister.as_view(),
        name="customer_register",
    )
]
