from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.SignUpView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("editpassword/", views.EditPassword.as_view(), name="editpassword"),
    path("editprofile/", views.edit_profile, name="editprofile"),
]
