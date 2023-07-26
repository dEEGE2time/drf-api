from django.urls import path
from profiles import views


urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    # from views.py implement this to be able to search for specific profiles with id.
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]