from django.urls import path
from .views import RegisterView

app_name ='accounts'
urlpatterns =[
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', RegisterView.as_view(), name="login"),
    path('logout/', RegisterView.as_view(), name="logout")
]