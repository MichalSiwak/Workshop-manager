"""mechanics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from car_mechanic.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartPage.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view()),
    path('register/', AddUserView.as_view()),
    path('contact/', ContactView.as_view()),
    path('about/', AboutrView.as_view()),
    path('home/', HomePageView.as_view(), name='home'),
    path('edit_order/<int:number>/', EditOrderView.as_view()),
    path('edit_user/', EditUserView.as_view()),
    path('add_order/', AddOrderView.as_view()),
    path('add_mechanic/', AddMechanicView.as_view(), name='new_mechanic'),
    path('order_list/', OrderListView.as_view()),
    path('edit_mechanic/<int:mechanic_id>/', EditMechanicView.as_view()),
    path('edit_workshop/', EditWorkshopView.as_view(), name='edit_workshop'),
]
