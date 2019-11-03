from django.urls import path
from .views import ProfileView, EditProfile

urlpatterns = [
    path('<slug:slug>', ProfileView.as_view(), name="user-profile"),
    path('editprofile/<int:id>/<slug:slug>', EditProfile.as_view(), name="edit-profile")
]