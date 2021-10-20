from django.urls import path
from .views import RegisterView, LoginView, LogoutView

app_name ='accounts'
urlpatterns =[
    # typical account stuff, register, login, and logout
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout")
]