from django.urls import path
from . import views

urlpatterns = [
    path("details/<int:id>/", views.details_view, name="details"),
    path("borrow/<int:id>/<int:userid>/", views.borrow_view, name="borrow"),
    path("return/<int:id>/<int:userid>/<int:buyid>/", views.return_view, name="return"),
]
